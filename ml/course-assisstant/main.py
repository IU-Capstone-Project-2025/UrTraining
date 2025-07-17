import os
import fastapi
import uvicorn
from openai import AsyncOpenAI
from models import CourseAssistantRequest
from selection_assistent import CourseAssistant


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

MODEL_ID = os.getenv("MODEL_ID", "google/gemma-3-27b-it")

client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url="https://api.kluster.ai/v1")

app = fastapi.FastAPI()
course_assistant_instance = CourseAssistant(client, MODEL_ID)

@app.post("/course-assistant-chat")
async def course_assistant(request: CourseAssistantRequest):
    try:
        return await course_assistant_instance.chat(request)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
