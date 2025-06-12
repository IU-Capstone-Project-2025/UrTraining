import os
from dotenv import load_dotenv
from typing import Dict, Optional, Any

from ml.scripts.prompts import CLIENT_FORM_SYNT_DATA_PROMPT as prefix

from openai import OpenAI

load_dotenv()

KLUSTER_AI_TOKEN: str = os.getenv("KLUSTER_AI_TOKEN")
MODELS: Dict[str, str] = {
    "gemma": "google/gemma-3-27b-it",
    "deepseek_r1": "deepseek-ai/DeepSeek-R1-0528",
    "llama3.1_8b": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
    "qwen235b": "Qwen/Qwen3-235B-A22B-FP8",
}
print(KLUSTER_AI_TOKEN)
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=KLUSTER_AI_TOKEN,
)


def get_response(
    model_name: str,
    user_prompt: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = 0.25,
    top_k: Optional[int] = 50,
) -> Dict[str, Any]:
    model_id: str = MODELS.get(model_name, None)
    assert (
        model_id is not None
    ), f"Model type '{model_name}' is not supported. List of supported models: {MODELS.keys()}"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_prompt})

    response: Dict[str, Any] = client.chat.completions.create(
        model=model_id, messages=messages, temperature=temperature
    )

    return response


print(get_response("gemma", "Привет. Ты кто?"))
