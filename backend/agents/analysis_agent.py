# backend/agents/analysis_agent.py
import uuid
import datetime
from llm_router import llm_router

def run(context: dict) -> dict:
    """
    AnalysisAgent: use LLM to generate a structured JSON insight.
    """
    grid   = context.get("grid", {})
    house  = context.get("house", {})
    weather = context.get("weather", {})

    prompt = """
You are an Energy Analysis Agent. 
Input:
  • grid: {grid}
  • house: {house}
  • weather: {weather}

Output:
A string in JSON object format with exactly two keys:
  1. recommendation — a single concise sentence describing the optimal energy action.
  2. "confidence" — a decimal number between 0.0 and 1.0 estimating your confidence.

Like this:
{{
  "recommendation": "<string>",
  "confidence": <float>
}}

Example valid output:
{{"recommendation":"Turn off the geyser during peak load hours","confidence":0.87}}

—no markdown, no backticks, no explanation, no extra keys.
Do not add any extra keys or commentary. **Output ONLY JSON**, no markdown, no code fences.
""".format(grid=grid, house=house, weather=weather)

    llm_response = llm_router(prompt).strip()

    # parse or trust it as JSON
    insight = llm_response
    laam = {
        "id":        str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "from":      "AnalysisAgent",
        "to":        "TeacherAgent",
        "type":      "insight",
        "payload":   insight if isinstance(insight, dict) else {"recommendation": insight},
        "reason":    "LLM-generated structured analysis"
    }
    return {"output": laam}
