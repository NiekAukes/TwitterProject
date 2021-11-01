#here, the goal is to create a classifier/algorithm for the provided data.
#we need to seperate official tweets from regular ones
#and we need to get most essential weather tweets, not those that happen to contain 'weer'

# list of tweets ==> list of official + list of regular
from Tweet import *
OfficialAccounts = ["wska_nl"]


def SeperateTweets(tweetlist):
    officiallist = []
    regularlist = []
    for tweet in tweetlist:
        if tweet['user']['screen_name'] in OfficialAccounts:
            officiallist.append(tweet)
        else:
            regularlist.append(tweet)
    
    return (officiallist,regularlist)

if __name__ == "__main__":
    print(SeperateTweets(data)[0][0]['user']['screen_name'])