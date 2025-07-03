def generate_insights(df):
    df["origin_country"] = df["origin_country"].str.strip()

    top_countries = (
        df["origin_country"]
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={"origin_country": "count", "index": "country"})
        .to_dict(orient="records")
    )

    hourly_activity = (
        df.groupby("hour")
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
    )

    top_callsigns = (
        df["callsign"]
        .value_counts()
        .head(5)
        .reset_index()
        .rename(columns={"callsign": "count", "index": "callsign"})
        .to_dict(orient="records")
    )

    df["route"] = df["origin_country"] + " → [" + df["latitude"].astype(str) + ", " + df["longitude"].astype(str) + "]"
    top_routes = (
        df["route"]
        .value_counts()
        .head(5)
        .reset_index()
        .rename(columns={"route": "count", "index": "route"})
        .to_dict(orient="records")
    )

    map_data = []
    if "latitude" in df.columns and "longitude" in df.columns:
        map_data = df[["latitude", "longitude"]].dropna().rename(
            columns={"latitude": "lat", "longitude": "lon"}
        ).to_dict(orient="records")

    peak_hour = int(df["hour"].mode()[0]) if not df["hour"].empty else None

    peak_day = (
        int(df["last_seen"].dt.day.mode()[0])
        if "last_seen" in df.columns and not df["last_seen"].empty
        else None
    )

    unique_aircraft = df["icao24"].nunique() if "icao24" in df.columns else 0
    avg_flights_per_hour = float(df.groupby("hour").size().mean()) if not df.empty else 0
    total_flights = int(len(df))

    return {
        "top_countries": top_countries,
        "hourly_activity": hourly_activity,
        "top_routes": top_routes,
        "map_data": map_data,
        "peak_hour": peak_hour,
        "peak_day": peak_day,
        "top_callsigns": top_callsigns,
        "unique_aircraft": unique_aircraft,
        "avg_flights_per_hour": avg_flights_per_hour,
        "total_flights": total_flights,
        "heatmap_data": map_data,
    }