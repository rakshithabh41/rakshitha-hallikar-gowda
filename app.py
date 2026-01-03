# ============================================================
# IMPORT LIBRARIES
# ============================================================
import streamlit as st
import pandas as pd
import feedparser
import folium
from streamlit_folium import st_folium

# ============================================================
# PAGE CONFIG (MUST BE FIRST)
# ============================================================
st.set_page_config(
    page_title="Maritime Anomaly Detection",
    page_icon="🚢",
    layout="wide"
)

# ============================================================
# TITLE & DESCRIPTION
# ============================================================
st.title("🚢 Anomaly Detection in Maritime Traffic for Coastal Security")
st.markdown("**Satellite-based & AIS-driven Maritime Surveillance Dashboard**")

# ============================================================
# 🌍 SATELLITE MAP – COASTAL REGION
# ============================================================
st.subheader("🛰️ Satellite View – Indian Coastal Region")

m = folium.Map(
    location=[15.0, 73.0],
    zoom_start=5,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="ESRI Satellite"
)

# ============================================================
# 📍 AIS-BASED ANOMALY DATA (SAMPLE – DATA DRIVEN)
# ============================================================
anomaly_data = pd.DataFrame({
    "Vessel_ID": ["V-101", "V-203", "V-411"],
    "Latitude": [14.8, 16.2, 12.9],
    "Longitude": [72.5, 74.1, 75.4],
    "Issue": ["Speed Anomaly", "AIS Spoofing", "Route Deviation"]
})

# Add markers to map
for _, row in anomaly_data.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"""
        <b>Vessel ID:</b> {row['Vessel_ID']}<br>
        <b>Anomaly:</b> {row['Issue']}
        """,
        icon=folium.Icon(color="red", icon="warning-sign")
    ).add_to(m)

st_folium(m, width=1200, height=500)

# ============================================================
# 📊 ANOMALY TABLE
# ============================================================
st.subheader("📊 Detected Maritime Anomalies (AIS Data)")
st.dataframe(anomaly_data, use_container_width=True)

# ============================================================
# 📰 TOP 10 LATEST NEWS (WITH IMAGES & LINKS)
# ============================================================
st.subheader("📰 Top 10 Latest News – Maritime Anomaly & Coastal Security")

rss_url = (
    "https://news.google.com/rss/search?"
    "q=maritime+anomaly+detection+coastal+security+AIS+satellite"
    "&hl=en-IN&gl=IN&ceid=IN:en"
)

feed = feedparser.parse(rss_url)

if feed.entries:
    for i, entry in enumerate(feed.entries[:10], start=1):

        col1, col2 = st.columns([1, 3])

        # -------- IMAGE --------
        with col1:
            image_url = None
            if "media_thumbnail" in entry:
                image_url = entry.media_thumbnail[0]["url"]
            elif "media_content" in entry:
                image_url = entry.media_content[0]["url"]

            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ship_icon.svg/512px-Ship_icon.svg.png",
                    use_container_width=True
                )

        # -------- TEXT --------
        with col2:
            st.markdown(f"### {i}. {entry.title}")
            st.markdown(f"[🔗 Read full article]({entry.link})")

        st.markdown("---")
else:
    st.error("Unable to fetch news at the moment.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
---
**Project:** Anomaly Detection in Maritime Traffic for Coastal Security  
**Domain:** Coastal Surveillance & Maritime Security  
**Technologies:** AIS | Satellite Imagery | GIS | Python | Streamlit  
""")
