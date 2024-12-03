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

# Function for Price Distribution for Different Property Types in Each State
def query_property_type_comparison():
    client = bigquery.Client()
    query = """
    WITH FilteredData AS (
        SELECT 
            state_name, 
            property_type, 
            price_aprox_usd
        FROM `bigquery-public-data.properati_properties_br.properties_rent_201802`
        WHERE surface_covered_in_m2 > 0
    )
    SELECT 
        state_name, 
        property_type, 
        MIN(price_aprox_usd) AS min_price, 
        MAX(price_aprox_usd) AS max_price, 
        AVG(price_aprox_usd) AS avg_price
    FROM FilteredData
    GROUP BY state_name, property_type
    ORDER BY state_name;
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]

def query_cheapest_areas():
    client = bigquery.Client()
    query = """
    WITH filtered_data AS (
        SELECT 
            country_name, 
            state_name, 
            price_aprox_usd / surface_covered_in_m2 AS price_per_m2,
            property_type
        FROM `bigquery-public-data.properati_properties_br.properties_rent_201802`
        WHERE surface_covered_in_m2 > 0
    )

    SELECT 
        country_name, 
        state_name, 
        AVG(price_per_m2) AS avg_price_per_m2,
        property_type
    FROM filtered_data
    GROUP BY country_name, state_name, property_type
    ORDER BY avg_price_per_m2 ASC
    LIMIT 50;
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]