# backend/agents/weather_agent.py
"""
WeatherInfoAgent  — pulls current & next-6-hour rain + temperature
Returns both a LAAM message and a dict to be dropped into ctx["weather"].
"""

import requests, uuid, datetime, os

# House co-ordinates are read once from env or ctx["user_profile"]["location"]
LAT  = float(os.getenv("LATITUDE" , "37.7749"))   # San Francisco default
LON  = float(os.getenv("LONGITUDE", "-122.4194"))

def _now_iso():
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

def fetch_weather(lat: float, lon: float) -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&hourly=temperature_2m,precipitation_probability,weathercode"
        "&forecast_hours=6"
        "&timezone=UTC"
    )
    r = requests.get(url, timeout=7)
    r.raise_for_status()
    data = r.json()

    # --- helpers ------------------------------------------------------------
    cw   = data["current_weather"]
    temp = cw["temperature"]
    code = cw["weathercode"]
    raining_now = code in RAIN_CODES              # see constant below

    hh   = data["hourly"]
    rain_probs = hh["precipitation_probability"]
    next_6h_max = max(rain_probs) if rain_probs else 0

    weather_dict = {
        "temp_celsius": temp,
        "is_raining_now": raining_now,
        "rain_probability_next_hours": next_6h_max,  # %
        "forecast": [
            {
                "ts": ts,
                "temp_c": t,
                "prob_rain": p,
                "weathercode": c
            }
            for ts, t, p, c in zip(
                hh["time"], hh["temperature_2m"],
                hh["precipitation_probability"], hh["weathercode"]
            )
        ],
        "last_updated": _now_iso()
    }
    return weather_dict

# WMO weather-code groups that signify rain / drizzle / shower / thunder
RAIN_CODES = {51,53,55,61,63,65,80,81,82,95,96,99}  # 

# ---------------------------------------------------------------------------

def run(ctx: dict) -> dict:
    lat = ctx.get("user_profile", {}).get("location", {}).get("lat", LAT)
    lon = ctx.get("user_profile", {}).get("location", {}).get("lon", LON)

    wx = fetch_weather(lat, lon)

    laam = {
        "id": str(uuid.uuid4()),
        "timestamp": _now_iso(),
        "from": "WeatherInfoAgent",
        "to": "broadcast",
        "type": "data_update",
        "payload": wx,
        "reason": "6-hour forecast from Open-Meteo",
        "ttl": 600
    }
    return {"output": wx, "laam": laam}
