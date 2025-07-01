import uuid
from typing import Optional
from pydantic import BaseModel, Field

class CourseAssistantResponse(BaseModel):
    answer: str = Field(..., description="Assistant's response")
    session_id: uuid.UUID = Field(..., description="Session ID")
    status: str = Field("success", description="Execution status")

class CourseAssistantRequest(BaseModel):
    session_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Unique session identifier"
    )
    query: str = Field(..., min_length=1, description="User query")
    user_form: str = Field(..., description="User form data")
    course_data: dict = Field(..., description="Course data in JSON format")
