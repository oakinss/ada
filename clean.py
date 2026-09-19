import pandas as pd
import polars as pl

# Read ASCII
df_pd = pd.read_sas("LLCP2025.XPT")

# Convert to Polars
df = pl.from_pandas(df_pd)

# Inspect the Polars DataFrame
print(df.shape)

# Select specific columns
df = df.select(
    "DIABETE4",
    "_AGE80", 
    "_BMI5",
    "_SEX", 
    "_RFHYPE6", 
    "_TOTINDA",
).rename({
    "DIABETE4": "diabetes",
    "_AGE80": "age",
    "_BMI5": "bmi",
    "_SEX": "sex",
    "_RFHYPE6": "hypertension",
    "_TOTINDA": "activity",})

# Recode
df = df.with_columns(
    pl.col("diabetes").replace({2:0, 3:0, 4:0, 7:None, 9:None}), 
    (pl.col("bmi").replace({777:None, 999:None}) / 100).alias("bmi"), 
    pl.col("sex").replace({1:0, 2:1}), 
    pl.col("hypertension").replace({1:0, 2:1, 9:None}), 
    pl.col("activity").replace({2:0, 9:None}), 
)

# Drop rows with missing diabetes information 
df = df.drop_nulls("diabetes")
df.write_parquet("cleaned_data.parquet")
