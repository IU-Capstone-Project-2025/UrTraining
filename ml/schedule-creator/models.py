import uuid
from typing import List, Dict, Union
from pydantic import BaseModel, Field

class ScheduledWorkout(BaseModel):
    date: str = Field(..., description="Date of the workout in DD.MM.YYYY format")
    index: int = Field(..., description="Index of the workout in the original plan")

class TrackerAssistantRequest(BaseModel):
    weeks_number: int
    training_plan: List[dict] = Field(..., description="Training plan data in JSON format")
    training_profile: dict = Field(..., description="User training profile data in JSON format")
    start_date: str

class TrackerAssistantResponse(BaseModel):
    schedule: List[ScheduledWorkout] = Field(..., description="Created schedule")
    status: str = Field("success", description="Execution status")
