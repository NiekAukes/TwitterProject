from eca import *
from eca import emit
import eca.http as http

from eca.generators import start_offline_tweets
import datetime
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

search = ""

def checksearch(tweet):
   global search #explicitly referencing the global variable search
   if search != "": #check if there is anything searched
      if isintweet(tweet, search.split()): #and run the function i just made
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

   sret = Search(e)
   print(e.data)
   global search 
   search = e.data['searchtext']

   emit('official', {}) #signal to clear the twitter feed
   emit('regular', {})

   fire("rqcache")

@event("rqcache")
def rqCache(ctx, e):
   print("cache requested")
   global search

   #repush official tweets
   newlist = cachedOfficialTweets
   if search != "":
      newlist = [tweet for tweet in cachedOfficialTweets if isintweet(tweet, search.split())]
      
   print(len(newlist))
   emit('official', newlist)
   #repush regular tweets
   newlist = cachedRegularTweets
   if search != "":
      newlist = [tweet for tweet in cachedRegularTweets if isintweet(tweet, search.split())]
   emit('regular', newlist)

@event('init')
def setup(ctx, e):
   #start_tweets(Classifier.OfficialTweets, time_factor=10000, event_name='chirpofficial')
   thread = Thread(target = supertweetgen, args = (Classifier.data, 1000,))
   thread.start()
   #start_tweets(Classifier.RegularTweets, time_factor=10000, event_name='chirpregular')
   
   #tweetonce(Classifier.OfficialTweets[0])

def postTweet(tweet, channel):
   global search
   if search != "":
      if not isintweet(tweet, search.split()):
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

      if checksearch(tweet):
             return
      
   emit('official', tweetls)
   
   emit("weather", tweetls[-1])

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

      if checksearch(tweet):
         return
      
   emit('regular', tweetls)



#for updating graph
@event('weather_update_graph_update')
def updateGraph(context,e):
   emit('sample',{
    'action': 'add',
    'value': sample
   })

#for making search functionality work, in progress
@event('search')
def searchbtn(context,e): #WHEN USER WANTS TO SEARCH, DECODE MSG
   pass