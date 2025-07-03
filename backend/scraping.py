import pandas as pd
import requests

def get_airline_data():
    """
    Fetches flight data from OpenSky Network (free access, no key required).
    Returns a DataFrame with limited fields (as OpenSky is focused on live flights).
    """
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    states = data.get("states", [])

    records = []
    for s in states:
        records.append({
            "icao24": s[0],
            "callsign": s[1].strip() if s[1] else "N/A",
            "origin_country": s[2],
            "time_position": s[3],
            "last_contact": s[4],
            "longitude": s[5],
            "latitude": s[6],
            "on_ground": s[8],
        })

    df = pd.DataFrame(records)
    df = df.dropna(subset=["longitude", "latitude"])
    df["last_seen"] = pd.to_datetime(df["last_contact"], unit="s")
    df["location"] = df["latitude"].astype(str) + ", " + df["longitude"].astype(str)
    return df