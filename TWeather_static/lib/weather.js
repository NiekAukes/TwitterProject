//Connect the javascript to the python ECA lib
(function($, block) {
block.fn.weather = function(config) {
    var options = $.extend({
        memory: 20
    }, config);

    //get a reference to all the elements in the WeatherConditions section and Alerts section
    var $img = document.getElementById("weatherimage");
    var $currtemp = document.getElementById("currtemp");
    var $location = document.getElementById("location");
    var $currtime = document.getElementById("currtime");

    var $humidity = document.getElementById("humidity");
    var $wind_spd = document.getElementById("wind_spd");
    var $air_press = document.getElementById("air_press");
    var $rain = document.getElementById("rain");
        
    var $w_alert_img = document.getElementById("alertIcon");
    var $w_alert_text = document.getElementById("alertText");

    // register default handler for updating the weather conditions and weather alerts
    this.actions(function(e, wCond){
        console.log(wCond);
        //convert every dictionary value to a float that needs to be one, I don't want to end up getting javascripted (weird type errors, or none at all when there really should be.)
        w_wind = parseFloat(wCond.wind.replace(",", "."));
        w_uv = parseFloat(wCond.UV.replace(",", ".")); //basically how sunny it is
        w_rain = parseFloat(wCond.rain.replace(",", "."));
        w_temp = parseFloat(wCond.temp.replace(",", "."));
        console.log(w_wind)
        //EXAMPLE TIME: "Tue Oct 11 09:24:35 +0000 2011"
        w_time_hour = wCond.Date.split(" ")[3].split(':')[0]
        
        //set a boolean if it is day or not, to show day/night versions of the weather condition pictures
        isDay = w_time_hour >= 6 && w_time_hour <= 18 ? true : false;
        
        
        var imgurl = "";
        var condition = "";
        // ALGORITHM DO DEDUCT WEATHER CONDITIONS, adjusts picture and text automatically in weatherconditions
        //if Windy
        if(w_wind> 5){
            imgurl = isDay ? "Assets/WeatherCond/animated/cloudy.svg" : "Assets/WeatherCond/animated/cloudy-night-3.svg";
            condition = "windy";
        }
        //if Sunny
        else if(w_uv >= 0.5 && w_rain <= 0.2 && w_wind < 1){
            imgurl = isDay ? "Assets/WeatherCond/animated/day.svg" : "Assets/WeatherCond/animated/night.svg";
            condition = "sunny";
        }
        //if Cloudy
        else if(w_uv < 0.5 && w_rain <= 0.2){
            imgurl = isDay ? "Assets/WeatherCond/animated/cloudy-day-1.svg" : "Assets/WeatherCond/animated/cloudy-night-1.svg";
            condition = "cloudy";
        }
        //if Snowy
        else if(w_rain > 0.2 && w_temp <= 0){
            imgurl = "Assets/WeatherCond/animated/snowy-5.svg";
            condition = "snowy";
        }
        //if Rainy
        else if(w_rain > 0.2){
            imgurl = "Assets/WeatherCond/animated/rainy-1.svg";
            condition = "rainy";
        }
        else{
            imgurl = isDay ? "Assets/WeatherCond/animated/day.svg" : "Assets/WeatherCond/animated/night.svg";
            condition = "neutral";
        }
        $img.src = imgurl;
        
        //set currtemperature, location and time appropriately
        $currtemp.innerHTML = wCond.Temperature + "°C, " + condition;
        $location.innerHTML = wCond.location;
        $currtime.innerHTML = wCond.Date.split(" ")[3];
       
        //also set the humidity, wind speed and air pressure
        $humidity.innerHTML = "Humidity: " + wCond.humidity+"%";
        $wind_spd.innerHTML = "Wind speed: "+wCond.wind + " m/s";
        $air_press.innerHTML = "Air pressure: " +wCond.hpa+ " hPa";
        $rain.innerHTML = "Rain: "+wCond.rain+" mm";
        //....and also check for any crazy weather alerts, to update weather alert section:
        //EXTREME WEATHER
        if(w_temp > 35 || w_temp < -8 || w_wind > 8 || w_rain > 4 || w_uv > 4){
            $w_alert_img.src = "Assets/Circles/svg/RedCircle.svg";
            $w_alert_text.innerHTML = (w_temp > 35 || w_temp < -8) ? "Burning hot weather!" : w_wind > 5 ? "Extreme wind!" : w_rain > 4 ? "Extreme rain!" : "High levels of UV!";
        }
        //MODERATELY EXTREME WEATHER
        else if(w_temp > 25 || w_temp < -2 || w_wind > 4 || w_rain > 2 || w_uv > 2){
            $w_alert_img.src = "Assets/Circles/svg/OrangeCircle.svg";
            $w_alert_text.innerHTML = (w_temp > 25 || w_temp < -2) ? "Hot weather" : w_wind > 3 ? "Moderate wind" : w_rain > 2 ? "Moderate rain" : "Relatively high levels of UV";
        }
        //NORMAL WEATHER
        else{
            $w_alert_img.src = "Assets/Circles/svg/GreenCircle.svg";
            $w_alert_text.innerHTML = "No alerts"
        }
    });
    return this.$element;
};
})(jQuery, block);