import os
import uvicorn
import fastapi
from openai import AsyncOpenAI
from fastapi.middleware.cors import CORSMiddleware

from models import TrackerAssistantRequest
from schedule_assistant import TrackerAssistant

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

MODEL_ID = os.getenv("MODEL_ID", "google/gemma-7b-it")

client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url="https://api.together.xyz/v1")

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracker_instance = TrackerAssistant(client, MODEL_ID)

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "schedule-creator"}

@app.post("/generate-tracker")
async def generate_tracker(request: TrackerAssistantRequest):
    try:
        return await tracker_instance.generate(request)
    except Exception as e:
        return {"Error processing request:": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
