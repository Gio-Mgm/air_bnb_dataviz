import pandas as pd
import numpy as np

from functions import reduce_mem_usage

df = pd.read_csv("./data/01_raw/reviews.csv")
df = df[['listing_id', 'id', 'date', 'reviewer_id']]

df["day"] = pd.DatetimeIndex(df.date).dayofweek
df["month"] = pd.DatetimeIndex(df.date).month

# Reducing memory usage
df, NAlist = reduce_mem_usage(df)
print("_________________")
print("")
print(
    "Warning: the following columns have missing values filled with 'df['column_name'].min() -1': ")
print("_________________")
print("")
print(NAlist)

df.to_csv("./data/02_intermediate/reviews.csv", index=False)

print("Complete")


