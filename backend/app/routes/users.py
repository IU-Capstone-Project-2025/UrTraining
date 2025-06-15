from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserUpdate, UserResponse
from app.routes.auth import get_current_user
from app.database import get_db
from app.crud import get_user_by_id, create_user, update_user_profile, get_training_profile
from app.models.database_models import User as DBUser
from datetime import datetime

router = APIRouter()

def convert_db_user_to_response(db_user: DBUser, profile=None) -> UserResponse:
    """Convert database user to UserResponse model"""
    user_data = {
        "personal_data": {
            "full_name": db_user.full_name
        },
        "basic_information": {
            "gender": profile.gender if profile else None,
            "age": profile.age if profile else None,
            "height_cm": profile.height_cm if profile else None,
            "weight_kg": profile.weight_kg if profile else None
        },
        "training_goals": profile.training_goals if profile and profile.training_goals else [],
        "training_experience": {
            "level": profile.training_level if profile else None,
            "frequency_last_3_months": profile.frequency_last_3_months if profile else None
        },
        "preferences": {
            "training_location": profile.training_location if profile else None,
            "location_details": profile.location_details if profile else None,
            "session_duration": profile.session_duration if profile else None
        },
        "health": {
            "joint_back_problems": profile.joint_back_problems if profile else None,
            "chronic_conditions": profile.chronic_conditions if profile else None,
            "health_details": profile.health_details if profile else None
        },
        "training_types": {
            "strength_training": profile.strength_training if profile else None,
            "cardio": profile.cardio if profile else None,
            "hiit": profile.hiit if profile else None,
            "yoga_pilates": profile.yoga_pilates if profile else None,
            "functional_training": profile.functional_training if profile else None,
            "stretching": profile.stretching if profile else None
        },
        "id": str(db_user.id),
        "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
        "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
    }
    
    return UserResponse(**user_data)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user profile
    """
    try:
        # Create user in database
        db_user = create_user(
            db=db,
            username=f"user_{datetime.now().timestamp()}",  # Generate unique username
            email=user.personal_data.full_name.lower().replace(" ", ".") + "@example.com",
            password="temppassword123",  # Temporary password
            full_name=user.personal_data.full_name
        )
        
        # Update training profile with provided data
        from app.crud import update_training_profile
        profile_data = {
            "gender": user.basic_information.gender,
            "age": user.basic_information.age,
            "height_cm": user.basic_information.height_cm,
            "weight_kg": user.basic_information.weight_kg,
            "training_goals": [goal.value for goal in user.training_goals],
            "training_level": user.training_experience.level,
            "frequency_last_3_months": user.training_experience.frequency_last_3_months,
            "training_location": user.preferences.training_location,
            "location_details": user.preferences.location_details,
            "session_duration": user.preferences.session_duration,
            "joint_back_problems": user.health.joint_back_problems,
            "chronic_conditions": user.health.chronic_conditions,
            "health_details": user.health.health_details,
            "strength_training": user.training_types.strength_training,
            "cardio": user.training_types.cardio,
            "hiit": user.training_types.hiit,
            "yoga_pilates": user.training_types.yoga_pilates,
            "functional_training": user.training_types.functional_training,
            "stretching": user.training_types.stretching
        }
        
        updated_profile = update_training_profile(db, db_user.id, profile_data)
        
        return convert_db_user_to_response(db_user, updated_profile)
        
    except Exception as e:
        print(f"Error creating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user profile"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all users with pagination
    """
    try:
        # Get users from database
        from app.models.database_models import User as DBUser
        users = db.query(DBUser).offset(skip).limit(limit).all()
        
        users_list = []
        for db_user in users:
            profile = get_training_profile(db, db_user.id)
            users_list.append(convert_db_user_to_response(db_user, profile))
        
        return users_list
        
    except Exception as e:
        print(f"Error retrieving users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID
    """
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        profile = get_training_profile(db, db_user.id)
        return convert_db_user_to_response(db_user, profile)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user profile
    """
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update basic user information if provided
        if user_update.personal_data:
            update_user_profile(db, user_id, full_name=user_update.personal_data.full_name)
        
        # Update training profile if provided
        from app.crud import update_training_profile
        profile_data = {}
        
        if user_update.basic_information:
            profile_data.update({
                "gender": user_update.basic_information.gender,
                "age": user_update.basic_information.age,
                "height_cm": user_update.basic_information.height_cm,
                "weight_kg": user_update.basic_information.weight_kg
            })
        
        if user_update.training_goals:
            profile_data["training_goals"] = [goal.value for goal in user_update.training_goals]
        
        if user_update.training_experience:
            profile_data.update({
                "training_level": user_update.training_experience.level,
                "frequency_last_3_months": user_update.training_experience.frequency_last_3_months
            })
        
        if user_update.preferences:
            profile_data.update({
                "training_location": user_update.preferences.training_location,
                "location_details": user_update.preferences.location_details,
                "session_duration": user_update.preferences.session_duration
            })
        
        if user_update.health:
            profile_data.update({
                "joint_back_problems": user_update.health.joint_back_problems,
                "chronic_conditions": user_update.health.chronic_conditions,
                "health_details": user_update.health.health_details
            })
        
        if user_update.training_types:
            profile_data.update({
                "strength_training": user_update.training_types.strength_training,
                "cardio": user_update.training_types.cardio,
                "hiit": user_update.training_types.hiit,
                "yoga_pilates": user_update.training_types.yoga_pilates,
                "functional_training": user_update.training_types.functional_training,
                "stretching": user_update.training_types.stretching
            })
        
        # Update profile if there's data to update
        if profile_data:
            # Remove None values
            profile_data = {k: v for k, v in profile_data.items() if v is not None}
            update_training_profile(db, user_id, profile_data)
        
        # Get updated user and profile
        updated_user = get_user_by_id(db, user_id)
        updated_profile = get_training_profile(db, user_id)
        
        return convert_db_user_to_response(updated_user, updated_profile)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user
    """
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete user and related data (cascading should handle training profile)
        db.delete(db_user)
        db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting user: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )

@router.get("/users/me/profile", response_model=UserResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user's profile
    """
    try:
        db_user = get_user_by_id(db, current_user["id"])
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        profile = get_training_profile(db, db_user.id)
        return convert_db_user_to_response(db_user, profile)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )

