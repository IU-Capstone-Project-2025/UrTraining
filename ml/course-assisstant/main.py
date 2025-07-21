import os
import fastapi
import uvicorn
from openai import AsyncOpenAI
from fastapi.middleware.cors import CORSMiddleware
from models import CourseAssistantRequest
from selection_assistent import CourseAssistant


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

MODEL_ID = os.getenv("MODEL_ID", "google/gemma-3-27b-it")

client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url="https://api.together.xyz/v1")

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

course_assistant_instance = CourseAssistant(client, MODEL_ID)

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "course-assisstant"}


def postprocess_response(response: str) -> str:
    response = response.replace("```json", "").replace("```", "")
    return response

@app.post("/course-assistant-chat")
async def course_assistant(request: CourseAssistantRequest):
    try:
        return await course_assistant_instance.chat(request)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
