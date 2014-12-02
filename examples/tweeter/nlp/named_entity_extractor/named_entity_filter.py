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
##                      "description": "named entity extractor",
##                      "required": true,
##                      "type": "TweetString",
##                      "format": "",
##                      "state" : "ENTITIES"
##                  }
##
##          ] }
##END-CONF

import re, os, time
import urllib2
from random import randint
from pumpkin import PmkSeed
from named_entity_extractor import extract_named_entities

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
            entities = extract_named_entities(tw)
            if len(entities) > 0:
                self.dispatch(pkt, ",".join(entities), ENTITIES)
