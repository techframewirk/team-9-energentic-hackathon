#backend/agnets/grid_agent.py
def run(input_json):
    return {
        "agent": "GridInfoAgent",
        "status": "success",
        "output": {
            "dr_signal": "reduce_usage_peak_6PM",
            "priority": "high"
        }
    }
