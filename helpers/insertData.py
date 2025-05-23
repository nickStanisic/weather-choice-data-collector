from helpers.database import get_db_connection
import sqlalchemy

def insertData(weather_data):
    try:
        engine = get_db_connection()
        with engine.connect() as conn:
            # Drop and create table
            conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS weather;"))
            
            conn.execute(sqlalchemy.text("""
                CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                dt INT,
                temperature FLOAT,
                lat FLOAT,
                lon FLOAT,
                date_time TIMESTAMP
                );
            """))
            
            # Insert data
            if weather_data:
                insert_query = sqlalchemy.text("""
                    INSERT INTO weather (dt, temperature, lat, lon, date_time)
                    VALUES (:dt, :temp, :lat, :lon, :datetime)
                """)
                
                for record in weather_data:
                    conn.execute(insert_query, {
                        'dt': record[0],
                        'temp': record[1], 
                        'lat': record[2],
                        'lon': record[3],
                        'datetime': record[4]
                    })
                
                conn.commit()
                print(f"Inserted {len(weather_data)} records successfully.")
            
    except Exception as e:
        print(f"Database error: {e}")