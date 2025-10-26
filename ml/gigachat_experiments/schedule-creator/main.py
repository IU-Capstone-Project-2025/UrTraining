import os
import uvicorn
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from gigachat_client import get_gigachat_client
from models import TrackerAssistantRequest
from schedule_assistant import TrackerAssistant

giga = get_gigachat_client()

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracker_instance = TrackerAssistant(giga, "GigaChat:latest")

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
