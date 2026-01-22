# for testing and creating ingestion script before add it to Dockerfile
docker run -it --rm `
  -e POSTGRES_USER="root" `
  -e POSTGRES_PASSWORD="root" `
  -e POSTGRES_DB="ny_taxi" `
  -v "ny_taxi_postgres_data:/var/lib/postgresql" `
  -p 5432:5432 `
  postgres:18

# use that script firstly to run your data base before uv_run_ingestion_sctipt_command.ps1
# .\commands\1_1_docker_postgress_base.ps1