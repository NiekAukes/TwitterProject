from eca import *

from eca.generators import start_offline_tweets
from datetime import datetime
import textwrap
from WeatherEventGen import *
import Classifier
import WeatherCondition
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
   #start_tweets(Classifier.RegularTweets, time_factor=10000, event_name='chirpregular')
   #tweetonce(Classifier.OfficialTweets[0])
   #onReceiveTweet(1)
   
   get_stream(set, onReceiveTweet)

@event('chirpofficial')
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
   
   #plug in weather conditions
   print(tweet)
   print("\n")
   condition = WeatherCondition.Extract(tweet)
   if (condition != None):
         emit("weather", tweet)
   
   # generate output
   emit('official', tweet)

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
   emit('regular', tweet)

@event('weather_update_rawtext_update')
def updateRawText(context  ,e):
       pass

@event('weather_update_graph_update')
def updateGraph(context,e):
   emit('sample',{
    'action': 'add',
    'value': sample
})
