from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Optional
from app.models.user import User, UserCreate, UserUpdate, UserResponse
from app.routes.auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter()

# In-memory storage (replace with database in production)
fake_users_db: Dict[str, dict] = {}

def user_to_response(user_id: str, user_data: dict) -> UserResponse:
    """Convert stored user data to UserResponse model"""
    user_response_data = user_data.copy()
    user_response_data["id"] = user_id
    return UserResponse(**user_response_data)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user profile
    """
    user_id = str(uuid.uuid4())
    current_time = datetime.now().isoformat()
    
    user_data = user.dict()
    user_data["created_at"] = current_time
    user_data["updated_at"] = current_time
    
    fake_users_db[user_id] = user_data
    
    return user_to_response(user_id, user_data)

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(skip: int = 0, limit: int = 100):
    """
    Retrieve all users with pagination
    """
    users_list = []
    user_items = list(fake_users_db.items())[skip:skip + limit]
    
    for user_id, user_data in user_items:
        users_list.append(user_to_response(user_id, user_data))
    
    return users_list

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieve a specific user by ID
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return user_to_response(user_id, fake_users_db[user_id])

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """
    Update a user's complete profile
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Get current user data
    current_user = fake_users_db[user_id].copy()
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            current_user[field] = value
    
    # Update timestamp
    current_user["updated_at"] = datetime.now().isoformat()
    
    # Save updated user
    fake_users_db[user_id] = current_user
    
    return user_to_response(user_id, current_user)

@router.patch("/users/{user_id}", response_model=UserResponse)
async def partially_update_user(user_id: str, user_update: UserUpdate):
    """
    Partially update a user's profile (same as PUT but more explicit)
    """
    return await update_user(user_id, user_update)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a user profile
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    del fake_users_db[user_id]
    return None

@router.get("/users/search/by-goal", response_model=List[UserResponse])
async def search_users_by_goal(goal: str, skip: int = 0, limit: int = 100):
    """
    Search users by training goal
    """
    matching_users = []
    
    for user_id, user_data in fake_users_db.items():
        if goal.lower() in [g.lower() for g in user_data.get("training_goals", [])]:
            matching_users.append(user_to_response(user_id, user_data))
    
    return matching_users[skip:skip + limit]

@router.get("/users/search/by-level", response_model=List[UserResponse])
async def search_users_by_level(level: str, skip: int = 0, limit: int = 100):
    """
    Search users by training experience level
    """
    matching_users = []
    
    for user_id, user_data in fake_users_db.items():
        user_level = user_data.get("training_experience", {}).get("level", "")
        if level.lower() == user_level.lower():
            matching_users.append(user_to_response(user_id, user_data))
    
    return matching_users[skip:skip + limit]

@router.get("/users/{user_id}/recommendations")
async def get_user_recommendations(user_id: str):
    """
    Get training recommendations based on user profile
    This is a placeholder for ML-based recommendations
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    user_data = fake_users_db[user_id]
    
    # Simple recommendation logic based on user data
    recommendations = []
    
    # Based on training goals
    goals = user_data.get("training_goals", [])
    if "weight_loss" in goals:
        recommendations.append("High-intensity cardio workouts")
        recommendations.append("Circuit training programs")
    if "muscle_gain" in goals:
        recommendations.append("Progressive strength training")
        recommendations.append("Compound exercises focus")
    if "improve_flexibility" in goals:
        recommendations.append("Daily stretching routines")
        recommendations.append("Yoga and pilates sessions")
    
    # Based on experience level
    level = user_data.get("training_experience", {}).get("level", "")
    if level == "beginner":
        recommendations.append("Start with bodyweight exercises")
        recommendations.append("Focus on form and technique")
    elif level == "advanced":
        recommendations.append("Complex movement patterns")
        recommendations.append("Periodized training programs")
    
    # Based on health considerations
    health = user_data.get("health", {})
    if health.get("joint_back_problems"):
        recommendations.append("Low-impact exercises recommended")
        recommendations.append("Include mobility and stability work")
    
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "generated_at": datetime.now().isoformat()
    }

@router.get("/users/stats/overview")
async def get_users_stats():
    """
    Get overview statistics of all users
    """
    if not fake_users_db:
        return {
            "total_users": 0,
            "training_levels": {},
            "popular_goals": {},
            "age_groups": {}
        }
    
    total_users = len(fake_users_db)
    training_levels = {}
    goals_count = {}
    age_groups = {"18-25": 0, "26-35": 0, "36-45": 0, "46+": 0}
    
    for user_data in fake_users_db.values():
        # Count training levels
        level = user_data.get("training_experience", {}).get("level", "unknown")
        training_levels[level] = training_levels.get(level, 0) + 1
        
        # Count goals
        for goal in user_data.get("training_goals", []):
            goals_count[goal] = goals_count.get(goal, 0) + 1
        
        # Count age groups
        age = user_data.get("basic_information", {}).get("age", 0)
        if age <= 25:
            age_groups["18-25"] += 1
        elif 26 <= age <= 35:
            age_groups["26-35"] += 1
        elif 36 <= age <= 45:
            age_groups["36-45"] += 1
        elif age > 45:
            age_groups["46+"] += 1
    
    return {
        "total_users": total_users,
        "training_levels": training_levels,
        "popular_goals": goals_count,
        "age_groups": age_groups
    } 