CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    dt INT,
    temperature FLOAT,
    lat FLOAT,
    lon FLOAT,
    date_time TIMESTAMP
);