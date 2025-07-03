import os

import fastapi
import uvicorn
from openai import OpenAI

from ml.assistants.models import SelectionAssistantRequest
from ml.assistants.selection_assistant import SelectionAssistant


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

app = fastapi.FastAPI()
selection_assistant_instance = SelectionAssistant(client, MODEL_ID)


@app.post("/selection-assistant-chat")
async def selection_assistant(request: SelectionAssistantRequest):
    return selection_assistant_instance.chat(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
