from fastapi import APIRouter

router = APIRouter()

@router.get("/programs")
def get_programs():
    return [
        {
            "id": 1,
            "title": "Mobility Reset",
            "description": "A course to reboot your flexibility and joint health.",
            "duration_weeks": 2,
            "level": "Beginner",
        }
    ]

@router.get("/recommendation")
def get_recommendation():
    return {
        "recommended_program": {
            "id": 1,
            "title": "Mobility Reset",
            "reason": "Great for beginners with joint issues",
        }
    }
