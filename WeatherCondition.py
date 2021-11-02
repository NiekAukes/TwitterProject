class WeatherCon():
    def __init__(self, WState, Temperature, Date, Humidity, Wind, AirPressure):
        self.WState = WState
        self.Temperature = Temperature
        self.Date = Date
        self.Humidity = Humidity
        self.Wind = Wind
        self.AirPressure = AirPressure

    def WeatherState(self):
        if self.Wind > self.AirPressure and self.Wind > self.Humidity:
            self.WState = "Windy"
        if self.AirPressure > self.Wind and self.AirPressure > self.Humidity:
            self.WState = "Dry"
        if self.Humidity > self.AirPressure and self.Humidity > self.Wind:
            self.WState = "Humid"

    def display(self):
        print("Weather State: " + self.WState)
        print("Temperature: " + str(self.Temperature))
        print("Date: " + self.Date)
        print("Humidity: " + str(self.Humidity))
        print("Wind: " + str(self.Wind))
        print("AirPressure: " + str(self.AirPressure))

#test1 = WeatherCon("---", 23, "12/03/2003", 23, 43, 12)
#test2 = WeatherCon("---", 50, "12/04/2020", 50, 10, 34)
#test2.WeatherState()
#test2.display()

test = "07:07:43-T. 5,3\u00baC |Hum 95%-wind 0,0 m/s.(F0bft).--- |\n1020,36 hPa.Rising |rain 2,0 mm |Uv 0,0 | #Buren #weer #weather #rain"
Humidity = test.find("Hum")
Time = test.find("-T")
Wind = test.find("wind")
if "-T" in test:
    print("Time: " + test[0:8])
if "Hum" in test:
    print("Humidity: " + test[Humidity + 4] + test[Humidity + 5])
if "wind" in test:
    print("Wind: " + test[Wind + 5] + test[Wind + 6] + test[Wind + 7])
print(Wind)



    



