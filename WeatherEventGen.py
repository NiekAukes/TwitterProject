from os import times
from threading import Thread
from TwitterAPIHandler import *
import time
from datetime import datetime
from eca import fire_global
from eca.generators import *
import json
import ctypes
import TWeather
from Classifier import *
from Search import *
from eca import fire, get_context, context_switch, register_auxiliary, auxiliary

def processTweet(data, includes):
    try:
      tweetdata = data
      tweetincl = includes
      #print(tweetdata['text'])
   
    except:
      print("something went wrong here")
      return
      #parse data into accepted format
      #data needed:
      #   tweet.user.screen_name
      #   tweet.user.name
      #   tweet.user.profile_image_url
      #   tweet.created_at
      #   tweet.text
      #   tweet.entities
    twet = {}
    twet['user'] = {}
    twet['user']['screen_name'] = tweetincl['users'][0]['username']
    twet['user']['name'] = tweetincl['users'][0]['name']
    twet['user']['profile_image_url'] = tweetincl['users'][0]['profile_image_url']
    twet['created_at'] = datetime.strptime(tweetdata['created_at'], "%Y-%m-%dT%H:%M:%S.000Z").strftime('%a %b %d %H:%M:%S %z %Y')
    twet['text'] = tweetdata['text']
    twet['entities'] = {}
    if "entities" in tweetdata:
      twet['entities']['hashtags'] = []
      twet['entities']['user_mentions'] = []
      twet['entities']['urls'] = []

      if "hashtags" in tweetdata['entities']:
         for item in tweetdata['entities']['hashtags']:
            twet['entities']['hashtags'].append({"text":item['tag'], "indices":[item['start'], item['end']]})

      if "mentions" in tweetdata['entities']:
         for item in tweetdata['entities']['mentions']:
            twet['entities']['user_mentions'].append({"id_str":item["id"],"id":int(item["id"]),"screen_name":item['username'],"name":item['username'], "indices":[item['start'], item['end']]})
      
      if "urls" in tweetdata['entities']:
         for item in tweetdata['entities']['urls']:
            twet['entities']['urls'].append({"url":item['url'],"display_url":item['display_url'], "indices":[item['start'], item['end']]})

    
    if not checksearch(twet):
        return

    if Classifier.isofficial(twet):
        fire_global('chirpofficial', twet)
    else:
        #if Classifier.tweetIsAboutWeather_Certainty(twet) > Classifier.classifier_threshold:
        fire_global("chirpregular", twet)
       

def onReceiveTweet(json_file):
   #if Classifier.tweetIsAboutWeather_Certainty(json_file) < classifier_threshold:
   #   return
   id = json_file['data']['id']
   url = "https://api.twitter.com/2/tweets/{}?{}&{}&{}&{}".format(id, expansions, tweet_fields, user_fields, place_fields)


   resp = requests.request("GET", url, auth=bearer_oauth)

   if resp.status_code != 200:
      raise Exception(
         "Request returned an error: {} {}".format(
            resp.status_code, resp.text
            )
        )
   try:
      tweetdata = json.loads(resp.content)
      tweetincl = tweetdata['includes']
      tweetdata = tweetdata['data']
      processTweet(tweetdata, tweetincl)
   except:
      print(resp.content)





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
    else:
        twitterthread = Thread(target = get_stream, args =(set, onReceiveTweet, ))
        twitterthread.start()
        #repeat it

