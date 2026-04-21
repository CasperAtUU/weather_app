"""
Houten Weather Widget — Streamlit Version
==========================================
Live weather for Houten, NL. Deploy to Streamlit Cloud.

Deploy:
    1. Push this file + requirements.txt to GitHub
    2. Go to https://share.streamlit.io
    3. Connect your repo → done
"""

import streamlit as st
import urllib.request
import json
from datetime import datetime
import pytz
import time

# ── Config ──────────────────────────────────────────────────────────────────
LATITUDE = 52.0294
LONGITUDE = 5.1692
API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current=temperature_2m,apparent_temperature,weathercode,windspeed_10m"
    "&hourly=precipitation,precipitation_probability"
    "&daily=sunrise,sunset"
    "&wind_speed_unit=ms"
    "&timezone=Europe%2FAmsterdam"
)

# WMO weather-code → (label, emoji)
WMO_CODES = {
    0:  ("Clear sky",        "☀️"),
    1:  ("Mainly clear",     "🌤️"),
    2:  ("Partly cloudy",    "⛅"),
    3:  ("Overcast",         "☁️"),
    45: ("Foggy",            "🌫️"),
    48: ("Icy fog",          "🌫️"),
    51: ("Light drizzle",    "🌦️"),
    53: ("Drizzle",          "🌦️"),
    55: ("Heavy drizzle",    "🌧️"),
    61: ("Slight rain",      "🌧️"),
    63: ("Rain",             "🌧️"),
    65: ("Heavy rain",       "🌧️"),
    71: ("Slight snow",      "🌨️"),
    73: ("Snow",             "❄️"),
    75: ("Heavy snow",       "❄️"),
    77: ("Snow grains",      "🌨️"),
    80: ("Rain showers",     "🌦️"),
    81: ("Rain showers",     "🌧️"),
    82: ("Violent showers",  "⛈️"),
    85: ("Snow showers",     "🌨️"),
    86: ("Heavy snow shwrs", "❄️"),
    95: ("Thunderstorm",     "⛈️"),
    96: ("Thunderstorm+hail","⛈️"),
    99: ("Thunderstorm+hail","⛈️"),
}


def fetch_weather():
    """Fetch weather from Open-Meteo."""
    try:
        req = urllib.request.Request(
            API_URL, headers={"User-Agent": "HoutenWeatherApp/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        cur = data["current"]
        code = int(cur["weathercode"])
        label, emoji = WMO_CODES.get(code, ("Unknown", "🌡️"))
        
        # Extract sunrise/sunset (today's first entry)
        daily = data["daily"]
        sunrise = daily["sunrise"][0].split("T")[1][:5]  # HH:MM
        sunset = daily["sunset"][0].split("T")[1][:5]    # HH:MM
        
        # Extract next 6 hours of hourly precipitation
        hourly = data["hourly"]
        now_idx = 0  # Current hour
        hourly_data = []
        for i in range(6):  # Next 6 hours
            if now_idx + i < len(hourly["precipitation"]):
                hourly_data.append({
                    "precip_mm": hourly["precipitation"][now_idx + i],
                    "prob": hourly["precipitation_probability"][now_idx + i],
                })
        
        return {
            "temp": round(cur["temperature_2m"]),
            "feels_like": round(cur["apparent_temperature"]),
            "wind_ms": round(cur["windspeed_10m"], 1),
            "condition": label,
            "emoji": emoji,
            "updated": datetime.now(pytz.timezone("Europe/Amsterdam")).strftime("%H:%M"),
            "sunrise": sunrise,
            "sunset": sunset,
            "hourly": hourly_data,
        }
    except Exception as e:
        return None


# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Houten Weather",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Auto-refresh every 10 minutes ────────────────────────────────────────────
st.markdown("""
    <script>
        setTimeout(function() {
            location.reload();
        }, 600000);  // 600000 ms = 10 minutes
    </script>
""", unsafe_allow_html=True)

# ── Custom CSS for dark theme ───────────────────────────────────────────────
st.markdown("""
    <style>
    :root {
        --bg-primary: #0f1923;
        --bg-secondary: #162230;
        --text-primary: #e8f4fd;
        --text-secondary: #7bafc8;
        --accent: #4fc3f7;
    }
    
    body {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stMetric {
        background-color: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid var(--accent);
    }
    
    .stMetric label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric [data-testid="metricValue"] {
        color: var(--text-primary) !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }
    
    h1, h2, h3 {
        color: var(--text-primary) !important;
    }
    
    .stButton > button {
        background-color: var(--accent);
        color: var(--bg-primary);
        border: none;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #7dd3fc;
    }
    </style>
""", unsafe_allow_html=True)

# ── Title ────────────────────────────────────────────────────────────────────
st.title("🌤️ Houten Weather")
st.markdown("**Real-time weather for Houten, Netherlands**")
st.markdown("---")

# ── Fetch and display ────────────────────────────────────────────────────────
data = fetch_weather()

if data:
    # Layout: two columns for temp + condition
    col1, col2 = st.columns([1.5, 1.5])
    
    with col1:
        st.metric(
            label="Temperature",
            value=f"{data['temp']}°C",
            delta=f"Feels like {data['feels_like']}°C"
        )
    
    with col2:
        st.metric(
            label="Condition",
            value=data['emoji'],
            delta=data['condition']
        )
    
    # Divider
    st.markdown("---")
    
    # Additional info
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric(label="Wind", value=f"{data['wind_ms']} m/s")
    
    with col4:
        st.metric(label="Updated", value=data['updated'])
    
    with col5:
        st.metric(label="Location", value="Houten, NL")
    
    # ── Sun times ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("**☀️ Sun Times (Amsterdam)**")
    
    sun_col1, sun_col2 = st.columns(2)
    with sun_col1:
        st.metric(label="Sunrise", value=data['sunrise'])
    with sun_col2:
        st.metric(label="Sunset", value=data['sunset'])
    
    # ── Rain forecast (next 6 hours) ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("**🌧️ Rain Forecast (Next 6 Hours)**")
    
    rain_data = []
    ams_tz = pytz.timezone("Europe/Amsterdam")
    now_ams = datetime.now(ams_tz)
    for i, h in enumerate(data['hourly']):
        hour = (now_ams.hour + i) % 24
        rain_data.append({
            "Hour": f"{hour:02d}:00",
            "Precipitation (mm)": h['precip_mm'],
            "Probability (%)": h['prob'],
        })
    
    if rain_data:
        import pandas as pd
        df = pd.DataFrame(rain_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Info
    st.markdown(f"""
    <div style="text-align: center; color: var(--text-secondary); font-size: 0.85rem; margin-top: 2rem;">
    ✓ Data refreshes every 10 minutes<br>
    🔄 Manual refresh: Button below
    </div>
    """, unsafe_allow_html=True)
    
    # Refresh button
    if st.button("🔄 Refresh Now", key="refresh_btn"):
        st.rerun()

else:
    st.error("❌ Could not fetch weather data. Check your connection.")
    if st.button("Retry"):
        st.rerun()
