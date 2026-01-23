import os
import requests
import pandas as pd
import numpy as np
import click
from sqlalchemy import create_engine
from tqdm.auto import tqdm

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--url', required=True, help='URL of the file (CSV or Parquet)')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-table', default='taxi_data', help='Name of the target table')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, url, chunksize, target_table):
    
    # 1. Dynamiczne ustalenie nazwy pliku
    file_name = "data_to_ingest.parquet" if ".parquet" in url else "data_to_ingest.csv"
    
    # 2. Pobieranie pliku (Stream)
    print(f"Downloading {url}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    # 3. Połączenie z bazą danych
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    print('Connection to PostgreSQL established.')

   # 4. Przygotowanie iteratora w zależności od formatu
    if file_name.endswith('.parquet'):
        print("Reading Parquet file...")
        df = pd.read_parquet(file_name)
        
        # POPRAWKA: Zamiast array_split, używamy podziału na DataFrame'y
        df_iter = [df[i : i + chunksize] for i in range(0, len(df), chunksize)]
    else:
        print("Reading CSV file...")
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=chunksize, low_memory=False)

    # 5. Proces Ingestu (teraz zadziała uniwersalnie)
    first_chunk = True
    for df_chunk in tqdm(df_iter):
        # Teraz df_chunk na pewno jest DataFrame, więc .columns zadziała
        date_columns = [c for c in df_chunk.columns if 'datetime' in c.lower() or 'pep_p' in c.lower() or 'pep_d' in c.lower()]

        if first_chunk:
            # Tworzymy tabelę (if_exists="replace" usuwa starą o tej samej nazwie)
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists="replace")
            first_chunk = False
            print(f"Table '{target_table}' created successfully.")

        # Wrzucanie danych
        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")

    # Opcjonalne sprzątanie pliku po zakończeniu
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"Temporary file {file_name} removed.")

    print("Ingestion finished!")

if __name__ == '__main__':
    run()