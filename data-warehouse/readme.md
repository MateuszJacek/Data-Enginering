Create External Table
```sql
CREATE OR REPLACE EXTERNAL TABLE `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://linen-adapter-454718-k1-terra-bucket/yellow_tripdata_2024-*.parquet']
);
```
Create Native Table (Non-partitioned)
```sql
CREATE OR REPLACE TABLE `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned` AS
SELECT * FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_external`;
```

Question 1: What is count of records for the 2024 Yellow Taxi Data?
```sql
SELECT COUNT(*) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_external`;
```
Answer: 20,332,093

Question 2: Estimated amount of data read for distinct PULocationIDs
```sql
SELECT DISTINCT(PULocationID) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_external`;
SELECT DISTINCT(PULocationID) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned`;
```
Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table

Question 3: Understanding columnar storage (Bytes estimation)
```sql
-- Query 1
SELECT PULocationID FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned`;

-- Query 2
SELECT PULocationID, DOLocationID FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned`;
Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
```

Question 4: How many records have a fare_amount of 0?
```sql
SELECT COUNT(*) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;
```
Answer: 8,333

Question 5: Best strategy for optimization (Filter by tpep_dropoff_datetime, Order by VendorID)
```sql
CREATE OR REPLACE TABLE `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_external`;
```
Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

Question 6: VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15
```sql
SELECT DISTINCT(VendorID) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';

SELECT DISTINCT(VendorID) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';
```
Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

Question 7: Where is the data stored in the External Table?
Answer: GCP Bucket

Question 8: Is it best practice to always cluster your data?
Answer: False

Question 9: Bytes read by SELECT count(*) from materialized table
Query:

```sql
SELECT COUNT(*) FROM `linen-adapter-454718-k1.ny_taxi.yellow_tripdata_non_partitioned`;
```
Answer: 0 bytes. BigQuery uses table metadata to calculate count(*) for native tables without scanning the actual data.