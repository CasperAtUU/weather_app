"""
Houten Weather Dashboard — Refined Edition
===========================================
A modern, visually refined weather dashboard with glassmorphism design.

Run:
    pip install streamlit
    streamlit run dashboard.py
"""

import streamlit as st
import urllib.request
import json
from datetime import datetime
import pytz

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Houten Weather",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS: Glassmorphism + Dark Theme ───────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 50%, #0f1428 100%);
        background-attachment: fixed;
    }

    /* Remove default Streamlit styling */
    [data-testid="stAppViewContainer"] {
        padding: 0;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 2rem 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Typography */
    h1, h2, h3 {
        color: #e8f4fd;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    p {
        color: #a8c5d9;
    }

    /* Glassmorphism card styling */
    .glass-card {
        background: rgba(22, 34, 48, 0.45);
        backdrop-filter: blur(12px) saturate(180%);
        border: 1px solid rgba(79, 195, 247, 0.12);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 1px rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(79, 195, 247, 0.05) 0%, transparent 100%);
        pointer-events: none;
        border-radius: 20px;
    }

    .glass-card:hover {
        background: rgba(22, 34, 48, 0.55);
        border-color: rgba(79, 195, 247, 0.25);
        box-shadow: 
            0 16px 48px rgba(79, 195, 247, 0.1),
            inset 0 1px 1px rgba(255, 255, 255, 0.08);
        transform: translateY(-4px);
    }

    /* Main temperature card */
    .temp-card {
        background: linear-gradient(135deg, rgba(79, 195, 247, 0.1) 0%, rgba(22, 34, 48, 0.5) 100%);
        backdrop-filter: blur(16px) saturate(200%);
        border: 1px solid rgba(79, 195, 247, 0.18);
        box-shadow: 
            0 8px 32px rgba(79, 195, 247, 0.08),
            inset 0 1px 2px rgba(255, 255, 255, 0.08);
    }

    .temp-card:hover {
        border-color: rgba(79, 195, 247, 0.35);
        box-shadow: 
            0 16px 48px rgba(79, 195, 247, 0.15),
            inset 0 1px 2px rgba(255, 255, 255, 0.1);
    }

    /* Metric label & value styling */
    .metric-label {
        color: #7bafc8;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        display: block;
        margin-bottom: 8px;
        opacity: 0.9;
    }

    .metric-value {
        color: #e8f4fd;
        font-size: 36px;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -1px;
    }

    .metric-value.large {
        font-size: 64px;
        background: linear-gradient(135deg, #4fc3f7 0%, #7dd3fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-secondary {
        color: #a8c5d9;
        font-size: 13px;
        margin-top: 6px;
        font-weight: 400;
    }

    .metric-icon {
        font-size: 48px;
        margin-bottom: 12px;
        display: inline-block;
    }

    /* Section divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(79, 195, 247, 0.2), transparent);
        margin: 32px 0;
    }

    .section-title {
        color: #e8f4fd;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 20px;
        margin-top: 12px;
        letter-spacing: -0.3px;
    }

    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 40px;
        animation: fadeInDown 0.6s ease-out;
    }

    .header-container h1 {
        font-size: 48px;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #e8f4fd 0%, #4fc3f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .header-container p {
        font-size: 16px;
        color: #a8c5d9;
        font-weight: 300;
    }

    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    [data-testid="stMetric"] {
        background: transparent !important;
    }

    [data-testid="metricValue"] {
        color: #4fc3f7 !important;
    }

    [data-testid="metricLabel"] {
        color: #7bafc8 !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4fc3f7 0%, #1e88e5 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(79, 195, 247, 0.25);
    }

    .stButton > button:hover {
        box-shadow: 0 8px 24px rgba(79, 195, 247, 0.4);
        transform: translateY(-2px);
    }

    /* Responsive */
    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem;
        }

        .header-container h1 {
            font-size: 36px;
        }

        .metric-value.large {
            font-size: 48px;
        }

        .metric-value {
            font-size: 28px;
        }
    }

    /* Error styling */
    .stError {
        background: rgba(239, 83, 80, 0.1) !important;
        border: 1px solid rgba(239, 83, 80, 0.3) !important;
        border-radius: 12px !important;
    }

    /* Status indicator */
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4caf50;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
""", unsafe_allow_html=True)

# ── Config ───────────────────────────────────────────────────────────────────
LATITUDE = 52.0294
LONGITUDE = 5.1692
API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current=temperature_2m,apparent_temperature,weathercode,windspeed_10m"
    "&daily=sunrise,sunset"
    "&timezone=Europe%2FAmsterdam"
)

WMO_CODES = {
    0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"), 45: ("Foggy", "🌫️"), 48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"), 53: ("Drizzle", "🌦️"), 55: ("Heavy drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"), 63: ("Rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
    71: ("Slight snow", "🌨️"), 73: ("Snow", "❄️"), 75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "🌨️"), 80: ("Rain showers", "🌦️"), 81: ("Rain showers", "🌧️"),
    82: ("Violent showers", "⛈️"), 85: ("Snow showers", "🌨️"), 86: ("Heavy snow", "❄️"),
    95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm+hail", "⛈️"), 99: ("Thunderstorm+hail", "⛈️"),
}

# ── Fetch Weather ────────────────────────────────────────────────────────────
def fetch_weather():
    try:
        req = urllib.request.Request(
            API_URL, headers={"User-Agent": "HoutenWeatherDashboard/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        cur = data["current"]
        code = int(cur["weathercode"])
        label, emoji = WMO_CODES.get(code, ("Unknown", "🌡️"))
        
        daily = data["daily"]
        sunrise = daily["sunrise"][0].split("T")[1][:5]
        sunset = daily["sunset"][0].split("T")[1][:5]
        
        ams_tz = pytz.timezone("Europe/Amsterdam")
        updated = datetime.now(ams_tz).strftime("%H:%M")
        
        return {
            "temp": round(cur["temperature_2m"]),
            "feels_like": round(cur["apparent_temperature"]),
            "wind_ms": round(cur["windspeed_10m"], 1),
            "condition": label,
            "emoji": emoji,
            "sunrise": sunrise,
            "sunset": sunset,
            "updated": updated,
        }
    except Exception as e:
        return None

# ── Auto-refresh ────────────────────────────────────────────────────────────
st.markdown("""
    <script>
        setTimeout(function() {
            location.reload();
        }, 600000);
    </script>
