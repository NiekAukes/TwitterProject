from eca import *
import eca.http
import random

from eca.generators import start_offline_tweets
import datetime
import textwrap
from WeatherEventGen import *
import Classifier
import WeatherCondition


#Adding a handler for the search button press.
def add_request_handlers(httpd):
    httpd.add_route('/api/search', eca.http.GenerateEvent('search'), methods=['POST'])

@event('init')
def setup(ctx, e):
   start_tweets(Classifier.OfficialTweets, time_factor=10000, event_name='chirpofficial')
   start_tweets(Classifier.RegularTweets, time_factor=10000, event_name='chirpregular')
   
   
   #tweetonce(Classifier.OfficialTweets[0])

@event('chirpofficial')
def tweet(ctx, e):
   # we receive a tweet
   tweet = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
   tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'   

   # generate output
   print(tweet['user']['name'])
   print(tweet['text'])
   emit('official', tweet)
   weatherCond = (WeatherCondition.Extract(tweet))
   print(weatherCond['Temperature'])
   print(weatherCond['Time'])

   emit('updateGraph',{
    'action': 'add',
    'value': {
       'Time':1,#weatherCond['Time'],
       'Temp':weatherCond['Temperature']}
   })


@event('chirpregular')
def tweet(ctx, e):
   # we receive a tweet
   tweet = e.data

   #I've been able to locate the user image urls, because I couldn't stand the 'image not found' icon on every tweet. -Douwe Osinga
   #class of tweet is dict, so try to change the value of the image keys to the default twitter user image.
   tweet['user']['profile_image_url'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
   tweet['user']['profile_image_url_https'] = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'   

   # parse date (NOT USED RIGHT NOW)
   #time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
   
   # nicify text (NOT USED RIGHT NOW)
   #text = textwrap.fill(tweet['text'],initial_indent='    ', subsequent_indent='    ')
   
   #update the weather graph based on location data.
   
   # generate output
   #print(tweet['user']['name'])
   emit('regular', tweet)



#for making search functionality and graph work, in progress
@event('search')
def search(context,e): #WHEN USER WANTS TO SEARCH, DECODE MSG
   print("Testing, is the search button working???")

# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))

   