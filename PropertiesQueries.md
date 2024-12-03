# README: Optimized vs. Non-Optimized SQL Queries

This document provides an overview of different SQL queries used for analyzing real estate data. The queries are divided into "optimized" and "not optimized" versions based on performance and best practices for SQL query writing.

## Query Analysis

### 1. Top Affordable Areas

**Non-Optimized Version:**
```sql
SELECT  
    place_name,
    AVG(price) AS avg_price,
    COUNT(*) AS number_of_listings
FROM 
    (SELECT place_name, price, 'rent' AS operation FROM `bigquery-public-data.properati_properties_br.properties_rent_201801`
     UNION ALL
     SELECT place_name, price, 'rent' AS operation FROM `bigquery-public-data.properati_properties_br.properties_rent_201802`) AS all_properties
WHERE 
    operation = 'rent' AND price IS NOT NULL
GROUP BY 
    place_name
ORDER BY 
    avg_price ASC
LIMIT 10;
```

**Optimized Version:**
```sql
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

```

**Explanation:** 
The non-optimized version uses a subquery that combines two separate data sources using `UNION ALL` and filters the result using a `WHERE` clause. The optimized version performs the filtering and grouping operation separately for each data source before combining the results, which reduces the amount of data processed at each step and can improve performance.

### 2. Property Type Comparison

**Non-Optimized Version:**
```sql
SELECT 
    property_type,
    AVG(price) AS avg_price,
    COUNT(*) AS number_of_listings
FROM 
    (SELECT property_type, price FROM `bigquery-public-data.properati_properties_br.properties_sell_201801`
     UNION ALL
     SELECT property_type, price FROM `bigquery-public-data.properati_properties_br.properties_sell_201802`) AS all_properties
GROUP BY 
    property_type
ORDER BY 
    avg_price DESC;
```

**Optimized Version:**
```sql
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
```

**Explanation:**
The non-optimized version aggregates the data from both tables using a subquery, which can be slower for large datasets. The optimized version executes the aggregation independently for each table and then combines the results, making it easier for the database engine to execute and cache intermediate results efficiently.

### 3. Rental Price Trends

**Non-Optimized Version:**
```sql
SELECT 
    EXTRACT(YEAR FROM created_on) AS year,
    EXTRACT(MONTH FROM created_on) AS month,
    AVG(price) AS avg_price
FROM 
    (SELECT created_on, price FROM `bigquery-public-data.properati_properties_br.properties_sell_201801`
     UNION ALL
     SELECT created_on, price FROM `bigquery-public-data.properati_properties_br.properties_sell_201802`) AS all_properties
GROUP BY 
    year, month
ORDER BY 
    year, month;
```

**Optimized Version:**
```sql
SELECT 
    EXTRACT(YEAR FROM created_on) AS year,
    EXTRACT(MONTH FROM created_on) AS month,
    AVG(price) AS avg_price
FROM 
    `bigquery-public-data.properati_properties_br.properties_sell_201801`
GROUP BY 
    year, month
UNION ALL
SELECT 
    EXTRACT(YEAR FROM created_on) AS year,
    EXTRACT(MONTH FROM created_on) AS month,
    AVG(price) AS avg_price
FROM 
    `bigquery-public-data.properati_properties_br.properties_sell_201802`
GROUP BY 
    year, month
ORDER BY 
    year, month;
```

**Explanation:**
The non-optimized version processes the data using a subquery, which can be slower due to the need to materialize the intermediate result. The optimized version runs the extraction and aggregation separately for each table, allowing for more efficient parallel processing and better use of database indexing.

---

## Conclusion

The optimized versions of the SQL queries are designed to execute faster and handle large datasets more efficiently. They avoid complex subqueries and instead leverage separate aggregations for each data source, which allows for better performance and scalability.

