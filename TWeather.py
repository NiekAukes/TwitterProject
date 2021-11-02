from eca import *

from eca.generators import start_offline_tweets
import datetime
import textwrap
from WeatherEventGen import *

@event('init')
def setup(ctx, e):
   start_tweets('data/weer.json', time_factor=10000, event_name='chirp')

@event('chirp')
def tweet(ctx, e):
   # we receive a tweet
   tweet = e.data

   # parse date
   time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

   # nicify text
   text = textwrap.fill(tweet['text'],initial_indent='    ', subsequent_indent='    ')
   print(text)
   # generate output
   emit('official', tweet)