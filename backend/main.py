# backend/main.py
"""
Single‐file orchestrator with ONE periodic trigger that pulls fresh data
from the World‐Engine mocks via Grid / House / Weather agents,
then cascades through Analysis → Teacher → CEO → Housekeeper,
logging every inter‐agent message to agent_actions.log.
"""

import json, time, os, uuid, datetime, pathlib
from dotenv import load_dotenv

# paths & interval
BASE_DIR   = pathlib.Path(__file__).parent
CTX_PATH   = BASE_DIR / "session_context.json"
LOG_PATH   = BASE_DIR / "logs" / "agent_actions.log"
INTERVAL_S = int(os.getenv("TRIGGER_INTERVAL", "10"))

# look for a .env file in this same directory
env_path = BASE_DIR/ ".env"
load_dotenv(env_path)

from agents import (
    grid_run, house_run, weather_run,
    analysis_run, teacher_run, ceo_run,
    hk_run
)

# canonical empty context
DEFAULT_CTX = {
  "grid": {},
  "house": {},
  "weather": {},
  "insights": [],
  "actions": [],
  "flex_offers": [],
  "beckn_transactions": {},
  "world_engine_events": [],
  "user_profile": {},
  "metrics": {
    "energy_saved_kwh": 0.0,
    "cost_saved_inr": 0.0,
    "co2_avoided_kg": 0.0
  },
  "log_pointer": str(LOG_PATH),
}


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def load_ctx() -> dict:
    if CTX_PATH.exists():
        return json.loads(CTX_PATH.read_text())
    CTX_PATH.parent.mkdir(exist_ok=True, parents=True)
    CTX_PATH.write_text(json.dumps(DEFAULT_CTX, indent=2))
    return DEFAULT_CTX.copy()


def save_ctx(ctx: dict):
    CTX_PATH.write_text(json.dumps(ctx, indent=2))


def log_laam(msg: dict):
    LOG_PATH.parent.mkdir(exist_ok=True, parents=True)
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(msg) + "\n")


def make_laam(frm: str, to: str, typ: str, payload: dict, reason: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "timestamp": now_iso(),
        "from": frm,
        "to": to,
        "type": typ,
        "payload": payload,
        "reason": reason,
        "ttl": INTERVAL_S
    }


def run_cycle(ctx: dict):
    # 1️⃣ Pull fresh external data + log
    grid_out = grid_run(ctx)["output"]
    ctx["grid"] = grid_out
    log_laam(make_laam("GridInfoAgent", "InsightAgent", "data_update",
                       grid_out, "periodic grid data pull"))

    house_out = house_run(ctx)["output"]
    ctx["house"] = house_out
    log_laam(make_laam("HouseInfoAgent", "InsightAgent", "data_update",
                       house_out, "periodic house data pull"))
    
    weather_out = weather_run(ctx)
    ctx["weather"] = weather_out["output"]
    log_laam(weather_out["laam"])

    # 2️⃣ Analysis + log insight
    insight_laam = analysis_run(ctx)["output"]
    # parse the LLM JSON if it came back as a string
    if isinstance(insight_laam["payload"], str):
        insight_laam["payload"] = json.loads(insight_laam["payload"])
    ctx.setdefault("insights", []).append(insight_laam)
    log_laam(insight_laam)

    # 3️⃣ Teacher explanation + log
    teach_laam = teacher_run(ctx, insight_laam)["output"]
    if isinstance(teach_laam["payload"], str):
        teach_laam["payload"] = json.loads(teach_laam["payload"])
    log_laam(teach_laam)

    # 4️⃣ CEO decides + maybe creates device commands + log
    ceo_out = ceo_run(ctx, insight_laam, teach_laam)["output"]
    # ❇️  Print the speak text every cycle
    print(f"🤖 CEO says: {ceo_out['speak']}")

    #  — wrap “speak” itself in a tiny LAAM so our log remains a valid stream
    speak_laam = make_laam(
        frm="CEOAgent",
        to="User/Terminal",
        typ="insight",
        payload={"speak": ceo_out["speak"]},
        reason="CEO spoken output"
    )
    log_laam(speak_laam)

    #  — now log the actual command if there is one
    action_laam = ceo_out.get("action")
    if action_laam:
        log_laam(action_laam)
        hk_laam = hk_run(ctx, action_laam)["output"]
        ctx.setdefault("actions", []).append(hk_laam)
        log_laam(hk_laam)

    # 5️⃣ Persist context
    ctx["last_cycle"] = now_iso()
    save_ctx(ctx)

    print(f"[{ctx['last_cycle']}] cycle complete – "
          f"insights={len(ctx['insights'])}, actions={len(ctx['actions'])}")


def main():
    ctx = load_ctx()
    print("✨ agentic-home-energy orchestrator running – Ctrl-C to exit")
    try:
        while True:
            start = time.time()
            run_cycle(ctx)
            elapsed = time.time() - start
            time.sleep(max(0, INTERVAL_S - elapsed))
    except KeyboardInterrupt:
        print("\n👋 graceful shutdown – context saved.")
        save_ctx(ctx)


if __name__ == "__main__":
    main()