@router.get("/users/search/by-goal", response_model=List[UserResponse])
async def search_users_by_goal(goal: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Search users by training goal
    """
    try:
        from app.models.database_models import TrainingProfile
        from sqlalchemy import func
        
        # Search for profiles that contain the goal in their training_goals JSON array
        profiles = db.query(TrainingProfile).filter(
            func.json_array_length(TrainingProfile.training_goals) > 0
        ).all()
        
        matching_users = []
        for profile in profiles:
            if profile.training_goals and goal.lower() in [g.lower() for g in profile.training_goals]:
                db_user = get_user_by_id(db, profile.user_id)
                if db_user:
                    matching_users.append(convert_db_user_to_response(db_user, profile))
        
        return matching_users[skip:skip + limit]
        
    except Exception as e:
        print(f"Error searching users by goal: {e}")
        return []

@router.get("/users/search/by-level", response_model=List[UserResponse])
async def search_users_by_level(level: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Search users by training experience level
    """
    try:
        from app.models.database_models import TrainingProfile
        
        profiles = db.query(TrainingProfile).filter(
            TrainingProfile.training_level.ilike(f"%{level}%")
        ).offset(skip).limit(limit).all()
        
        matching_users = []
        for profile in profiles:
            db_user = get_user_by_id(db, profile.user_id)
            if db_user:
                matching_users.append(convert_db_user_to_response(db_user, profile))
        
        return matching_users
        
    except Exception as e:
        print(f"Error searching users by level: {e}")
        return []

@router.get("/users/{user_id}/recommendations")
async def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
    """
    Get training recommendations based on user profile
    This is a placeholder for ML-based recommendations
    """
    try:
        db_user = get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        profile = get_training_profile(db, user_id)
        if not profile:
            return {
                "user_id": user_id,
                "recommendations": ["Complete your training profile to get personalized recommendations"],
                "generated_at": datetime.now().isoformat()
            }
        
        # Simple recommendation logic based on user data
        recommendations = []
        
        # Based on training goals
        goals = profile.training_goals or []
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
        if profile.training_level == "beginner":
            recommendations.append("Start with bodyweight exercises")
            recommendations.append("Focus on form and technique")
        elif profile.training_level == "advanced":
            recommendations.append("Complex movement patterns")
            recommendations.append("Periodized training programs")
        
        # Based on health considerations
        if profile.joint_back_problems:
            recommendations.append("Low-impact exercises recommended")
            recommendations.append("Include mobility and stability work")
        
        if not recommendations:
            recommendations = ["Update your training profile for personalized recommendations"]
        
        return {
            "user_id": user_id,
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )

@router.get("/users/stats/overview")
async def get_users_stats(db: Session = Depends(get_db)):
    """
    Get overview statistics of all users
    """
    try:
        from app.models.database_models import User as DBUser, TrainingProfile
        from sqlalchemy import func
        
        # Get total users count
        total_users = db.query(func.count(DBUser.id)).scalar()
        
        if total_users == 0:
            return {
                "total_users": 0,
                "training_levels": {},
                "popular_goals": {},
                "age_groups": {}
            }
        
        # Get training levels count
        training_levels = {}
        level_stats = db.query(
            TrainingProfile.training_level,
            func.count(TrainingProfile.training_level)
        ).group_by(TrainingProfile.training_level).all()
        
        for level, count in level_stats:
            if level:
                training_levels[level] = count
        
        # Get popular goals
        goals_count = {}
        profiles_with_goals = db.query(TrainingProfile).filter(
            TrainingProfile.training_goals.isnot(None)
        ).all()
        
        for profile in profiles_with_goals:
            if profile.training_goals:
                for goal in profile.training_goals:
                    goals_count[goal] = goals_count.get(goal, 0) + 1
        
        # Get age groups
        age_groups = {"18-25": 0, "26-35": 0, "36-45": 0, "46+": 0}
        age_stats = db.query(TrainingProfile.age).filter(
            TrainingProfile.age.isnot(None)
        ).all()
        
        for (age,) in age_stats:
            if age <= 25:
                age_groups["18-25"] += 1
            elif 26 <= age <= 35:
                age_groups["26-35"] += 1
            elif 36 <= age <= 45:
                age_groups["36-45"] += 1
            else:
                age_groups["46+"] += 1
        
        return {
            "total_users": total_users,
            "training_levels": training_levels,
            "popular_goals": goals_count,
            "age_groups": age_groups
        }
        
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return {
            "total_users": 0,
            "training_levels": {},
            "popular_goals": {},
            "age_groups": {}
        } 