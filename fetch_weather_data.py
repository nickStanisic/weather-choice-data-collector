import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import time
import schedule
from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")


def get_weather(min_lat, lat_increase, min_lon, lon_increase):
    weather_data = []
    for i in range(min_lat,min_lat - lat_increase, -1):
        for j in range(min_lon, min_lon + lon_increase, 1):
            for n in range(0,4):
                for l in range(0,4):
                    lat = i + n/4
                    lon = j + l/4
                    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial')
                    if response.status_code == 200:
                        data = response.json()
                        for k in range(0,data.get('cnt')):
                            date = data.get('list')[k].get('dt')
                            temperature = data.get('list')[k].get('main').get('temp')
                            dateTime = datetime.now()
                            weather_data.append((date, temperature, lat, lon, dateTime))
    #try to get data into postgres
    try: 
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()

        #drop table, if it exists
        cursor.execute(
            """ 
            DROP TABLE IF EXISTS weather;
            """
        )

        #create new weather table
        cursor.execute(
            """ 
            CREATE TABLE IF NOT EXISTS weather (
            id SERIAL PRIMARY KEY,
            dt INT,
            temperature FLOAT,
            lat FLOAT,
            lon FLOAT,
            date_time TIMESTAMP
            );
            """
        )

        #bulk insert data into table 
        if weather_data:
            insert_query = """
                INSERT INTO weather (dt, temperature, lat, lon, date_time)
                VALUES %s;
            """
            psycopg2.extras.execute_values(cursor, insert_query, weather_data)
            conn.commit()
            print(f"Inserted {len(weather_data)} records successfully.")
        else:
            print("No weather data to insert.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Database error: {e}")



schedule.every().day.at("17:50").do(get_weather(40,5,-109,7))

print("Weather data retrieval started, waiting for scheduler")
while True:
    schedule.run_pending()
    time.sleep(60)
