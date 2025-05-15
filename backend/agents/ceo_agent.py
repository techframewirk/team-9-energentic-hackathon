# backend/agents/ceo_agent.py
import uuid
import datetime
import json
from llm_router import llm_router

def run(context: dict, analysis_msg: dict, teach_msg: dict) -> dict:
    """
    CEOAgent: decide if an appliance command is needed, output structured JSON.
    """
    expl = teach_msg["payload"].get("explanation", "")
    rec  = analysis_msg["payload"].get("recommendation", "")
    prompt = f"""
You are the CEO Agent. You are like the head of this entire organization. You will receive a short English explanation from TeacherAgent on what recomendation the AnaylysisAgent gave. Based on that, decide whether to issue a device command or only speak. Your task is to reduce costs, but not at the cost of User Comfort. 
Here is the TeacherAgent's explaination:
  "{expl}"
Here is the AnalysisrAgent's recomendation:
  "{rec}"

Decide whether to issue a device command. You are encouraged to be proactive and issue actions, but not all the time 

Output:
A JSON object with exactly:
  • "speak": string — what you say to the user. keep this short and sweet like a brief
  • "action": either null or an object with:
      - "target": string (e.g. "ac", "ev_charger")
      - "command": string (e.g. "set_temp", "pause_charging")
      - "params": object with any key/value parameters.

Example 1) When action is needed:
{{
  "speak": "Sure—turning off your geyser now.",
  "action": {{
    "target": "geyser",
    "command": "turn_off",
    "params": {{}}
  }}
}}

Example 2) When no action is needed:
{{
  "speak": "Got it—no changes necessary right now.",
  "action": null
}}

Do not output anything but valid JSON. **Output ONLY JSON as text**, no markdown, no code fences. Do NOT wrap it in triple backticks or any extra text.
"""

    llm_out = llm_router(prompt).strip()
    try:
        result = json.loads(llm_out)
    except json.JSONDecodeError:
        result = {"speak": expl, "action": None}

    speak = result.get("speak", expl)
    act   = result.get("action")
    action_laam = None

    if isinstance(act, dict):
        action_laam = {
            "id":        str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "from":      "CEOAgent",
            "to":        "HousekeeperAgent",
            "type":      "command",
            "payload":   act,
            "reason":    "LLM-generated structured command"
        }

    return {"output": {"speak": speak, "action": action_laam}}
