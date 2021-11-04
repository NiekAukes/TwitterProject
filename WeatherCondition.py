import Tweet
import Classifier
from datetime import datetime
Classifier.OfficialTweets

#main function to extract info from the tweets
def ExtractWeatherFromTweet(Tweet):
    #ret is the dictionary that stored the extracted info from the tweets.
    #e.g. {location: amsterdam, Humidity: 94% .....}
    ret = {
    "Date":Tweet['created_at'],       #this is the date and location of the tweets
    "location":Tweet['place']['full_name']
    }

    #finding each Criteria from the tweets
    Humidity = Tweet['text'].find("Hum")
    Wind = Tweet['text'].find("wind")
    AirPressure = Tweet['text'].find("hPa") # ... hpa
    Rain = Tweet['text'].find("rain")
    UV = Tweet['text'].find("Uv")
    Temp = Tweet['text'].find("-T")

    #storing the right value in the dictionary ret.
    ret['temp'] = Tweet['text'][Temp + 4: Temp + 8].replace("º", "")
    ret['humidity'] = Tweet['text'][Humidity + 4:Humidity + 6]
    ret['wind'] = Tweet['text'][Wind + 5:Wind + 8]
    ret['hpa'] = Tweet['text'][AirPressure - 8: AirPressure - 1].replace("\n", "")
    ret['hpastatus'] = ""

    #count until end of word
    index = AirPressure + 4
    while(Tweet['text'][index] != " "):
        ret['hpastatus'] += Tweet['text'][index]
        index += 1

    #storing the right value in the dictionary ret.
    ret['rain'] = Tweet['text'][Rain + 5: Rain + 9].replace(" ", "")
    ret['UV'] = Tweet['text'][UV + 2:UV + 6].replace(" ", "")

    return ret

#test
if __name__ == "__main__":
    #print(Classifier.OfficialTweets[400])
    print(ExtractWeatherFromTweet(Classifier.OfficialTweets[0]))
    




 
   



