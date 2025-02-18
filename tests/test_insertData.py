import pytest
from unittest.mock import patch, MagicMock
from helpers.insertData import insertData

@patch("helpers.insertData.psycopg2.extras.execute_values")
@patch("helpers.insertData.psycopg2.connect")
def test_insertData_with_records(mock_connect, mock_execute_values):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.connection.encoding = "UTF8"

    weather_data = [
        (123456, 75.0, 40.0, -109.0, "2023-01-01 10:00:00"),
        (223456, 65.0, 41.0, -108.0, "2023-01-01 11:00:00"),
    ]

    insertData(weather_data)

    drop_call = ("DROP TABLE IF EXISTS weather;",)
    
    #check if these calls were made once
    mock_cursor.execute.assert_any_call(*drop_call)

    #check that commit was called
    assert mock_conn.commit.called, "Commit was not called"

    #check that cursor and conn was closed
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    mock_execute_values.assert_called_once_with(
        mock_cursor,
        """
                INSERT INTO weather (dt, temperature, lat, lon, date_time)
                VALUES %s;
            """,
        weather_data
    )

@patch("helpers.insertData.psycopg2.connect")
def test_insertData_no_records(mock_connect):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    weather_data = []

    insertData(weather_data)

    #make sure cursor doesnt execute queries
    assert not mock_cursor.executemany.called
    assert mock_cursor.execute.called
