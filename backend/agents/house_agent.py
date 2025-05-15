#backend/agnets/house_agent.py

def run(input_json):
    return {
        "agent": "HouseInfoAgent",
        "status": "success",
        "output": {
            "thermostat": 23,
            "ev_status": "charging",
            "geyser": "on"
        }
    }
