import Tweet
import Classifier

Classifier.OfficialTweets



def Extract(origTweet):

    Tweet = 'has_{} 1' .format(origTweet)
    ret = {}
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
    else:
        splittime = origTweet['created_at'].split()
        ret['Time'] = splittime[0:len(splittime)-2]
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


#test
if __name__ == "__main__":
    #print(Classifier.OfficialTweets[0])
    #print(Extract(Classifier.OfficialTweets[0]))
    #print(Extract(Classifier.OfficialTweets[2]))
    #print("-----------------------")
    #print("-----------------------")
    print(ret)






 
   



