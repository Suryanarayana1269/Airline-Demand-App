import pandas as pd

def process_data(df):
    df = df.copy()
    df = df.dropna(subset=["origin_country", "last_seen"])
    df["hour"] = df["last_seen"].dt.hour
    return df