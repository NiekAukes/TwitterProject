import datetime

def gethashtagsfromcontent(content):
    return []

class GeoData:
    def __init__(self, x, y):
        self.x = x
        self.y = x

class Tweet:
    def __init__(self, author, date, id, content, author_id):
        self.text
        self.creation_date
        self.geo





        self.author = author #str
        self.dateposted = date #datetime
        self.tweetid = id #int
        self.content = content #str
        self.hashtags = gethashtagsfromcontent(content) #list<str>
        self.author_id = author_id


def gettweetfromjson(jsoncontent):
