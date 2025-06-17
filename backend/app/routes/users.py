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
    try:
        # Build user data with proper defaults and validation
        user_data = {
            "personal_data": {
                "full_name": db_user.full_name or "Unknown"
            },
            "basic_information": {
                "gender": profile.gender if profile and profile.gender else "male",  # Default gender
                "age": profile.age if profile and profile.age else 25,  # Default age
                "height_cm": profile.height_cm if profile and profile.height_cm else 170,  # Default height
                "weight_kg": profile.weight_kg if profile and profile.weight_kg else 70.0  # Default weight
            },
            "training_goals": profile.training_goals if profile and profile.training_goals else ["maintain_fitness"],  # Default goal
            "training_experience": {
                "level": profile.training_level if profile and profile.training_level else "beginner",  # Default level
                "frequency_last_3_months": profile.frequency_last_3_months if profile and profile.frequency_last_3_months else "1_2_times_week"  # Default frequency
            },
            "preferences": {
                "training_location": profile.training_location if profile and profile.training_location else "home",  # Default location
                "location_details": profile.location_details if profile and profile.location_details else "no_equipment",  # Default details
                "session_duration": profile.session_duration if profile and profile.session_duration else "30_45_min"  # Default duration
            },
            "health": {
                "joint_back_problems": profile.joint_back_problems if profile and profile.joint_back_problems is not None else False,
                "chronic_conditions": profile.chronic_conditions if profile and profile.chronic_conditions is not None else False,
                "health_details": profile.health_details if profile and profile.health_details else None
            },
            "training_types": {
                "strength_training": profile.strength_training if profile and profile.strength_training else 3,  # Default interest
                "cardio": profile.cardio if profile and profile.cardio else 3,
                "hiit": profile.hiit if profile and profile.hiit else 2,
                "yoga_pilates": profile.yoga_pilates if profile and profile.yoga_pilates else 2,
                "functional_training": profile.functional_training if profile and profile.functional_training else 3,
                "stretching": profile.stretching if profile and profile.stretching else 4
            },
            "id": str(db_user.id),
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
            "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
        }
        
        print(f"Attempting to create UserResponse for user {db_user.id} with data: {user_data}")
        return UserResponse(**user_data)
        
    except Exception as e:
        print(f"❌ DETAILED ERROR for user {db_user.id} ({db_user.username}):")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        print(f"   User full_name: {db_user.full_name}")
        print(f"   Profile exists: {profile is not None}")
        if profile:
            print(f"   Profile details:")
            print(f"     - gender: {profile.gender} (type: {type(profile.gender)})")
            print(f"     - age: {profile.age} (type: {type(profile.age)})")
            print(f"     - training_goals: {profile.training_goals} (type: {type(profile.training_goals)})")
            print(f"     - training_level: {profile.training_level} (type: {type(profile.training_level)})")
        
        # Try to create a minimal user response to avoid total failure
        try:
            minimal_data = {
                "personal_data": {"full_name": db_user.full_name or "Unknown"},
                "basic_information": {"gender": "male", "age": 25, "height_cm": 170, "weight_kg": 70.0},
                "training_goals": ["maintain_fitness"],
                "training_experience": {"level": "beginner", "frequency_last_3_months": "1_2_times_week"},
                "preferences": {"training_location": "home", "location_details": "no_equipment", "session_duration": "30_45_min"},
                "health": {"joint_back_problems": False, "chronic_conditions": False, "health_details": None},
                "training_types": {"strength_training": 3, "cardio": 3, "hiit": 2, "yoga_pilates": 2, "functional_training": 3, "stretching": 4},
                "id": str(db_user.id),
                "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
                "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
            }
            print(f"✅ Using minimal data fallback for user {db_user.id}")
            return UserResponse(**minimal_data)
        except Exception as fallback_error:
            print(f"❌ Even minimal fallback failed for user {db_user.id}: {fallback_error}")
            raise e  # Re-raise original error

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
        # Debug: Check database connection
        print("Attempting to connect to database...")
        
        # Get users from database
        from app.models.database_models import User as DBUser
        print("Querying users from database...")
        users = db.query(DBUser).offset(skip).limit(limit).all()
        print(f"Found {len(users)} users in database")
        
        if not users:
            print("No users found in database - returning empty list")
            return []
        
        users_list = []
        skipped_users = []
        
        for i, db_user in enumerate(users):
            try:
                print(f"Processing user {i+1}/{len(users)}: ID={db_user.id}, username={db_user.username}")
                
                # Get training profile with more detailed logging
                profile = get_training_profile(db, db_user.id)
                print(f"Retrieved profile for user {db_user.username}: {'Yes' if profile else 'No'}")
                
                # Convert to response format
                user_response = convert_db_user_to_response(db_user, profile)
                users_list.append(user_response)
                print(f"Successfully processed user {db_user.username}")
                
            except Exception as user_error:
                error_msg = f"Error processing user {db_user.username} (ID: {db_user.id}): {user_error}"
                print(error_msg)
                skipped_users.append({
                    "id": db_user.id,
                    "username": db_user.username,
                    "error": str(user_error)
                })
                # Continue processing other users
                continue
        
        print(f"Successfully processed {len(users_list)} users, skipped {len(skipped_users)} users")
        if skipped_users:
            print("Skipped users:")
            for skipped in skipped_users:
                print(f"  - {skipped['username']} (ID: {skipped['id']}): {skipped['error']}")
        
        return users_list
        
    except Exception as e:
        print(f"Error retrieving users: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
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

@router.get("/users/test")
async def test_users_endpoint():
    """
    Simple test endpoint to check if users route is working
    """
    return {
        "message": "Users endpoint is working",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/users/db-test")
async def test_database_connection(db: Session = Depends(get_db)):
    """
    Test database connection
    """
    try:
        # Try to count users
        from app.models.database_models import User as DBUser
        user_count = db.query(DBUser).count()
        
        return {
            "message": "Database connection successful",
            "user_count": user_count,
            "status": "success"
        }
    except Exception as e:
        return {
            "message": "Database connection failed",
            "error": str(e),
            "status": "failed"
        }



@router.get("/users/debug/raw")
async def debug_raw_user_data(limit: int = 10, db: Session = Depends(get_db)):
    """
    Debug endpoint to show raw user data without processing
    """
    try:
        from app.models.database_models import User as DBUser
        
        users = db.query(DBUser).limit(limit).all()
        raw_data = []
        
        for user in users:
            profile = get_training_profile(db, user.id)
            raw_data.append({
                "database_user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                    "created_at": str(user.created_at),
                    "updated_at": str(user.updated_at)
                },
                "training_profile": {
                    "exists": profile is not None,
                    "data": {
                        "gender": profile.gender if profile else None,
                        "age": profile.age if profile else None,
                        "height_cm": profile.height_cm if profile else None,
                        "weight_kg": profile.weight_kg if profile else None,
                        "training_goals": profile.training_goals if profile else None,
                        "training_level": profile.training_level if profile else None,
                        "frequency_last_3_months": profile.frequency_last_3_months if profile else None,
                        "training_location": profile.training_location if profile else None,
                        "location_details": profile.location_details if profile else None,
                        "session_duration": profile.session_duration if profile else None,
                        "joint_back_problems": profile.joint_back_problems if profile else None,
                        "chronic_conditions": profile.chronic_conditions if profile else None,
                        "health_details": profile.health_details if profile else None,
                        "strength_training": profile.strength_training if profile else None,
                        "cardio": profile.cardio if profile else None,
                        "hiit": profile.hiit if profile else None,
                        "yoga_pilates": profile.yoga_pilates if profile else None,
                        "functional_training": profile.functional_training if profile else None,
                        "stretching": profile.stretching if profile else None
                    } if profile else None
                }
            })
        
        return {
            "total_users_found": len(users),
            "raw_user_data": raw_data
        }
        
    except Exception as e:
        return {"error": str(e)} 