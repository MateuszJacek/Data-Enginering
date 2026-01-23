docker run -it --rm `
   --network="hwork_default" `
    green_taxi_ingest:v001 `
   --pg-user="postgres" `
   --pg-pass="postgres" `
   --pg-host="db" `
   --pg-port=5432 `
   --pg-db="ny_taxi" `
   --url='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv' `
   --chunksize=10000 `
   --target-table="taxi_zone"

   # .\ingestion_script_taxi_zone_lookup.ps1