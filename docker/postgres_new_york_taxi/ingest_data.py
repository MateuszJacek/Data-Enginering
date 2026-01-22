#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


pd.__file__ # to ensure from what environment get pandas dependencies


# In[4]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'


# In[5]:


df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)


# In[6]:


# Display first rows
df.head()


# In[7]:


# Check data types
df.dtypes


# In[8]:


# Check data shape
df.shape


# In[12]:


# Firstly we choose dtypes before we get data in next steps
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[13]:


df.head() #like we see for example vendorID change type


# In[14]:


get_ipython().system('uv add sqlalchemy')


# In[17]:


get_ipython().system('uv add psycopg2-binary')


# In[18]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[20]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine)) # get schema which we can use to create table dataset


# In[21]:


# and for execution that schema:
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[22]:


# addind data segment


# In[25]:


df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[26]:


get_ipython().system('uv add tqdm')


# In[28]:


from tqdm.auto import tqdm

first = True

for df_chunk in tqdm(df_iter):

    if first:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))

