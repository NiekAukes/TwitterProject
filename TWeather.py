from eca import *
import eca.http as http

from eca.generators import start_offline_tweets
from datetime import datetime
import textwrap
from WeatherEventGen import *
import Classifier
import WeatherCondition
from threading import Thread
from Search import *
from dateutil import parser

MAX_CACHE = 500
GraphMemory = 50
searchval = ""

cachedOfficialTweets = []
cachedRegularTweets = []



#Adding a handler for the search button press.
def add_request_handlers(httpd):
   httpd.add_route('/hello', http.HelloWorld, methods=['GET'])
   httpd.add_route('/api/search', http.GenerateEvent('Search'), methods=['POST'])
   httpd.add_route('/api/cache', http.GenerateEvent('rqcache'), methods=['POST'])

#add event for search
@event("Search")
def rqSearch(ctx, e):
   
   print(e.data)
   global searchval 
   searchval = e.data['search2'] #I don't know why they called it search2

   emit('official', {}) #signal to clear the twitter feed
   emit('regular', {}) #ive made it so that the twitter feed clears when an empty object is sent
   #also request the cache
   fire("rqcache")

@event("rqcache")
def rqCache(ctx, e):
   print("cache requested")
   global searchval
   global minimalscore

   #repush official tweets
   newlist = cachedOfficialTweets
   if searchval != "":
      newlist = [tweet for tweet in cachedOfficialTweets if getSearchPoints(tweet, searchval) > minimalscore]
      
   print("sent list: " + str(len(newlist)))

         
   global GraphMemory
   #only push the last 50 tweets to the weathergraph
   for tweet in newlist[-GraphMemory:]  if len(newlist) > GraphMemory else newlist:
      if tweet['user']['screen_name'] != "wska_nl":
         continue
      weatherCond = WeatherCondition.ExtractWeatherFromTweet(tweet)
      global BaseTime
      #update the graph
      emit('updateGraph',{
      'action': 'add',
      'value': float(weatherCond['temp'].replace(",","."))
      })
      emit('updateWeatherStats',weatherCond)
      
   emit('official', newlist)
   #repush regular tweets
   newlist = cachedRegularTweets
   if searchval != "":
      newlist = [tweet for tweet in cachedRegularTweets if getSearchPoints(tweet, searchval) > minimalscore]
   print("sent list: " + str(len(newlist)))
   emit('regular', newlist)
#import TwitterAPIHandler
import requests
from TwitterAPIHandler import *

classifier_threshold = 1




@event('init')
def setup(ctx, e):
   #thread = Thread(target = supertweetgen, args = (Classifier.data, 10000,))
   #thread.start()
   
   #tweetonce(Classifier.OfficialTweets[0])
   #onReceiveTweet(1)


   
   #i've craeted my own event generator, this allows us to have more control over the generation process
   thread = Thread(target = supertweetgen, args = (Tweet.data, 5000, False, "Dec 25 15:55:54 2011", ))
   thread.start()

   
BaseTime = datetime.strptime("Mon oct 10 00:00:00 2011", '%a %b %d %H:%M:%S %Y')

@event('chirpofficial')
def tweet(ctx, e):
       # we receive a tweet
   tweetls = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   if not isinstance(tweetls, list):
      tweetls = [tweetls]

   #do the same thing with the weathergraph as in rqcache()
   global GraphMemory
   for tweet in tweetls[-GraphMemory:]  if len(tweetls) > GraphMemory else tweetls:
      if tweet['user']['screen_name'] != "wska_nl":
         continue
      weatherCond = WeatherCondition.ExtractWeatherFromTweet(tweet)
      global BaseTime
      #update the graph
      emit('updateGraph',{
      'action': 'add',
      'value': float(weatherCond['temp'].replace(",","."))
      })
      emit('updateWeatherStats',weatherCond)

   for tweet in tweetls:
      #replace user profile if it doesn't exist
      if parser.parse(tweet['created_at']).year < 2021 :
         tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
         tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'  
      if (len(cachedOfficialTweets) > MAX_CACHE):
         cachedOfficialTweets.pop(0)
      cachedOfficialTweets.append(tweet)

      #check if it needs to be filtered
      global searchval
      if not checksearch(tweet, searchval):
         return

   emit('official', tweetls)
   # generate output

   #retrieve weatherconditions from the tweets
   


@event('chirpregular')
def tweet(ctx, e):
   # we receive a tweet

   #most of this is the same as in chirpofficial, so for docs refer to there
   tweetls = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   if not isinstance(tweetls, list):
      tweetls = [tweetls]

   for tweet in tweetls:
      if parser.parse(tweet['created_at']).year < 2021 :
         tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
         tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'  
      if (len(cachedRegularTweets) > MAX_CACHE):
         cachedRegularTweets.pop(0)
      cachedRegularTweets.append(tweet)
      global searchval
      if not checksearch(tweet, searchval):
         return
      
   emit('regular', tweetls)

   