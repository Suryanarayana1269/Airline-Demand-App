from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.scraping import get_airline_data
from backend.processor import process_data
from backend.insights import generate_insights
import pandas as pd
from functools import lru_cache
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache data for 5 minutes
@lru_cache(maxsize=1)
def cached_data():
    df = get_airline_data()
    df = process_data(df)
    timestamp = time.time()
    return df, timestamp

@app.get("/fetch")
async def fetch_insights(
    country: str = Query(None),
    hour: str = Query(None),
    all_options: bool = Query(False)
):
    df, cached_time = cached_data()

    # Provide filter options if requested
    if all_options:
        countries = sorted(df["origin_country"].dropna().unique().tolist())
        hours = sorted(df["hour"].dropna().unique().tolist())
        return {"countries": countries, "hours": hours}

    # Apply filters
    if country:
        df = df[df["origin_country"] == country]
    if hour:
        df = df[df["hour"] == int(hour)]

    insights = generate_insights(df)
    return insights