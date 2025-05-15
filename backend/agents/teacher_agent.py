# backend/agents/teacher_agent.py
import uuid
import datetime
from llm_router import llm_router

def run(context: dict, insight_msg: dict) -> dict:
    """
    TeacherAgent: turn a recommendation into a structured explanation.
    """
    rec = insight_msg["payload"].get("recommendation", "")
    prompt = f"""
You are a Teacher Agent. You will receive a JSON now: Input recommendation:
  "{rec}"

Output:
Explain that recommendation in plain English, 1–2 sentences.  
Do NOT output JSON, code fences, or markdown—just the sentence.
"""

    llm_response = llm_router(prompt).strip()
    explanation = llm_response
    laam = {
        "id":        str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "from":      "TeacherAgent",
        "to":        "CEOAgent",
        "type":      "insight",
        "payload":   explanation if isinstance(explanation, dict) else {"explanation": explanation},
        "reason":    "LLM-generated structured explanation"
    }
    return {"output": laam}
