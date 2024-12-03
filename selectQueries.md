

### 1) Counting Projects per City
No Optimization:
```
SELECT proj_city, COUNT(*) AS project_count
FROM `bigquery-public-data.sdoh_hud_housing.2017_lihtc_database_hud`
GROUP BY proj_city
ORDER BY project_count DESC
LIMIT 10;


If data sets are extremely large because it processes all the rows, groups them by cities, and then orders the results. Since sorting is done after grouping it can be slower

Optimzed

WITH project_counts AS (
  SELECT proj_cty, COUNT(*) AS project_count
  FROM `bigquery-public-data.sdoh_hud_housing.2017_lihtc_database_hud`
  GROUP BY proj_cty
)
SELECT proj_cty, project_count
FROM project_counts
ORDER BY project_count DESC
LIMIT 20;

With clause helps readability and also helps with pre filtering rather than having to process the entire table in the final results 

```

![Query 1 Output](images/Q1Optimized.png)
![Query 1.1 Output](images/Query1non.png)

### 1) Counting Projects per City