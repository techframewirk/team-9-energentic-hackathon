# backend/test_weather.py
import json
from agents.weather_agent import run as weather_run

if __name__ == "__main__":
    # fake empty ctx or pull in your real session_context.json
    ctx = {"user_profile": {"location": {"lat":37.7749, "lon":-122.4194}}}

    res = weather_run(ctx)
    print("\n=== Weather OUTPUT ===")
    print(json.dumps(res["output"], indent=2))
    print("\n=== Weather LAAM ===")
    print(json.dumps(res["laam"], indent=2))
