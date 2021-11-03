from eca import *
import eca.http

from eca.generators import start_offline_tweets
import datetime
import textwrap
from WeatherEventGen import *
import Classifier
import WeatherCondition

def isintweet(tweet, criteria):
   text = tweet['text']
   if any(x in text for x in criteria):
      return True
   return False

def Search(json):
   return (Classifier.OfficialTweets[:10], Classifier.RegularTweets[:10])

search = ""

cachedOfficialTweets = []
cachedRegularTweets = []


#Adding a handler for the search button press.
def add_request_handlers(httpd):
    httpd.add_route('/api/search', eca.http.GenerateEvent('Search'), methods=['POST'])
    httpd.add_route('/api/cache', eca.http.GenerateEvent('rqcache'), methods=['POST'])


@event("Search")
def rqSearch(ctx, e):

   sret = Search(e)
   print(e.data)
   global search 
   search = e.data['searchtext']

   rqCache(ctx, e)

@event("rqcache")
def rqCache(ctx, e):
   print("cache requested")
   global search
   for tweet in cachedOfficialTweets:
      print("off")
      if search != "":
         if not isintweet(tweet, search.split()):
            continue
      emit('official', tweet)
   for tweet in cachedRegularTweets:
      print("reg")
      if search != "":
         if not isintweet(tweet, search.split()):
            continue
      emit('regular', tweet)

@event('init')
def setup(ctx, e):
   start_tweets(Classifier.OfficialTweets, time_factor=10000, event_name='chirpofficial')
   start_tweets(Classifier.RegularTweets, time_factor=10000, event_name='chirpregular')
   
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
   tweet = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
   tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'  
   if (len(cachedOfficialTweets) > 5000):
      cachedOfficialTweets.pop()
   cachedOfficialTweets.insert(0, tweet)

   global search
   if search != "":
      if not isintweet(tweet, search.split()):
         return

   emit('official', tweet)
   emit("weather", tweet)

@event('chirpregular')
def tweet(ctx, e):
   # we receive a tweet
   tweet = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
   tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'   

   if (len(cachedRegularTweets) > 5000):
      cachedRegularTweets.pop()
   cachedRegularTweets.insert(0, tweet)

   global search
   if search != "":
      if not isintweet(tweet, search.split()):
         return

   emit('regular', tweet)



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