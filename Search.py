from WeatherCondition import *
import Tweet
import Classifier

Classifier.OfficialTweets

def isintweet(tweet, criteria):
   #get the text, in a real algorithm, run this with account name too

   text = tweet['text']
   if any(x in text for x in criteria): #simple check i ripped from stackoverflow
      return True
   return False

search = ""

def checksearch(tweet):
   global search #explicitly referencing the global variable search
   if search != "": #check if there is anything searched
      if isintweet(tweet, search.split()): #and run the function i just made
         return True
      else: return False
   return True




if __name__ == "__main__":
    #print(Classifier.OfficialTweets[0])
    checksearch(Classifier.OfficialTweets[0])
    #SearchTweet(Classifier.OfficialTweets)
    












    
    

