from WeatherCondition import *
import Tweet
import Classifier

Classifier.OfficialTweets

def SearchTweet(x):
    newret = dict()
    search = input("Search key words: ")
    for (key, value) in x.items():
        if key == search:
            newret[key] = value
    print('Filtered Dictionary : ')
    print(newret)

def Search(Tweet):
    newlist = []
    Tweet1 = 'has_{} 1' .format(Tweet)
    end = Tweet1.find("n_r")
    print(end)
    for i in range(3):
        print(Tweet[i])
    newlist.append(Tweet[14:140])
    print(newlist)



if __name__ == "__main__":
    #print(Classifier.OfficialTweets[0])
    Search(Classifier.OfficialTweets[0])
    #SearchTweet(Classifier.OfficialTweets)
    












    
    

