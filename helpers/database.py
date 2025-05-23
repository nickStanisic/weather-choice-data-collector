import os
import sqlalchemy
from google.cloud.sql.connector import Connector

def get_db_connection():
    """Get database connection for Cloud SQL"""
    if os.getenv('ENVIRONMENT') == 'local':
        # For local testing
        return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
    else:
        # For Cloud Run
        connector = Connector()
        
        def getconn():
            conn = connector.connect(
                os.getenv('CLOUD_SQL_CONNECTION_NAME'),
                "pg8000",
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db=os.getenv('DB_NAME'),
            )
            return conn
        
        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
        return engine