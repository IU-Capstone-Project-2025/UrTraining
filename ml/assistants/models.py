import uuid
import typing as tp

from pydantic import BaseModel


class SelectionAssistantResponse(BaseModel):
    answer: str


class SelectionAssistantRequest(BaseModel):
    session_id: uuid.UUID
    query: str
    user_form: str
    available_courses: tp.List[str]
