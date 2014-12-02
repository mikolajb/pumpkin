###START-CONF
##{
##"object_name": "sentiment_analyses",
##"object_poi": "qpwo-2345",
##"auto-load": true,
##"remoting" : true,
##"parameters": [
##                 {
##                      "name": "tweet",
##                      "description": "",
##                      "required": true,
##                      "type": "TweetString",
##                      "format": "",
##                      "state" : "ENGLISH"
##                  }
##              ],
##"return": [
##              {
##                      "name": "tweet",
##                      "description": "topic detector",
##                      "required": true,
##                      "type": "TweetString",
##                      "format": "",
##                      "state" : "MOVIE"
##                  }
##
##          ] }
##END-CONF

import re, os, time
import urllib2
from random import randint
from pumpkin import PmkSeed
from topic_detector import TopicDetector

class topic_filter(PmkSeed.Seed):

    def __init__(self, context, poi=None):
        PmkSeed.Seed.__init__(self, context,poi)
        self.wd = self.context.getWorkingDir()

    def on_load(self):
        print "Loading: " + self.__class__.__name__
        url = "URL-TO-DATA-FILE"
        file_name = self.wd+"topic_detection_data.pickle"
        self.get_net_file(url, file_name)
        self.td = TopicDetector(file_name)

    def get_net_file(self, url, file_name):
        #file_name = url.split('/')[-1]
        downloaded = False
        while not downloaded:
            try:
                u = urllib2.urlopen(url)
                f = open(file_name, 'wb')
                meta = u.info()
                file_size = int(meta.getheaders("Content-Length")[0])
                self.logger.info ("Downloading: %s Bytes: %s" % (file_name, file_size))

                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                    #status = status + chr(8)*(len(status)+1)
                    #print status,
                f.close()
                downloaded = True
            except Exception as e:
                self.logger.error("Error downloading, trying again....")
                time.sleep(5)
                pass

    def run(self, pkt, tweet):
        m = re.search('W(\s+)(.*)(\n)', tweet, re.S)
        if m:
            tw = m.group(2)
            if self.td.is_topic('movies', tw):
                self.dispatch(pkt, tweet, "MOVIE")
