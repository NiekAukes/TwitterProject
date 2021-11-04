from os import times
import threading
import time
from datetime import datetime
from eca import fire_global
from eca.generators import *
import json
import ctypes
import TWeather
import Classifier
from eca import fire, get_context, context_switch, register_auxiliary, auxiliary

def supertweetgen(datacpy, timescale=1000, loop=True, begintime="Mon Nov 28 15:55:54 +0000 2011", classifier_threshold = 2):
    #our own event generator, 
    # if tweets are before begintime, all of them will be sent at once
    #we've also made changes to javascript lib functions to create more functionality
    data = datacpy[:]
    officialcatchuptweets = []
    regularcatchuptweets = []
    last_time = datetime.strptime(begintime, '%a %b %d %H:%M:%S %z %Y')
    for tweet in data:
        tweet_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        tweet['created_at'] = datetime.strftime(tweet_time, '%a %b %d %H:%M:%S %Y') #fix the date so timezone isn't shown
        if (tweet_time < last_time):
            #immediately print
            if Classifier.isofficial(tweet):
                officialcatchuptweets.append(tweet)
            else:
                if(Classifier.tweetIsAboutWeather_Certainty(tweet) > classifier_threshold):
                    regularcatchuptweets.append(tweet)
        else:
            #send all tweets with fire_global
            if len(officialcatchuptweets) > 0:
                fire_global("chirpofficial", officialcatchuptweets)
                officialcatchuptweets = []
            if len(regularcatchuptweets) > 0:
                fire_global("chirpregular", regularcatchuptweets)
                regularcatchuptweets = []

            #delay the tweet
            wait = tweet_time - last_time
            delay = wait.total_seconds() / timescale

            last_time = tweet_time
            time.sleep(delay)
            if Classifier.isofficial(tweet):
                fire_global("chirpofficial", tweet)
            else:
                if(Classifier.tweetIsAboutWeather_Certainty(tweet) > classifier_threshold):
                    fire_global("chirpregular", tweet)

    if len(officialcatchuptweets) > 0:
        fire_global("chirpofficial", officialcatchuptweets)
        officialcatchuptweets = []
    if len(regularcatchuptweets) > 0:
        fire_global("chirpregular", regularcatchuptweets)
        regularcatchuptweets = []
    if (loop):
        supertweetgen(datacpy, timescale=1000, loop=True, begintime=begintime, classifier_threshold = 2)
        #repeat it

