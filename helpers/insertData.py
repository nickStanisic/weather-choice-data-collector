import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def insertData(weather_data):
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
