from WeatherCondition import *
import Tweet
import Classifier
from dateutil import parser
import math





def stdcomp(obj, args):
    return obj
def mergesort(data, key = stdcomp, keyargs = ()):
    datacpy = data.copy()

    
    if (len(datacpy) > 2): #if the remaining list length is greater than 2, then subdivide into smaller lists
        pt1 = datacpy[:len(datacpy)//2]
        pt2 = datacpy[len(datacpy)//2:]
        pt1 = mergesort(pt1, key, keyargs) #and apply 2 branch recursions
        pt2 = mergesort(pt2, key, keyargs)

        endarray = pt1.copy() #do a single-iteration insertion algo to combine 2 lists
        i = 0
        
        for element in pt2:
            while(i < len(endarray)):
                
                if (key(endarray[i], keyargs) > key(element, keyargs)):
                    break
                i += 1
            endarray.insert(i, element)
        return endarray     # end of insertion algo

    else:               # if the remaining list length is 2 or smaller, then compare or return if it's a single value 
        if (len(datacpy) < 2):
            return datacpy
        if key(datacpy[0], keyargs) > key(datacpy[1], keyargs):
            datacpy[0], datacpy[1] = datacpy[1], datacpy[0]
            
        return datacpy


def getSearchPoints(tweet, criteria):
    if criteria == "":
        return True
    score = 0
    score_mod = math.e ** (3* (len(criteria) / len(criteria.split())))
    splt = criteria.split()
    if isintweet(tweet['text'], splt): #and run the function i just made
        score += 1 * score_mod / len(splt)
    if isintweet(tweet['user']['screen_name'], splt): #and run the function i just made
        score += 1 * score_mod / len(splt)
    if isintweet(tweet['user']['name'],splt): #and run the function i just made
        score += 1 * score_mod / len(splt)
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %Y')
    for sp in criteria.split():
        try:
            pars = parser.parse(sp)
            if pars.day == date.day: #and run the function i just made
                score += 1 * score_mod / len(splt)
            if pars.month == date.month: #and run the function i just made
                score += 1 * score_mod / len(splt)
            if pars.year == date.year: #and run the function i just made
                score += 1 * score_mod / len(splt)
            if pars.day == date.day and pars.month == date.month:
                score += 3 * score_mod / len(splt)
        except:
            pass
    
    score_mod = math.e ** (len(criteria))
    #specific criteria
    if isintweet(tweet['text'], [criteria]): #and run the function i just made
        score += 1 * score_mod
    if isintweet(tweet['user']['screen_name'], [criteria]): #and run the function i just made
        score += 1 * score_mod
    if isintweet(tweet['user']['name'], [criteria]): #and run the function i just made
        score += 1 * score_mod
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %Y')
    try:
        pars = parser.parse(criteria)
        if pars.day == date.day: #and run the function i just made
            score += 3 * score_mod
        if pars.month == date.month: #and run the function i just made
            score += 3 * score_mod
        if pars.year == date.year: #and run the function i just made
            score += 3 * score_mod
        if pars.day == date.day and pars.month == date.month:
            score += 10 * score_mod
    except:
        pass
    return score


if __name__ == "__main__":
    #print(Classifier.OfficialTweets[0])
    #Search(Classifier.OfficialTweets[0])
    #SearchTweet(Classifier.OfficialTweets)
    serch = "ws"
    minscore = 30
    me = [(getSearchPoints(data, serch), data) for data in Classifier.OfficialTweets]
    me = [(score, data)for (score,data) in me if score > minscore]
    sort = sorted(me, key=lambda x: x[0])
    result = [data for score, data in sort]

    print(result)
    

def isintweet(text, criteria):
       #get the text, in a real algorithm, run this with account name too

   if any(x in text for x in criteria): #simple check i ripped from stackoverflow
      return True
   return False

minimalscore = 20
def checksearch(tweet, searchval):
    global minimalscore

    print(searchval)
    if searchval != "": #check if there is anything searched
      return getSearchPoints(tweet, searchval) > minimalscore #and run the function i just made

    return True










    
    

