from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "123":
        return {"token": "fake-jwt-token"}
    return {"error": "Invalid credentials"}