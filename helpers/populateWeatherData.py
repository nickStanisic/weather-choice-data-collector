from datetime import datetime

def populateWeatherData(data, weather_data, lat, lon):
    for k in range(0,data.get('cnt')):
            date = data.get('list')[k].get('dt')
            temperature = data.get('list')[k].get('main').get('temp')
            dateTime = datetime.now()
            weather_data.append((date, temperature, lat, lon, dateTime))