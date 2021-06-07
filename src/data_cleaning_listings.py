import numpy as np
import pandas as pd

from functions import reduce_mem_usage

df = pd.read_csv("./data/01_raw/listings.csv")

# Columns selection
df = df[[
    'id',
    'host_id',
    'host_response_time',
    'host_response_rate',
    'host_is_superhost',
    'host_identity_verified',
    'latitude',
    'longitude',
    'property_type',
    'room_type',
    'bathrooms_text',
    'bedrooms',
    'beds',
    'price',
    'minimum_nights',
    'number_of_reviews',
    'review_scores_rating',
    'instant_bookable'
]]

# Column renaming
rename = {
    "bathrooms_text": "bathrooms",
    "price": "price_USD"
}
df.rename(columns=rename, inplace=True)

# Format price_USD to float
df["price_USD"] = df["price_USD"].str.strip("$").str.split(",").str.join("").astype("float64")

# Extract number of bathrooms
df["bathrooms"] = df["bathrooms"].str.split(" ", n=1, expand=True)[0]
df["bathrooms"] = np.where(
    df["bathrooms"].isin(["Private", "Shared"]), "1", df["bathrooms"]
)
df["bathrooms"] = np.where(
    df["bathrooms"] == "Half-bath", "0.5", df["bathrooms"]
)
df["bathrooms"] = df["bathrooms"].astype("float64")

# -----------------------------#
# Formating some columns values
# -----------------------------#

def rndlim(x, lim=4):
    if pd.notna(x):
        x = round(x)
    if x >= lim:
        return f"{lim} or more"
    else:
        return x

df["bathrooms"] = df["bathrooms"].apply(rndlim)
df["bedrooms"] = df["bedrooms"].apply(rndlim)
df["beds"] = df["beds"].apply(rndlim, lim=6)

def min_nights(x):
    if x < 7:
        return x

    minis = [90, 60, 28, 14, 7]
    for mini in minis:
        if x >= mini:
            return f"{mini}+"

df["minimum_nights"] = df["minimum_nights"].apply(min_nights)

# Extract property_type
df["property_type"] = df["property_type"].str.split().str[-1]

# Group property types in "Others"
s = df["property_type"].value_counts()
df.loc[df["property_type"].isin(s[(s < 50)].index), "property_type"] = "other"

df["property_type"] = np.where(
    df["property_type"] == "hostel", "hotel", df["property_type"]
)

df["property_type"] = np.where(
    df["property_type"] == "breakfast", "bed and breakfast", df["property_type"]
)

df["host_response_rate"] = df["host_response_rate"].str.strip("%").astype("float64")

to_bool_cols = [
    "host_is_superhost",
    "host_identity_verified",
    "instant_bookable"
]

# Convert in boolean
for col in to_bool_cols:
    df[col] = np.where(df[col] == 't', True, False)
    df[col] = df[col].astype('bool')

strs =[
    'host_response_time','host_response_rate', 'bathrooms', 'bedrooms', 'beds', 'review_scores_rating'
]
for col in strs:
    df[col] = df[col].fillna('Na')

# Reducing memory usage
df, NAlist = reduce_mem_usage(df)
print("_________________")
print("")
print(
    "Warning: the following columns have missing values filled with 'df['column_name'].min() -1': ")
print("_________________")
print("")
print(NAlist)

print("Saving...")
df.to_csv("./data/02_intermediate/listings.csv", index=False)
print("Complete !")
