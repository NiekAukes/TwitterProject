#here, the goal is to create a classifier/algorithm for the provided data.
#we need to seperate official tweets from regular ones
#and we need to get most essential weather tweets, not those that happen to contain 'weer'

# list of tweets ==> list of official + list of regular
from Tweet import *
OfficialAccounts = ["wska_nl"]
OfficialTweets = []
RegularTweets = []
def isofficial(tweet):
    return tweet['user']['screen_name'] in OfficialAccounts

### FUNCTION FOR DETERMINING IF USERS ARE TALKING ABOUT THE WEATHER OR NOT ###

### EDIT THE THRESHOLD FOR STRICTER SELECTION OF PERSONAL TWEETS ABOUT WEATHER ###
CERTAINTYTHRESHOLD = 1 #amount of keywords found in the message. If it exceeds this threshold, then it'll be displayed.
keywordlist = ['zomer','herfst','winter','temperatuur','barometer','mist',
                'bliksem','dauw','droog','gladheid','gevoelstemperatuur',
                'hagel','hemel','hPA','hittegolf','hitte','klimaat','golf','golven',
                'nat','mist','nat','neerslag','regen','motregen','motsneeuw','nevel',
                'onweer','bui','sneeuw','storm','tropisch','tropen','weerbericht','wervelwind',
                'windhoos','wolken','bries', 'zon'] #not weer because it is already filtered on that.

def tweetIsAboutWeather_Certainty(tweet):
    score = 0

    #generate the word string from the tweet text
    seperatewordlist = [x.lower() for x in (tweet['text'].split())]
    wordsstring = ''.join(seperatewordlist)

    #extract the hashtags from the nested dictionary list (why twitter, why a nested dict list)
    hastagdictlist = tweet['entities']['hashtags']
    hastaglist = []
    for dict in hastagdictlist:
        hastaglist.append(dict['text'])
    hashtags = [x.lower() for x in hastaglist]

    #JOIN THE TWEET TEXT AND THE HASHTAGS
    wordsstring += ''.join(hashtags)

    for keyword in keywordlist:
        for i in range(0, (len(wordsstring) - len(keyword))):
            #check if the keywords match for every possible string made up from the hashtags and the text
            if(wordsstring[i:i+len(keyword)] == keyword):
                score += 1
                #DEBUG: print("found "+wordsstring[i:i+len(keyword)])
    
    if(score > CERTAINTYTHRESHOLD):print("TWEET: "+tweet['text']+" HASHTAGS: "+str(hastaglist)+",SCORE :"+ str(score))
    return score


def SeperateTweets(tweetlist):
    officiallist = []
    regularlist = []
    
    for tweet in tweetlist:
        if tweet['user']['screen_name'] in OfficialAccounts:
            officiallist.append(tweet)
        else:
            #run algorithm to see if the personal tweet is about weather
            if(tweetIsAboutWeather_Certainty(tweet) > CERTAINTYTHRESHOLD):
                regularlist.append(tweet)
    
    return (officiallist,regularlist)


OfficialTweets = SeperateTweets(data)
RegularTweets = OfficialTweets[1]
OfficialTweets = OfficialTweets[0]

print(*[x['text']+"\n" for x in RegularTweets])

if __name__ == "__main__":
    print(SeperateTweets(data)[0][0]['user']['screen_name'])
