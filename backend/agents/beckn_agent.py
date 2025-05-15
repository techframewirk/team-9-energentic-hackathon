# backend/agents/beckn_agent.py
"""
👉 Stub for the BecknAgent.
   Later you’ll replace the placeholder logic with real Beckn flows
   (search / select / init / confirm / status) using the sandbox URLs.
"""

import uuid
import datetime

def run(context: dict, laam_msg: dict | None = None) -> dict:
    """
    For now it just echoes that it’s alive.
    `laam_msg` will be the LAAM command you pass when the CEO wants
    to buy / enrol / whatever.
    """
    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "from": "BecknAgent",
        "to": laam_msg.get("from", "broadcast") if laam_msg else "broadcast",
        "type": "response",
        "payload": {"status": "noop – stub"},
        "reason": "BecknAgent stub executed."
    }
