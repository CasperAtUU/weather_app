# Houten Weather — Streamlit Edition

A real-time weather widget for Houten, Netherlands. Deploys instantly to Streamlit Cloud.

## Files

- `streamlit_weather_app.py` — Main app
- `requirements.txt` — Dependencies (just Streamlit)

## Local Testing

```bash
pip install streamlit
streamlit run streamlit_weather_app.py
```

Then open `http://localhost:8501` in your browser.

## Deploy to Streamlit Cloud

1. **Create a GitHub repo** with these files:
   ```
   your-repo/
   ├── streamlit_weather_app.py
   └── requirements.txt
   ```

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Click "New app"** and select your repo + `streamlit_weather_app.py`

4. **Done!** Your app is live at `yourname-weather-something.streamlit.app`

5. **Share the link** — anyone can open it on their phone

## Notes

- Data refreshes every 10 minutes (cached)
- Click "Refresh Now" for instant update
- Works on any device, anywhere (no WiFi needed)
- Free Streamlit Cloud tier is generous

---

**Made with ❄️ for Houten, NL**
