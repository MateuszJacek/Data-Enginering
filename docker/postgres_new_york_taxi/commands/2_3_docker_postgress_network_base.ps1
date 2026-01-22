# create base for postgres and uv containers for run ingestion script
docker run -it --rm `
  -e POSTGRES_USER="root" `
  -e POSTGRES_PASSWORD="root" `
  -e POSTGRES_DB="ny_taxi" `
  -v "ny_taxi_postgres_data:/var/lib/postgresql" `
  -p 5432:5432 `
  --network="pg-network" `
  --name pgdatabase `
  postgres:18

# use to run your data base with network before run 2_4 ingestion script in docker container
# .\commands\2_3_docker_postgress_network_base.ps1