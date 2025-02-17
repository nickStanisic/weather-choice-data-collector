from datetime import datetime
import requests
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("API_KEY")

def weatherCall(lat, lon):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial')
    if response.status_code == 200:
        return response.json()
        