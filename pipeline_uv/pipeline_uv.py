import sys
import pandas as pd

day = int(sys.argv[1])
print(f"Running pipeline_UV for day {day}")

print(pd.__version__)

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df.to_parquet(f"output_day_{sys.argv[1]}_uv.parquet")