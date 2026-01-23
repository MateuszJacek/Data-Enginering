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

   # .\ingestion_script_green_taxi.ps1