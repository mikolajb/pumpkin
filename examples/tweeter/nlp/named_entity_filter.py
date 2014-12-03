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
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

class topic_filter(PmkSeed.Seed):

    def __init__(self, context, poi=None):
        PmkSeed.Seed.__init__(self, context,poi)
        self.wd = self.context.getWorkingDir()

    def on_load(self):
        print "Loading: " + self.__class__.__name__

    def extract_named_entities(text):
        sentences = sent_tokenize(text)
        sentences = [word_tokenize(sent) for sent in sentences]
        sentences = [pos_tag(sent) for sent in sentences]
        result = []
        for sent in sentences:
            result += [word[0] for word, tag in ne_chunk(sent, binary=True).pos()
                       if tag == 'NE']
        return result

    def run(self, pkt, tweet):
        m = re.search('W(\s+)(.*)(\n)', tweet, re.S)
        if m:
            tw = m.group(2)
            entities = self.extract_named_entities(tw)
            if len(entities) > 0:
                self.dispatch(pkt, ",".join(entities), ENTITIES)
