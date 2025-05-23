from datetime import datetime
from helpers.weatherCall import weatherCall
from helpers.populateWeatherData import populateWeatherData
from helpers.insertData import insertData

def get_weather(min_lat, lat_increase, min_lon, lon_increase):
    weather_data = []
    
    print(f"[{datetime.utcnow()}] Starting weather data collection...")
    
    for i in range(min_lat, min_lat - lat_increase, -1):
        for j in range(min_lon, min_lon + lon_increase, 1):
            for n in range(0, 8):
                for l in range(0, 8):
                    lat = i + n/8
                    lon = j + l/8
                    data = weatherCall(lat, lon)
                    if data:  # Check if API call was successful
                        populateWeatherData(data, weather_data, lat, lon)
                    else:
                        print(f"Failed to get weather data for lat={lat}, lon={lon}")
    
    # Try to get data into DB
    if weather_data:
        insertData(weather_data)
        print(f"[{datetime.utcnow()}] ✓ Successfully inserted {len(weather_data)} rows")
    else:
        print(f"[{datetime.utcnow()}] ✗ No weather data to insert")

if __name__ == "__main__":
    try:
        get_weather(40, 4, -109, 7)
        print("Weather data collection completed successfully!")
    except Exception as exc:
        # Log the stacktrace so Cloud Logging marks the execution failed
        import traceback
        import sys
        print(f"Error during weather data collection: {exc}")
        traceback.print_exc()
        sys.exit(1)