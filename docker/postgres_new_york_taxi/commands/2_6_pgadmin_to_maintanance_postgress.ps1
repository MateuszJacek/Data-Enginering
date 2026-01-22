# In another terminal, run pgAdmin on the same network
docker run -it `
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" `
  -e PGADMIN_DEFAULT_PASSWORD="root" `
  -v pgadmin_data:/var/lib/pgadmin `
  -p 8085:80 `
  --network=pg-network `
  --name pgadmin `
  dpage/pgadmin4

# use in third terminal to run pgAdmin connected to the postgres DB
# after run 2_3 docker_postgress_network_base.ps1 and have postgres DB running
# .\commands\2_6_pgadmin_to_maintanance_postgress.ps1
# https://7trmlr76-8085.euw.devtunnels.ms/login?next=/ trzeba dodać w port:8085
# lub http://127.0.0.1:8085