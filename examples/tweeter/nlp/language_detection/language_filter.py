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
##                      "state" : "DANISH|DUTCH|ENGLISH|FINNISH|FRENCH|GERMAN|HUNGARIAN|ITALIAN|NORWEGIAN|PORTUGUESE|RUSSIAN|SPANISH|SWEDISH|TURKISH"
##                  }
##
##          ] }
##END-CONF

import re, os, time
import urllib2
from random import randint
from pumpkin import PmkSeed
from language_detector import detect_language

class topic_filter(PmkSeed.Seed):

    def __init__(self, context, poi=None):
        PmkSeed.Seed.__init__(self, context,poi)
        self.wd = self.context.getWorkingDir()

    def on_load(self):
        print "Loading: " + self.__class__.__name__

    def run(self, pkt, tweet):
        m = re.search('W(\s+)(.*)(\n)', tweet, re.S)
        if m:
            tw = m.group(2)
            language = detect_language(tw)
            self.dispatch(pkt, tweet, str.upper(language))
