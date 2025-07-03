import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="Airline Demand Insights", layout="wide")

# Custom header with emoji
st.markdown(
    """
    <h1 style='text-align: center; color: #4F8BF9;'>✈️ Airline Demand Insights Dashboard</h1>
    <p style='text-align: center; color: #aaa; font-size: 18px;'>
        Analyze live airline market demand, trends, and activity with interactive charts and maps.
    </p>
    """,
    unsafe_allow_html=True,
)

# Sidebar filters with icons
st.sidebar.header("🔎 Filters")

# Fetch options for countries and hours from backend or define statically
@st.cache_data
def get_options():
    try:
        response = requests.get("http://localhost:8000/fetch?all_options=true", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {"countries": [], "hours": list(range(24))}

options = get_options()
selected_country = st.sidebar.selectbox("🌏 Origin Country", ["All"] + options.get("countries", []))
selected_hour = st.sidebar.selectbox("⏰ Hour of Day", ["All"] + [str(h) for h in options.get("hours", [])])

params = {}
if selected_country != "All":
    params["country"] = selected_country
if selected_hour != "All":
    params["hour"] = selected_hour

if st.button("🚀 Fetch Latest Activity Insights"):
    with st.spinner("Fetching data..."):
        try:
            response = requests.get("http://localhost:8000/fetch", params=params, timeout=20)
            if response.status_code == 200:
                data = response.json()

                st.markdown("### 📊 Key Stats")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Flights", data.get('total_flights', 0))
                col2.metric("Unique Aircraft", data.get('unique_aircraft', 0))
                col3.metric("Avg Flights/Hour", f"{data.get('avg_flights_per_hour', 0):.2f}")

                st.info(
                    f"**Peak Hour:** {data.get('peak_hour', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp; **Peak Day:** {data.get('peak_day', 'N/A')}"
                )
                st.markdown("---")

                # Top Countries
                st.subheader("🏆 Top 5 Origin Countries")
                df_countries = pd.DataFrame(data.get("top_countries", []))
                if not df_countries.empty and "country" in df_countries.columns and "count" in df_countries.columns:
                    st.plotly_chart(px.bar(df_countries, x="country", y="count", color="country", title="Top Origin Countries"))
                else:
                    st.warning("No country data available for the selected filter.")

                # Hourly Activity
                st.subheader("⏳ Hourly Activity Distribution")
                df_hourly = pd.DataFrame(data.get("hourly_activity", []))
                if not df_hourly.empty and "hour" in df_hourly.columns and "count" in df_hourly.columns:
                    st.plotly_chart(px.line(df_hourly, x="hour", y="count", markers=True, title="Hourly Activity"))
                else:
                    st.warning("No hourly activity data available.")

                # Top Routes
                st.subheader("🌐 Top 5 Routes (Origin → Destination)")
                df_routes = pd.DataFrame(data.get("top_routes", []))
                if not df_routes.empty:
                    st.dataframe(df_routes, use_container_width=True)
                else:
                    st.info("No route data available.")

                # Top Callsigns
                st.subheader("🛩️ Top 5 Most Active Callsigns")
                df_callsigns = pd.DataFrame(data.get("top_callsigns", []))
                if not df_callsigns.empty and "callsign" in df_callsigns.columns and "count" in df_callsigns.columns:
                    st.dataframe(df_callsigns, use_container_width=True)
                else:
                    st.info("No callsign data available.")

                # Flight Origins Map
                st.subheader("🗺️ Flight Origins Map")
                df_map = pd.DataFrame(data.get("map_data", []))
                if not df_map.empty and "lat" in df_map.columns and "lon" in df_map.columns:
                    st.map(df_map)
                else:
                    st.info("No map data available.")

                # Heatmap
                st.subheader("🔥 Flight Density Heatmap")
                df_heatmap = pd.DataFrame(data.get("heatmap_data", []))
                if not df_heatmap.empty and "lat" in df_heatmap.columns and "lon" in df_heatmap.columns:
                    st.pydeck_chart(pdk.Deck(
                        map_style="mapbox://styles/mapbox/light-v9",
                        initial_view_state=pdk.ViewState(
                            latitude=df_heatmap["lat"].mean(),
                            longitude=df_heatmap["lon"].mean(),
                            zoom=3,
                            pitch=50,
                        ),
                        layers=[
                            pdk.Layer(
                                "HeatmapLayer",
                                data=df_heatmap,
                                get_position='[lon, lat]',
                                radius=10000,
                                elevation_scale=50,
                                elevation_range=[0, 1000],
                                pickable=True,
                                extruded=True,
                            ),
                        ],
                    ))
                else:
                    st.info("No heatmap data available.")

                st.markdown("---")
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown(
    "<hr style='margin-top:2em;margin-bottom:1em'>"
    "<div style='text-align:center;color:#888;font-size:14px;'>"
    "Made with ❤️ by Suryanarayana"
    "</div>",
    unsafe_allow_html=True,
)
