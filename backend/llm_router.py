# backend/llm_router.py  – Gemini edition
import os, json, requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")           # NEW
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
TIMEOUT_S      = float(os.getenv("LLM_TIMEOUT", "90"))

def llm_router(prompt: str,
               max_tokens: int = 1024,
               temperature: float = 0.7,
               top_p: float = 0.95) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Set GEMINI_API_KEY")

    endpoint = (f"https://generativelanguage.googleapis.com/v1beta/"
                f"models/{GEMINI_MODEL}:generateContent")

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-goog-api-key": GEMINI_API_KEY                 # NEW
    }

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {                           # NEW
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p
        }
    }

    try:
        r = requests.post(endpoint, headers=headers,
                          json=payload, timeout=TIMEOUT_S)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"[llm_router] Error: {e}")
        return "[LLM error]"
