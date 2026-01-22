# run after runing docker compose to have the network and runing ingestion script container
docker run -it --rm `
   --network="postgres_new_york_taxi_default" `
    taxi_ingest:v001 `
   --pg-user="root" `
   --pg-pass="root" `
   --pg-host="pgdatabase" `
   --pg-port=5432 `
   --pg-db="ny_taxi" `
   --year=2021 `
   --month=1 `
   --chunksize=10000 `
   --target-table="yellow_taxi_data"

# .\commands\3_2_run_ingestion_container.ps1