# README: Optimized vs. Non-Optimized SQL Queries

This document provides an overview of different SQL queries used for analyzing real estate data. The queries are divided into "optimized" and "not optimized" versions based on performance and best practices for SQL query writing.

## Query Analysis

### 1. Top Affordable Areas To Rent

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

![Query 1 Output](images/Qq1.png)
### 2. Property Type Comparison

**Non-Optimized Version:**
    Direct filtering in the main query:
    If surface_covered_in_m2 > 0 applies to a large dataset, the filtering is done repeatedly and inefficiently during query execution.
    No use of pre-filtering or partitions:
    Query directly works on the entire dataset without reducing the scope early
```sql
SELECT 
  property_type,
  state_name,
  COUNT(*) AS property_count
FROM `bigquery-public-data.properati_properties_br.properties_rent_201802`
WHERE surface_covered_in_m2 > 0
GROUP BY property_type, state_name
ORDER BY property_type, property_count DESC;

```

**Optimized Version:**
    Pre-filtering:
    Moves filtering into a separate step, improving performance by focusing only on relevant data for grouping and counting.
    Simplified operations:
    Operates on the smaller pre_filtered_data, which is faster for grouping and sorting
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

![Query 1 Output](images/Q2.png)

### 3. Price Distribution for Different Property Types in Each State
To look at how prices are distributed for different property types (house vs apartment) in each state. This will give insights into price ranges

**Non-Optimized Version:**
    This version does not make use of aliases or efficient filtering, and processes the data without further optimizations like partitioning or clustering
```sql
SELECT 
  state_name, 
  property_type, 
  MIN(price_aprox_usd) AS min_price, 
  MAX(price_aprox_usd) AS max_price, 
  AVG(price_aprox_usd) AS avg_price
FROM `bigquery-public-data.properati_properties_br.properties_rent_201802`
WHERE surface_covered_in_m2 > 0
GROUP BY state_name, property_type
ORDER BY state_name;

```

**Optimized Version:**
Filter Early: In the optimized version, irrelevant rows are filtered using a CTE before applying aggregations, reducing the number of rows to process
By reducing data early and reusing filtered data, the query processes fewer rows, improving speed and efficiency
```sql
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

```
![Query 1 Output](images/Q3.png)
### 4. Cheapest Areas Based on Price per Square Meter

**Non-Optimized Version:**
**Explanation:**
Division in AVG():Its  performing the division inside the aggregation, which may not be as efficient as doing it after filtering.

```sql
SELECT 
  country_name, 
  state_name, 
  AVG(price_aprox_usd / surface_covered_in_m2) AS avg_price_per_m2,
  property_type
FROM `bigquery-public-data.properati_properties_br.properties_rent_201802`
WHERE surface_covered_in_m2 > 0
GROUP BY country_name, state_name, property_type
ORDER BY avg_price_per_m2 ASC
LIMIT 50;

```
**Optimized Version:**
**Explanation:**
Using a WITH clause: This simplifies the calculation of price_per_m2 before performing aggregation, ensuring the computation is done once and not repeatedly during the AVG() operation.
Pre-filtering data: By filtering surface_covered_in_m2 > 0, the number of rows processed during the aggregation is reduced, improving performance.
```sql
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

```
![Query 1 Output](images/Q4.png)

---

## Conclusion

The optimized versions of the SQL queries are designed to execute faster and handle large datasets more efficiently. They avoid complex subqueries and instead leverage separate aggregations for each data source, which allows for better performance and scalability. The non-optimized version processes the data using a subquery, which can be slower due to the need to materialize the intermediate result. The optimized version runs the extraction and aggregation separately for each table, allowing for more efficient parallel processing and better use of database indexing.

