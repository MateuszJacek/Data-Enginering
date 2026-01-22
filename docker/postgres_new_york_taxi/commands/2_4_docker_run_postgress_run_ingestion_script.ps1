# use to run ingestion script in second docker container with network to connect to postgres DB
docker run -it --rm `
   --network="pg-network" `
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

# use to run your ingestion script in docker container after run 2_3 docker_postgress_network_base.ps1
# in the same network and postgres DB running

# all modified ingestion files require rebuild in 2_1 docker build script

# .\commands\2_4_docker_run_postgress_run_ingestion_script.ps1