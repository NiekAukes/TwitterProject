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

def supertweetgen(data, timescale=1000, begintime="Mon Oct 31 15:55:54 +0000 2011"):

    officialcatchuptweets = []
    regularcatchuptweets = []
    last_time = datetime.strptime(begintime, '%a %b %d %H:%M:%S %z %Y')
    for tweet in data:
        tweet_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        tweet['created_at'] = datetime.strftime(tweet_time, '%a %b %d %H:%M:%S %Y')
        if (tweet_time < last_time):
            #immediately print
            if Classifier.isofficial(tweet):
                officialcatchuptweets.append(tweet)
            else:
                regularcatchuptweets.append(tweet)
        else:
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
                fire_global("chirpregular", tweet)

    if len(officialcatchuptweets) > 0:
        fire_global("chirpofficial", officialcatchuptweets)
        officialcatchuptweets = []
    if len(regularcatchuptweets) > 0:
        fire_global("chirpregular", regularcatchuptweets)
        regularcatchuptweets = []



def custom_tweet_gen(stop, data, time_factor=1000, dateconstraint=False):
    """
    Offline tweet replay.

    Takes a datafile formatted with 1 tweet per line, and generates a sequence of
    scaled realtime items.
    """
    # timing functions return false if we need to abort
    def delayer():
        return not stop.wait(delay / time_factor)

    def immediate():
        return not stop.is_set()

    # select timing function based on time_factor
    delayed = immediate if time_factor is None else delayer


    
    last_time = datetime.strptime("Mon Oct 30 15:55:54 +0000 2011", '%a %b %d %H:%M:%S %z %Y')
    lines = 0
    for tweet in data:
        lines += 1

        # time scale the tweet
        tweet_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        tweetdate = tweet_time.date()
        if ((tweetdate.day is not datetime.today().day) or (tweetdate.month is not datetime.today().month)) and dateconstraint:
            continue
        if (tweet_time < last_time):
            continue

        if not last_time:
            last_time = tweet_time

        wait = tweet_time - last_time 
        delay = wait.total_seconds()

        # delay and yield or break depending on success
        if delayed():
            yield tweet
            last_time = tweet_time
        else:
            break


def start_tweets(data, event_name='tweet', aux_name='tweeter', **kwargs):
    context = get_context()
    if context is None:
        raise NotImplementedError("Can not start offline tweet replay outside of a context.")
    register_auxiliary(aux_name, EventGenerator(context, generator=custom_tweet_gen, data=data, event_name=event_name, **kwargs))
    auxiliary(aux_name).start()
