from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Course(BaseModel):
    id: int
    name: str
    duration: int

fake_courses = [
    Course(id=1, name="Mobility Reset", duration=30, level="Beginner", goal="Flexibility"),
    Course(id=2, name="Fat Burn Express", duration=45, level="Intermediate", goal="Weight Loss"),
    Course(id=3, name="Power HIIT", duration=40, level="Advanced", goal="Endurance"),
    Course(id=4, name="Yoga for Energy", duration=50, level="All Levels", goal="Stress Relief"),
    Course(id=5, name="Morning Stretch", duration=20, level="Beginner", goal="Mobility"),
    Course(id=6, name="Total Body Strength", duration=60, level="Intermediate", goal="Muscle Gain"),
    Course(id=7, name="Core Crusher", duration=30, level="All Levels", goal="Core Strength"),
    Course(id=8, name="Glute Power", duration=35, level="Beginner", goal="Toning"),
    Course(id=9, name="Boxing Basics", duration=45, level="Beginner", goal="Cardio"),
    Course(id=10, name="Quick Fix: 15 Min Burner", duration=15, level="All Levels", goal="Fat Burn"),
    Course(id=11, name="Mobility Flow Advanced", duration=40, level="Advanced", goal="Flexibility"),
    Course(id=12, name="Low Impact Burn", duration=30, level="Beginner", goal="Weight Loss")
]

@router.get("/courses")
def get_courses():
    return fake_courses