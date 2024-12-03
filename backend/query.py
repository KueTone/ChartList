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
    SELECT country_name, currency, description, floor, id, place_name, price, property_type, rooms, state_name, title, image_thumbnail 
    FROM `bigquery-public-data.properati_properties_br.properties_sell_201802`
    LIMIT 10
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]


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

# Query to get average value by state, zip code, and property type DONES NOT WORK
def query_average_value():
    client = bigquery.Client()
    query = """
    SELECT 
        state AS State, 
        zip AS Zip_Code, 
        property_type AS Property_Type, 
        AVG(value_50) AS Average_Value
    FROM 
        `bigquery-public-data.us_res_real_est_data.block_value`
    WHERE 
        value_50 IS NOT NULL
    GROUP BY 
        state, zip, property_type
    ORDER BY 
        Average_Value DESC
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]