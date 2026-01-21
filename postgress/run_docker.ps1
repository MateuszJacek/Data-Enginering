#!/bin/bash
# Budowanie obrazu

docker run -it --rm ` # run docker container
  -e POSTGRES_USER="root" ` # set postgres user
  -e POSTGRES_PASSWORD="root" ` # set postgres password
  -e POSTGRES_DB="ny_taxi" ` # set default database
  -v "ny_taxi_postgres_data:/var/lib/postgresql/data" ` # persist data
  -p 5432:5432 ` # map port
  postgres:18 # specify image