import datetime

def gethashtagsfromcontent(content):
    return []

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
    def __init__(self, h, um, url):
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
    def __init__(self, author, date, id, content, author_id):
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




        self.author = author #str
        self.dateposted = date #datetime
        self.tweetid = id #int
        self.content = content #str
        self.hashtags = gethashtagsfromcontent(content) #list<str>
        self.author_id = author_id


def gettweetfromjson(jsoncontent):
    pass