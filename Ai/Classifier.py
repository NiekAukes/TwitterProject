#here, the goal is to create a classifier/algorithm for the provided data.
#we need to seperate official tweets from regular ones
#and we need to get most essential weather tweets, not those that happen to contain 'weer'

# list of tweets ==> list of official + list of regular



OfficialAccounts = ["wska_nl"]
def SeperateTweets(tweetlist):
    officiallist = []
    regularlist = []
    for tweet in tweetlist:
        if tweet.author in OfficialAccounts:
            pass