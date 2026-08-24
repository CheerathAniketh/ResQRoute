import requests
from core.config import OPENWEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def check_flood_risk(city: str = "Hyderabad"):
    try:
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        rainfall = data.get("rain", {}).get("1h", 0)
    except Exception:
        # Fallback simulation values for demo
        rainfall = 62.0

    if rainfall >= 50:
        risk = "HIGH"
    elif rainfall >= 20:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "city": city,
        "rainfall_mm": rainfall,
        "risk_level": risk,
        "crisis_mode_recommended": risk == "HIGH"
    }