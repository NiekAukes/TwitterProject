from WeatherCondition import *
import Tweet
import Classifier
import math

Classifier.OfficialTweets

def getSearchPoints(tweet, criteria):
    if criteria == "":
        return True
    score = 0
    #create score modifier
    score_mod = math.e ** (3 * (len(criteria) / len(criteria.split())))
    splt = criteria.split()

    #add score if there's a match for every word 
    if isintweet(tweet['text'], splt):  # and run the function i just made
        score += 1 * score_mod / len(splt)
    if isintweet(tweet['user']['screen_name'], splt):  # and run the function i just made
        score += 1 * score_mod / len(splt)
    if isintweet(tweet['user']['name'], splt):  # and run the function i just made
        score += 1 * score_mod / len(splt)
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %Y')
    for sp in criteria.split():
        try:
            #try to parse time
            pars = parser.parse(sp)
            if pars.day == date.day: 
                score += 1 * score_mod / len(splt)
            if pars.month == date.month: 
                score += 1 * score_mod / len(splt)
            if pars.year == date.year: 
                score += 1 * score_mod / len(splt)
            if pars.day == date.day and pars.month == date.month:
                score += 3 * score_mod / len(splt)
        except:
            pass

    #also score if there's a match on the whole word, extra high score
    score_mod = math.e ** (len(criteria))
    # specific criteria
    if isintweet(tweet['text'], [criteria]):  
        score += 1 * score_mod
    if isintweet(tweet['user']['screen_name'], [criteria]):
        score += 1 * score_mod
    if isintweet(tweet['user']['name'], [criteria]):  
        score += 1 * score_mod
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %Y')
    try:
        pars = parser.parse(criteria)
        if pars.day == date.day:  
            score += 3 * score_mod
        if pars.month == date.month:
            score += 3 * score_mod
        if pars.year == date.year:
            score += 3 * score_mod
        if pars.day == date.day and pars.month == date.month:
            score += 10 * score_mod
    except:
        pass
    return score


if __name__ == "__main__":
    pass


def isintweet(text, criteria):
    # very simple checker

    if any(x in text for x in criteria):  # simple check i ripped from stackoverflow
        return True
    return False


minimalscore = 20


def checksearch(tweet, searchval):
    global minimalscore

    if searchval != "":  # check if there is anything searched
        return getSearchPoints(tweet, searchval) > minimalscore

    return True
