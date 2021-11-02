import Tweet
import Classifier

Classifier.OfficialTweets

ret = {}

def Extract(Tweet):
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
        ret['Time'] = Tweet[14:22]     
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
    else:
        ret['Temp'] = Tweet[Time + 4] + Tweet[Time + 5] + Tweet[Time + 6]
    #Date, Created At
    if Date == -1:
        return None
    else:
        ret['Date'] = Tweet[439:449]
    #location
    if location == -1:
        return None
    elif Tweet[location + 12] == "'":
        i = 1
        temp = []
        while Tweet[location + 12 + i] != "'":
            temp.append(Tweet[location + 12 + i])
            i += 1
        j = ''.join(temp)
        ret['location'] = j
   
    return ret
    

def SearchTweet(Tweet, ret):
    while True:
        try:
            # Note: Python 2.x users should use raw_input, the equivalent of 3.x's input
            Item = input("Search by: ")
        except ValueError:
            print("Sorry, I didn't understand that.")
            #better try again... Return to the start of the loop
            continue
        else:
            #age was successfully parsed!
            #we're ready to exit the loop.
            break
    if Item.lower == "time" or Item.lower == "humidity" or Item.lower == "wind" or Item.lower == "wind direction"  or Item.lower == "air pressure"  or Item.lower == "air pressure"  or Item.lower == "rain" or Item.lower == "uv" or Item.lower == "temperature" or Item.lower == "date"  or Item.lower == "location":
        print("valid")
    else:
        False



    
    




#test
if __name__ == "__main__":
    x = ['has_{} 1'.format(d) for d in Classifier.OfficialTweets]
   # print(Classifier.OfficialTweets[0])
    print("-----------------------")
    print("-----------------------")
    #Extract(x[0])
    #print(ret)
    SearchTweet(x, ret)






 #if Item.lower == "time" or Item.lower == "humidity" or Item.lower == "wind" or Item.lower == "wind direction"  or Item.lower == "air pressure"  or Item.lower == "air pressure"  or Item.lower == "rain" or Item.lower == "uv" or Item.lower == "temperature" or Item.lower == "date"  or Item.lower == "location":   
   



