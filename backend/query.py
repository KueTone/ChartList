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

# Function to get top affordable places
def query_top_affordable_places():
    client = bigquery.Client()
    query = """
    SELECT 
        place_name, 
        AVG(avg_price) AS avg_price, 
        SUM(number_of_listings) AS total_listings
    FROM (
        SELECT  
            place_name,
            AVG(price) AS avg_price,
            COUNT(*) AS number_of_listings
        FROM 
            `bigquery-public-data.properati_properties_br.properties_rent_201801`
        WHERE 
            price IS NOT NULL
        GROUP BY 
            place_name
        
        UNION ALL
        
        SELECT  
            place_name,
            AVG(price) AS avg_price,
            COUNT(*) AS number_of_listings
        FROM 
            `bigquery-public-data.properati_properties_br.properties_rent_201802`
        WHERE 
            price IS NOT NULL
        GROUP BY 
            place_name
    ) AS top_areas
    GROUP BY 
        place_name
    ORDER BY 
        avg_price ASC
    LIMIT 10;
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]

# Function to compare property types
def query_property_type_comparison():
    client = bigquery.Client()
    query = """
    SELECT 
        property_type,
        AVG(price) AS avg_price,
        COUNT(*) AS number_of_listings
    FROM 
        `bigquery-public-data.properati_properties_br.properties_sell_201801`
    GROUP BY 
        property_type
    UNION ALL
    SELECT 
        property_type,
        AVG(price) AS avg_price,
        COUNT(*) AS number_of_listings
    FROM 
        `bigquery-public-data.properati_properties_br.properties_sell_201802`
    GROUP BY 
        property_type
    ORDER BY 
        avg_price DESC;
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]


