## Question 1. Understanding Docker images

Run the following command in the directory `docker/hwork/`:

```bash
docker run -it --entrypoint=bash python:3.13
```

After entering the container, check the version of pip:

```bash
root@39b29b3f5e06:/# pip -V
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

## Question 2. Understanding Docker Networking

### Accessing pgAdmin
To manage the database, open pgAdmin via the forwarded port:
* **Dev Tunnel:** [https://7trmlr76-8080.euw.devtunnels.ms/](https://7trmlr76-8080.euw.devtunnels.ms/)
* **Localhost:** [http://127.0.0.1:8080](http://127.0.0.1:8080)

Log in using the credentials defined in your `docker-compose.yaml` or script environment variables.

### Connecting to the Database
When registering a new server in pgAdmin, use the following settings:
* **Username/Password:** `postgres` / `postgres` (as defined in the image/env)
* **Port:** `5432`

#### Connection Test Results:
* **Hostname: `postgres`** – **SUCCESS**

Initially, the hostname **`postgres`** (based on the `container_name`) seemed like the most obvious choice. However, I decided to test the service name as well. To my surprise, the hostname **`db`** also worked perfectly.

* **Hostname: `db`** – **SUCCESS**

---

### Analysis: Why do both `postgres` and `db` work?

In Docker Compose, there are two ways a container can be identified within a network:

1. **Service Name:** Defined as `db:` in your YAML. Docker's internal DNS maps this name to the container's IP.
2. **Container Name:** Defined as `container_name: postgres`. This acts as an explicit alias.

Since pgAdmin and the database are in the same Docker network, pgAdmin can resolve both names to the same IP address. It is standard behavior for Docker Compose to allow resolution via the service name by default.

**Correct Answer for pgAdmin Connection:**
The hostname is **`db`** (service name) or **`postgres`** (container name), and the port is **`5432`** (internal container port).





Rozumiem, potrzebujesz surowego kodu Markdown, który po wklejeniu do edytora (np. VS Code czy GitHub) od razu zamieni się w ładnie sformatowany dokument z nagłówkami, listami i blokami kodu.

Oto gotowy kod do skopiowania:

Markdown
## Data Preparation & ETL Workflow

To prepare for the upcoming tasks, I developed a containerized ETL pipeline to ingest the required datasets into the PostgreSQL volume in two stages.

---

### 1. Environment & Project Setup
I initialized the workspace in the `hmwork` folder using **uv** for high-performance dependency management:

* **Initialization:** Created the project with `uv init --python 3.13`.
* **Configuration:** Copied the existing `pyproject.toml` from the `postgres_new_york_taxi` folder to reuse the base configuration.
* **Dependency Update:** Added missing libraries required for Parquet and database communication:
    ```bash
    uv add requests pyarrow fastparquet sqlalchemy psycopg2-binary
    ```
* **Synchronization:** Executed `uv sync` to lock the environment.

### 2. Universal Ingestion Script (`ingest_data.py`)
I modified the ingestion script (`hmwork/ingest_data.py`) to be more flexible. Instead of hardcoded paths, it now accepts a **direct source URL**. The script performs the following:
* Downloads the data from the source.
* Handles decompression and Parquet/CSV parsing.
* Streams the data into the database in chunks to optimize memory usage.

### 3. Dockerization
Prepared a `Dockerfile` (`hmwork/Docker`) to package the ingestion environment. The image is built using a dedicated PowerShell script to ensure consistency.

### 4. Automation via PowerShell Scripts (.ps1)
To manage the workflow efficiently, I created several `.ps1` scripts:

#### A. Build Process
`docker_build_green_taxi.ps1` – Stores the command to build the container:
```powershell
docker build -t green_taxi_ingest:v001 .
# Execution: .\docker_build_green_taxi.ps1
```

#### B. Data Loading (Two Stages)
I created two separate scripts to trigger the ingestion for each dataset, allowing for a clean, two-stage loading process:

* **Stage 1: Green Taxi Data**
    Executed `.\ingestion_script_green_taxi.ps1` to handle the November 2025 Parquet dataset.
* **Stage 2: Zone Lookups**
    Executed `.\ingestion_script_taxi_zone_lookup.ps1` to load the taxi zone reference table from the CSV source.

```powershell
docker run -it --rm `
   --network="hwork_default" `
    green_taxi_ingest:v001 `
   --pg-user="postgres" `
   --pg-pass="postgres" `
   --pg-host="db" `
   --pg-port=5432 `
   --pg-db="ny_taxi" `
   --url='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet' `
   --chunksize=10000 `
   --target-table="green_taxi_data"
```


### 5. Verification & Readiness
The process is complete once both tables are successfully verified within the PostgreSQL database via pgAdmin. 

With both **green_taxi_data** and **taxi_zone_lookup** tables fully populated, the environment is ready for the subsequent SQL analysis and the realization of Questions 3–6.


### SQL Analysis - Homework Solutions

Before starting the analysis, I verified the measurement units for the dataset. According to the [official NYC TLC documentation](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf), the `trip_distance` is recorded in **miles**.

---

### Question 3. Counting short trips
**Task:** For trips in November 2025 (exclusive of the upper bound), how many trips had a `trip_distance` ≤ 1 mile?

```sql
SELECT 
    COUNT(*)
FROM public.green_taxi_data 
WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```


Answer: 8007



### Question 4. Longest trip for each day
**Task:** Which was the pick-up day with the longest trip distance (considering only trips < 100 miles)?

```sql
SELECT 
    DATE(lpep_pickup_datetime) AS lpep_pickup_date
FROM public.green_taxi_data 
WHERE trip_distance IN (
    SELECT 
        MAX(trip_distance)
    FROM public.green_taxi_data 
    WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01'
      AND trip_distance < 100
);
```

Answer: 2025-11-14

### Question 5. Biggest pickup zone
**Task:** Which pickup zone had the largest total_amount (sum of all trips) on November 18th, 2025?

```sql
SELECT 
    DATE(gt.lpep_pickup_datetime) AS lpep_pickup_date,
    tz."Zone",
    SUM(gt.total_amount) AS total_amount
FROM public.green_taxi_data AS gt 
LEFT JOIN public.taxi_zone AS tz ON gt."PULocationID" = tz."LocationID"
WHERE CAST(lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY 1, 2
ORDER BY 3 DESC 
LIMIT 1;
```

Answer: East Harlem North


### Question 6. Largest tip
**Task:**  For passengers picked up in "East Harlem North" in November 2025, which drop-off zone had the largest tip?

```sql
WITH max_tip_amount AS (
    SELECT 
        "DOLocationID",
        tip_amount
    FROM public.green_taxi_data AS gt 
    LEFT JOIN public.taxi_zone AS tz ON gt."PULocationID" = tz."LocationID"
    WHERE CAST(lpep_pickup_datetime AS DATE) < '2025-12-01'
      AND tz."Zone" = 'East Harlem North'
    ORDER BY tip_amount DESC 
    LIMIT 1
)
SELECT mta.*, tz."Zone"
FROM max_tip_amount AS mta
LEFT JOIN public.taxi_zone AS tz ON mta."DOLocationID" = tz."LocationID";
```

Answer: Yorkville West