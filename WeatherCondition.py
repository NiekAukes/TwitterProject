import Tweet
import Classifier
from datetime import datetime
Classifier.OfficialTweets

def ExtractWeatherFromTweet(Tweet):
    newlist = []
    ret = {
    "Date":Tweet['created_at'],
    "location":Tweet['place']['full_name']

    }
    Humidity = Tweet['text'].find("Hum")
    Wind = Tweet['text'].find("wind")
    AirPressure = Tweet['text'].find("hPa") # ... hpa
    Rain = Tweet['text'].find("rain")
    UV = Tweet['text'].find("Uv")
    Temp = Tweet['text'].find("-T")

    ret['temp'] = Tweet['text'][Temp + 4: Temp + 8].replace("º", "")
    ret['humidity'] = Tweet['text'][Humidity + 4:Humidity + 6]
    ret['wind'] = Tweet['text'][Wind + 5:Wind + 8]
    ret['hpa'] = Tweet['text'][AirPressure - 8: AirPressure - 1]
    ret['hpastatus'] = ""

    #count until end of word
    index = AirPressure + 4
    while(Tweet['text'][index] != " "):
        ret['hpastatus'] += Tweet['text'][index]
        index += 1

    
    ret['rain'] = Tweet['text'][Rain + 5: Rain + 9].replace(" ", "")
    ret['UV'] = Tweet['text'][UV + 2:UV + 6].replace(" ", "")

    #Date, Created At [439:449]
    return ret

    

def Extract(Tweet):
    newlist = []
    ret = {}
    Tweet = 'has_{} 1' .format(Tweet)
    Humidity = Tweet.find("Hum")
    Time = Tweet.find("-T")
    Wind = Tweet.find("wind")
    AirPressure = Tweet.find("hPa")
    AirStatus = Tweet.find("hPa")
    Rain = Tweet.find("rain")
    UV = Tweet.find("Uv")
    Temp = Tweet.find("-T")
    Date = Tweet.find("created_at")
    location = Tweet.find("full_name")
    #Time 
    if Time == -1:
        return None
    elif Tweet[Date + 13] == "'":
        i = 1
        tempT = []
        for i in range(8):
            tempT.append(Tweet[Date + 25 + i])
            i += 1
        z = ''.join(tempT)
        ret['Time'] = z
    #Humidity in percentage
    if Humidity == -1:
        return None
    else:
        ret['Humidity'] = Tweet[Humidity + 4] + Tweet[Humidity + 5]
    #Wind in meter per second
    if Wind == -1:
        return None
    else:
        ret['Wind'] = Tweet[Wind + 5] + Tweet[Wind + 6] + Tweet[Wind + 7]
    #Wind direction
    if Wind == -1:
        return None
    else:
        ret['Wind Direction'] = Tweet[Wind + 21] + Tweet[Wind + 22] + Tweet[Wind + 23]
    #Air pressure
    if AirPressure == -1:
        return None
    else:
        ret['Air Pressure'] = Tweet[69:76]
    #Air pressure status: Rising/Falling/Steady
    if AirPressure == -1:
        return None
    else:
        ret['AP Status'] = Tweet[81:87]
    #Rain in milimeters
    if Rain == -1:
        return None
    else:
        ret['Rain'] = Tweet[Rain + 5] + Tweet[Rain + 6] + Tweet[Rain + 7]
    #UV
    if UV == -1:
        return None
    else:
        ret['UV'] = Tweet[UV + 3] + Tweet[UV + 4] + Tweet[UV + 5]
    #Temperature
    if Temp == -1:
        return None
    elif Tweet[Temp + 2] == ".":
        i = 1
        temp1 = []
        while Tweet[Temp + 2 + i] != "º":
            temp1.append(Tweet[Temp + 2 + i])
            i += 1
        x = ''.join(temp1)
        ret['Temperature'] = x
    #Date, Created At [439:449]
    if Date == -1:
        return None
    elif Tweet[Date + 13] == "'":
        i = 1
        temp = []
        for j in range(10,):
            temp.append(Tweet[Date + 14 + j])
            i += 1
        k = ''.join(temp)
        ret['Date'] = k
    #location
    if location == -1:
        return None
    elif Tweet[location + 12] == "'":
        i = 1
        temp2 = []
        while Tweet[location + 12 + i] != "'":
            temp2.append(Tweet[location + 12 + i])
            i += 1
        j = ''.join(temp2)
        ret['location'] = j
    return ret

def AllTweets(Tweet):
    for i in range(len(Tweet)):
        print(Extract(Classifier.OfficialTweets[i]))


#test
if __name__ == "__main__":

    #print(Classifier.OfficialTweets[400])
    print(ExtractWeatherFromTweet(Classifier.OfficialTweets[400]))
    #print(Classifier.OfficialTweets[0])
    #print(Extract(Classifier.OfficialTweets[0]))
    #print("-----------------------")
    #print("-----------------------")
    #print(ret)






 
   



