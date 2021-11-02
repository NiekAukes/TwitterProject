import Tweet
import Classifier

Classifier.OfficialTweets

def Extract(Tweet):
    Humidity = Tweet.find("Hum")
    Time = Tweet.find("-T")
    Wind = Tweet.find("wind")
    AirPressure = Tweet.find("hPa")
    AirStatus = Tweet.find("hPa")
    Rain = Tweet.find("rain")
    UV = Tweet.find("Uv")
    Temp = Tweet.find("-T")

    #Time 
    if Time == -1:
        return None
    else:
        print("Time: " + Tweet[14:22])
    #Humidity in percentage
    if "Hum" in Tweet:
        print("Humidity: " + Tweet[Humidity + 4] + Tweet[Humidity + 5] + " %")
    #Wind in meter per second
    if "wind" in Tweet:
        print("Wind: " + Tweet[Wind + 5] + Tweet[Wind + 6] + Tweet[Wind + 7] + " m/s")
    #Wind direction
    if "wind" in Tweet:
        print("Wind Direction: " + Tweet[Wind + 21] + Tweet[Wind + 22] + Tweet[Wind + 23])
    #Air pressure
    if "hPa" in Tweet:
        print("Air Pressure: " + Tweet[69:76])
    #Air pressure status: Rising/Falling/Steady
    if "hPa" in Tweet:
        print("AP Status: " + "hPa." + Tweet[81:87])
    #Rain in milimeters
    if "rain" in Tweet:
        print("Rain: " + Tweet[Rain + 5] + Tweet[Rain + 6] + Tweet[Rain + 7] + "mm")
    #UV
    if "Uv" in Tweet:
        print("UV: " + Tweet[UV + 3] + Tweet[UV + 4] + Tweet[UV + 5])
    #Temperature
    if "-T" in Tweet:
        print("Temperature: " + Tweet[Time + 4] + Tweet[Time + 5] + Tweet[Time + 6] + " Celcius")



if __name__ == "__main__":
    x = ['has_{} 1'.format(d) for d in Classifier.OfficialTweets]
    print(Classifier.OfficialTweets[10])
    Extract(x[10])


