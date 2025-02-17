import time
import schedule
from helpers.weatherCall import weatherCall
from helpers.populateWeatherData import populateWeatherData
from helpers.insertData import insertData

def get_weather(min_lat, lat_increase, min_lon, lon_increase):
    weather_data = []
    for i in range(min_lat,min_lat - lat_increase, -1):
        for j in range(min_lon, min_lon + lon_increase, 1):
            for n in range(0,4):
                for l in range(0,4):
                    lat = i + n/4
                    lon = j + l/4
                    data = weatherCall(lat, lon)
                    populateWeatherData(data, weather_data, lat, lon)            
    #try to get data into postgresDB
    insertData(weather_data)

schedule.every().day.at("17:50").do(get_weather(40,1,-109,1))

print("Weather data retrieval started, waiting for scheduler")
while True:
    schedule.run_pending()
    time.sleep(60)
