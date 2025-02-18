import pytest
from unittest.mock import patch, MagicMock
from helpers.weatherCall import weatherCall
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")


@patch("helpers.weatherCall.requests.get")  
def test_weatherCall_Correct(mock_get):
    """
    Test weatherCall when the request is successful (status_code=200).
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"cnt": 1, "list": []}
    mock_get.return_value = mock_response

    lat = 40.0
    lon = -109.0

    result = weatherCall(lat, lon)

    #test correct response 
    assert result == {"cnt": 1, "list": []}
    #test to see if the correct URL is called and called once
    mock_get.assert_called_once_with(
        f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    )

@patch("helpers.weatherCall.requests.get")
def test_weatherCall_fail(mock_get):
    """
    Test weatherCall if the API responds with an error.
    """
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    lat = 40.0
    lon = -109.0

    result = weatherCall(lat, lon)

    assert result is None 