""", unsafe_allow_html=True)

# ── Main UI ──────────────────────────────────────────────────────────────────
data = fetch_weather()

# Header
st.markdown("""
    <div class="header-container">
        <h1>🌤️ Houten Weather</h1>
        <p>Real-time weather for Houten, Netherlands</p>
    </div>
""", unsafe_allow_html=True)

if data:
    # ── Main metrics (temperature + condition) ────────────────────────────────
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
            <div class="glass-card temp-card">
                <span class="metric-label">Temperature</span>
                <div class="metric-value large">%d°</div>
                <div class="metric-secondary">Feels like %d°</div>
            </div>
        """ % (data["temp"], data["feels_like"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="glass-card temp-card">
                <span class="metric-label">Condition</span>
                <div class="metric-icon">{data['emoji']}</div>
                <div style="color: #e8f4fd; font-size: 20px; font-weight: 500;">
                    {data['condition']}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # ── Secondary metrics (wind, updated, location) ───────────────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3, gap="large")
    
    with col3:
        st.markdown(f"""
            <div class="glass-card">
                <span class="metric-label">💨 Wind Speed</span>
                <div class="metric-value">{data['wind_ms']}</div>
                <div class="metric-secondary">m/s</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="glass-card">
                <span class="metric-label">🕐 Last Updated</span>
                <div class="metric-value" style="font-size: 32px; color: #4fc3f7;">{data['updated']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
            <div class="glass-card">
                <span class="metric-label">📍 Location</span>
                <div style="color: #e8f4fd; font-size: 20px; font-weight: 500; margin-top: 8px;">
                    Houten, NL
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # ── Sun times ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">☀️ Sun Times (Amsterdam)</div>', unsafe_allow_html=True)
    
    sun_col1, sun_col2 = st.columns(2, gap="large")
    
    with sun_col1:
        st.markdown(f"""
            <div class="glass-card">
                <span class="metric-label">🌅 Sunrise</span>
                <div class="metric-value">{data['sunrise']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with sun_col2:
        st.markdown(f"""
            <div class="glass-card">
                <span class="metric-label">🌇 Sunset</span>
                <div class="metric-value">{data['sunset']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col_refresh = st.columns([1, 1, 1])
    with col_refresh[1]:
        if st.button("🔄 Refresh Now", key="refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("""
        <div style="text-align: center; margin-top: 24px; color: #7bafc8; font-size: 12px;">
            <span class="status-dot"></span>Auto-refreshes every 10 minutes
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Could not fetch weather data. Check your connection.")
    if st.button("Retry", use_container_width=True):
        st.rerun()
