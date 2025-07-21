import requests
import os

from fastapi import HTTPException

KLUSTER_API_KEY = os.environ.get("KLUSTER_API_KEY")

if not KLUSTER_API_KEY:
    raise RuntimeError("KLUSTER_API_KEY environment variable not set")

HEADERS = {
    "Authorization": f"Bearer {KLUSTER_API_KEY}",
    "Content-Type": "application/json"
}


# === Helper to call Kluster LLM API ===

def call_kluster_llm(model: str, messages: list, max_tokens: int = 3500, temperature: float = 0.0) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=HEADERS, json=payload)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Kluster API error: {e} - {response.text}")
    return response.json()["choices"][0]["message"]["content"].strip()