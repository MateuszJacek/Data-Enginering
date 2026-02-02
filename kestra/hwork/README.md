## Methodology

To solve this assignment, I utilized the **09_gcp_taxi_scheduled** flow. This flow was used to automate the ingestion of NYC Taxi data (Yellow and Green) into Google Cloud Storage and subsequently into BigQuery.

For data processing, I leveraged Kestra's **Backfill** functionality, which allowed me to systematically load the required time periods for both years (2020 and 2021).

---

## Quiz Answers

### Q1. Uncompressed File Size (Yellow 2020-12)
* **Answer:** `128.3 MiB`
* **My Method:** I verified the size of the uncompressed CSV file directly in the **Google Cloud Storage Bucket** after the `extract` and `upload` tasks. I then performed a conversion from Megabytes (MB) to Mebibytes (MiB) to match the required format.

### Q2. Rendered Variable Value
* **Answer:** `green_tripdata_2020-04.csv`
* **My Method:** I analyzed the `variables` section of my YAML code to see how the string is generated. By combining the `taxi` input with the `trigger.date` formatted as `yyyy-MM`, the resulting string for Green Taxi in April 2020 is exactly `green_tripdata_2020-04.csv`.

### Q3. Yellow Taxi Rows (Year 2020)
* **Answer:** `24,648,499`
* **My Method:** I first ran a dedicated backfill for the entire year 2020. Once the ingestion was complete, I navigated to the **BigQuery Console**, selected the table `linen-adapter-454718-k1.trips_data_all.yellow_tripdata`, and retrieved the total row count from the **Details** tab.

### Q4. Green Taxi Rows (Year 2020)
* **Answer:** `1,734,051`
* **My Method:** Similar to the Yellow taxi data, I processed the year 2020 for Green taxis and verified the final count in the **Details** tab of the `linen-adapter-454718-k1.trips_data_all.green_tripdata` table in BigQuery.

### Q5. Yellow Taxi Rows (March 2021)
* **Answer:** `1,925,152`
* **My Method:** I specifically checked the temporary table `linen-adapter-454718-k1.trips_data_all.yellow_tripdata_2021_03` created during the March 2021 execution. The row count was obtained directly from the **Details** section of that specific table.

### Q6. Timezone Configuration for Schedule Trigger
* **Answer:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`
* **Justification:** In Kestra, the `Schedule` trigger is designed to work with the IANA Time Zone Database. Setting the timezone to `America/New_York` is crucial for data pipelines centered in New York, as it automatically accounts for Daylight Saving Time (DST). This ensures that the flow triggers at the correct local hour year-round, preventing potential data synchronization issues caused by the one-hour shifts in March and November.

---

## Infrastructure
* **Orchestrator:** Kestra
* **Data Lake:** Google Cloud Storage (GCS)
* **Data Warehouse:** Google BigQuery