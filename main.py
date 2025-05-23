from datetime import datetime
import schedule
from helpers.weatherCall import weatherCall
from helpers.populateWeatherData import populateWeatherData
from helpers.insertData import insertData

def get_weather(min_lat, lat_increase, min_lon, lon_increase):
    weather_data = []
    for i in range(min_lat,min_lat - lat_increase, -1):
        for j in range(min_lon, min_lon + lon_increase, 1):
            for n in range(0,8):
                for l in range(0,8):
                    lat = i + n/8
                    lon = j + l/8
                    data = weatherCall(lat, lon)
                    populateWeatherData(data, weather_data, lat, lon)            
    #try to get data into DB
    insertData(weather_data)
    print(f"[{datetime.utcnow()}] ✓ inserted {len(weather_data)} rows")

if __name__ == "__main__":
    try:
        get_weather(40,4,-109,7)
    except Exception as exc:
        # Log the stacktrace so Cloud Logging marks the execution failed
        import traceback, sys
        traceback.print_exc()
        sys.exit(1)
