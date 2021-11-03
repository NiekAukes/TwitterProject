from eca import *
from eca import emit
import eca.http as http

from eca.generators import start_offline_tweets
from datetime import datetime
import textwrap
from WeatherEventGen import *
import Classifier
import WeatherCondition
from threading import Thread

MAX_CACHE = 500

def isintweet(tweet, criteria):
   #get the text, in a real algorithm, run this with account name too

   text = tweet['text']
   if any(x in text for x in criteria): #simple check i ripped from stackoverflow
      return True
   return False

searchval = ""

def checksearch(tweet):
   global searchval #explicitly referencing the global variable search
   if searchval != "": #check if there is anything searched
      if isintweet(tweet, searchval.split()): #and run the function i just made
         return True
      else: return False
   return True
         

cachedOfficialTweets = []
cachedRegularTweets = []



#Adding a handler for the search button press.
def add_request_handlers(httpd):
    httpd.add_route('/api/search', http.GenerateEvent('Search'), methods=['POST'])
    httpd.add_route('/api/cache', http.GenerateEvent('rqcache'), methods=['POST'])


@event("Search")
def rqSearch(ctx, e):
   print(e.data)
   global searchval 
   searchval = e.data['search2'] #I don't know why they called it search2

   emit('official', {}) #signal to clear the twitter feed
   emit('regular', {})

   fire("rqcache")

@event("rqcache")
def rqCache(ctx, e):
   print("cache requested")
   global searchval

   #repush official tweets
   newlist = cachedOfficialTweets
   if searchval != "":
      newlist = [tweet for tweet in cachedOfficialTweets if isintweet(tweet, searchval.split())]
      
   print("sent list: " + str(len(newlist)))
   emit('official', newlist)
   #repush regular tweets
   newlist = cachedRegularTweets
   if searchval != "":
      newlist = [tweet for tweet in cachedRegularTweets if isintweet(tweet, searchval.split())]
   print("sent list: " + str(len(newlist)))
   emit('regular', newlist)
#import TwitterAPIHandler
import requests
from TwitterAPIHandler import *

def onReceiveTweet(json_file):
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
      print(tweetdata['text'])
   
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
   emit('official', twet)
   #id = json_file['data']['id']
   #url = "https://api.twitter.com/2/tweets?ids={}&{}".format(id,tweet_fields)
#
   #resp = requests.request("Get", "https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/{}".format(id))
#
   #if resp.status_code != 200:
   #     raise Exception(
   #         "Request returned an error: {} {}".format(
   #             resp.status_code, resp.text
   #         )
   #     )
   #try:
   #     tweetdata = json.loads(resp.content)
   #     emit('modern', tweetdata)
   #except:
   #     pass
       

@event('init')
def setup(ctx, e):
   #start_tweets(Classifier.OfficialTweets, time_factor=10000, event_name='chirpofficial')
   thread = Thread(target = supertweetgen, args = (Classifier.data, 10000,))
   thread.start()
   #start_tweets(Classifier.RegularTweets, time_factor=10000, event_name='chirpregular')
   
   
   #tweetonce(Classifier.OfficialTweets[0])
   #onReceiveTweet(1)
   
   get_stream(set, onReceiveTweet)

def postTweet(tweet, channel):
   global searchval
   if searchval != "":
      if not isintweet(tweet, searchval.split()):
         return
   
   emit(channel, tweet)



@event('chirpofficial')
def tweet(ctx, e):
   # we receive a tweet
   tweetls = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   if not isinstance(tweetls, list):
      tweetls = [tweetls]

   for tweet in tweetls:
      tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
      tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'  
      if (len(cachedOfficialTweets) > MAX_CACHE):
         cachedOfficialTweets.pop(0)
      cachedOfficialTweets.append(tweet)

      if not checksearch(tweet):
         return
   emit('official', tweetls)
   # generate output

   #retrieve weatherconditions from the tweets
   weatherCond = (WeatherCondition.Extract(tweetls[-1]))

   #update the graph
   emit('updateGraph',{
    'action': 'add',
    'value': {
       'series0':1,#weatherCond['Time'],
       'series1':weatherCond['Temperature']}
   })
   emit('updateWeatherStats',weatherCond)


@event('chirpregular')
def tweet(ctx, e):
   # we receive a tweet
   tweetls = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   if not isinstance(tweetls, list):
      tweetls = [tweetls]

   for tweet in tweetls:
      tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
      tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'  
      if (len(cachedRegularTweets) > MAX_CACHE):
         cachedRegularTweets.pop(0)
      cachedRegularTweets.append(tweet)

      if not checksearch(tweet):
         return
      
   emit('regular', tweetls)



# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))

   