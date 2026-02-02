### Q1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size?
* **Answer:** `128.3 MiB`
* **Verification:** This was confirmed by checking the `outputFiles` metadata in the Kestra execution outputs for the `extract` task.

### Q2. What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
* **Answer:** `green_tripdata_2020-04.csv`
* **Explanation:** The variable is defined as `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`.

### Q3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
* **Answer:** `24,648,499`
* **Query:** 
```sql
SELECT count(*) 
FROM `trips_data_all.yellow_tripdata` 
WHERE filename LIKE 'yellow_tripdata_2020%';
```

### Q4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?
* **Answer:**  1,734,051
* **Query:** 
```sql 
SELECT count(*) FROM trips_data_all.green_tripdata WHERE filename LIKE 'green_tripdata_2020%';
```

### Q5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
* **Answer:** `1,925,152`
* **Query:** 
```sql
SELECT count(*) 
FROM `trips_data_all.yellow_tripdata` 
WHERE filename = 'yellow_tripdata_2021-03.csv';
```

### Q6. How would you configure the timezone to New York in a Schedule trigger?
* **Answer:**  Add a timezone property set to America/New_York in the Schedule trigger configuration

Justification: Setting the timezone to America/New_York is the most robust method in Kestra. Unlike static offsets (e.g., UTC-5), this identifier references the IANA Time Zone Database, which automatically adjusts for Daylight Saving Time (DST). This prevents schedule drifting and ensures data consistency during seasonal time shifts in New York.