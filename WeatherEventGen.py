import threading
import time
from datetime import datetime
from eca.generators import *
import json
from eca import fire, get_context, context_switch, register_auxiliary, auxiliary

def custom_tweet_gen(stop, data, time_factor=1000, dateconstraint=False):
    """
    Offline tweet replay.

    Takes a datafile formatted with 1 tweet per line, and generates a sequence of
    scaled realtime items.
    """
    # timing functions return false if we need to abort
    def delayer(duration):
        return not stop.wait(delay / time_factor)

    def immediate(duration):
        return not stop.is_set()

    # select timing function based on time_factor
    delayed = immediate if time_factor is None else delayer


    
    last_time = None
    lines = 0
    for tweet in data:
        lines += 1

        # time scale the tweet
        tweet_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        tweetdate = tweet_time.date()
        if ((tweetdate.day is not datetime.today().day) or (tweetdate.month is not datetime.today().month)) and dateconstraint:
            continue

        if not last_time:
            last_time = tweet_time
            
        wait = tweet_time - last_time 
        delay = wait.total_seconds()
   
            # delay and yield or break depending on success
        if delayed(delay):
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
