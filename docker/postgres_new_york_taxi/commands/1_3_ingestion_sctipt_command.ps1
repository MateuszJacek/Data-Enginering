# before running that script make sure that your DB is running
uv run python ingest_data.py `
   --pg-user="root" `
   --pg-pass="root" `
   --pg-host="localhost" `
   --pg-port=5432 `
   --pg-db="ny_taxi" `
   --year=2021 `
   --month=1 `
   --chunksize=100000 `
   --target-table="yellow_taxi_data"

# use for testing before add ingestion script to Dockerfile
#.\commands\1_3_ingestion_sctipt_command.ps1