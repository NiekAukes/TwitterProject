from eca import *

from eca.generators import start_offline_tweets
import datetime
import textwrap
from WeatherEventGen import *
import Classifier

@event('init')
def setup(ctx, e):
   start_tweets(Classifier.RegularTweets, time_factor=100000, event_name='chirp')
   #tweetonce(Classifier.OfficialTweets[0])

@event('chirp')
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
   emit('official', tweet)
   emit("weather", tweet)

@event('weather_update_rawtext_update')
def updateRawText(context  ,e):
       pass

@event('weather_update_graph_update')
def updateGraph(context,e):
   emit('sample',{
    'action': 'add',
    'value': sample
})
