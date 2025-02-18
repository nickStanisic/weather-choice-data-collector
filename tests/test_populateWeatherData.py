import pytest
from datetime import datetime
from helpers.populateWeatherData import populateWeatherData

def test_populateWeatherData():
    input_data = {
        'cnt': 1,
        'list': [
            {
                'dt': 123456,
                'main': {'temp': 75.0}
            }
        ]
    }
    weather_data = []
    lat = 40.0
    lon = -109.0

    populateWeatherData(input_data, weather_data, lat, lon)

    assert len(weather_data) == 1
    record = weather_data[0]

    assert record[0] == 123456
    assert record[1] == 75.0
    assert record[2] == lat
    assert record[3] == lon
    assert isinstance(record[4], datetime)  

def test_populateWeatherData_multiple():
    """
    Test with multiple entries (cnt > 1).
    """
    input_data = {
        'cnt': 2,
        'list': [
            {'dt': 111111, 'main': {'temp': 70.0}},
            {'dt': 222222, 'main': {'temp': 80.0}},
        ]
    }
    weather_data = []
    lat = 41.0
    lon = -110.0

    populateWeatherData(input_data, weather_data, lat, lon)
    assert len(weather_data) == 2
    assert weather_data[0][0] == 111111
    assert weather_data[1][1] == 80.0
