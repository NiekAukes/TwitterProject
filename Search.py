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


        
        
def test(Tweet):
    newret = dict()
<<<<<<< Updated upstream
    search = input("Search words: ")
    for (key, value) in Tweet.items():
        print("hello")
        if key == search:
            print(key)
=======
    #search = input("Search words: ")
    for (key, value) in Tweet.items():
        print("hello")
>>>>>>> Stashed changes
    
    


if __name__ == "__main__":
    #print((Extract(Classifier.OfficialTweets[1])))
    #SearchTweet(Classifier.OfficialTweets)
    test(Classifier.OfficialTweets)




<<<<<<< Updated upstream








    
    

=======
>>>>>>> Stashed changes
