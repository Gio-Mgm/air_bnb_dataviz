import pandas as pd
import numpy as np
from functions import reduce_mem_usage

df = pd.read_csv("./data/01_raw/calendar.csv")

df = df[[
    'listing_id', 'date', 'available', 'price'
]]

df["is_weekend"] = pd.DatetimeIndex(df.date).dayofweek
df["is_weekend"] = np.where(df["is_weekend"].isin([4, 5]), 1, 0).astype('uint8')
df["month"] = pd.DatetimeIndex(df.date).month.astype("uint8")
# Format price_USD to int
df["price"] = df["price"].str.strip(
    "$").str.split(",").str.join("").astype("float16") 

df["available"] = np.where(df["available"] == 't', 1, 0)
df["available"] = df["available"].astype('uint8')
df["date"] = pd.to_datetime(df["date"])

df["listing_id"] = df["listing_id"].astype("object")


print("Saving calendar_...")
df.to_csv(
    f"./data/02_intermediate/calendar.csv", index=False)
print("Complete")

size = 1000000
list_of_dfs = [df.loc[i:i+size-1, :] for i in range(0, len(df), size)]

for i in range(len(list_of_dfs)):
    print(f"Saving calendar_{i}...")
    list_of_dfs[i].to_csv(
        f"./data/02_intermediate/calendar_{i}.csv", index=False)
    print("Complete")
