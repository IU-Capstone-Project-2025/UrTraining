import os
import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from models import CourseAssistantRequest
from selection_assistent import CourseAssistant
from gigachat_client import get_gigachat_client

giga = get_gigachat_client()

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

course_assistant_instance = CourseAssistant(giga, "GigaChat:latest")

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
