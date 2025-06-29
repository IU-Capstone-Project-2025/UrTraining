import os
import fastapi
import uvicorn
from openai import OpenAI
from models import CourseAssistantRequest
from course_assistant import CourseAssistant


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID", "gpt-3.5-turbo")


client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

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
