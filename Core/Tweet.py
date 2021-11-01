import datetime
import json
from pathlib import Path

class GeoPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = x

class entities:
    def __init__(self, h, um, url):
        self.hashtags
        self.user_mentions
        self.urls

class Place:
    def __init__(self):
        self.place_type
        self.country
        self.ccode
        self.full_name
        self.name
        self.id

#this class is just a databox and multiple instances of the same user can exist
class User:
    def __init__(self):
        self.time_zone
        self.created_at
        self.friends_count
        self.followers_count
        self.location
        self.lang
        self.statuses_count
        self.verified
        self.name
        self.id
        self.favourites_count
        self.screenname #unique


class Tweet:
    def __init__(self):
        self.id
        self.text
        self.creation_date
        self.geo
        self.retweet_count
        self.in_reply_to_status_id_str
        self.in_reply_to_status_id
        self.in_reply_to_user_id_str
        self.coordinates
        self.place
        self.user

import os.path

with open(os.path.abspath('Data\\weer.json')) as json_file:
    data = json.load(json_file)

    print(data[1]['id'])