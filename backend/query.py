from google.cloud import bigquery
from mysql.connector import connect, Error
import os

# Database configuration
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
}

# Function to get database connection
def get_db_connection():
    try:
        conn = connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise Exception("Database connection failed.")

# Query BigQuery
def query_block_value():
    client = bigquery.Client()
    query = """
    SELECT *
    FROM `bigquery-public-data.us_res_real_est_data.block_value`
    LIMIT 10
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]
