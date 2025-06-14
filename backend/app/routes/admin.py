from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

# Import from auth module
from app.routes.auth import get_current_user, fake_users_db

router = APIRouter()

@router.get("/stats")
async def get_admin_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get system statistics for admin dashboard"""
    
    # Get total users
    total_users = len(fake_users_db)
    
    # Get users with completed training profiles (assuming a profile is complete if it has basic info)
    completed_profiles = 0
    for user_data in fake_users_db.values():
        training_profile = user_data.get("training_profile", {})
        basic_info = training_profile.get("basic_information", {})
        if basic_info and any(basic_info.values()):
            completed_profiles += 1
    
    # For demo purposes, simulate some recent signups
    last_week_signups = min(2, total_users)  # Simulate 2 recent signups
    
    # For now, consider all users as active
    active_users = total_users
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "completed_profiles": completed_profiles,
        "last_week_signups": last_week_signups
    }

@router.get("/users/export")
async def export_users(
    basic: bool = Query(False, description="Export only basic user information"),
    current_user: dict = Depends(get_current_user)
):
    """Export all users data in JSON format"""
    
    exported_data = []
    user_id = 1
    
    for username, user_data in fake_users_db.items():
        user_export = {
            "id": user_id,
            "username": username,
            "email": user_data.get("email"),
            "full_name": user_data.get("full_name"),
            "is_active": True,  # All users in fake_db are active
            "created_at": datetime.utcnow().isoformat(),  # Simulated creation date
            "updated_at": datetime.utcnow().isoformat(),   # Simulated update date
            "hashed_password": user_data.get("hashed_password")  # Include password hash
        }
        
        if not basic:
            # Include training profile data if not basic export
            training_profile = user_data.get("training_profile")
            if training_profile:
                user_export["training_profile"] = {
                    "basic_information": training_profile.get("basic_information"),
                    "training_goals": training_profile.get("training_goals"),
                    "training_experience": training_profile.get("training_experience"),
                    "preferences": training_profile.get("preferences"),
                    "health": training_profile.get("health"),
                    "training_types": training_profile.get("training_types"),
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            else:
                user_export["training_profile"] = None
        
        exported_data.append(user_export)
        user_id += 1
    
    return {
        "export_type": "basic" if basic else "complete",
        "export_date": datetime.utcnow().isoformat(),
        "total_users": len(exported_data),
        "users": exported_data
    }

@router.get("/activity")
async def get_recent_activity(
    limit: int = Query(10, description="Number of recent activities to return"),
    current_user: dict = Depends(get_current_user)
):
    """Get recent user activity (simulated for demo purposes)"""
    
    activities = []
    
    # Simulate recent activities for demo purposes
    for username, user_data in list(fake_users_db.items())[:limit]:
        # Simulate user registration
        activities.append({
            "action": "User Registration",
            "user_email": user_data.get("email"),
            "timestamp": (datetime.utcnow() - timedelta(days=len(activities))).isoformat(),
            "details": f"New user {user_data.get('full_name') or user_data.get('email')} registered"
        })
        
        # Simulate profile update if user has training profile
        if user_data.get("training_profile"):
            activities.append({
                "action": "Profile Update",
                "user_email": user_data.get("email"),
                "timestamp": (datetime.utcnow() - timedelta(hours=len(activities) * 2)).isoformat(),
                "details": f"User {user_data.get('full_name') or user_data.get('email')} updated training profile"
            })
    
    # Sort activities by timestamp (most recent first)
    activities.sort(key=lambda x: x["timestamp"] or "", reverse=True)
    
    return activities[:limit]

@router.get("/users/{username}")
async def get_user_details(
    username: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed information about a specific user"""
    
    user_data = fake_users_db.get(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_details = {
        "username": username,
        "email": user_data.get("email"),
        "full_name": user_data.get("full_name"),
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "training_profile": None
    }
    
    training_profile = user_data.get("training_profile")
    if training_profile:
        user_details["training_profile"] = {
            "basic_information": training_profile.get("basic_information"),
            "training_goals": training_profile.get("training_goals"),
            "training_experience": training_profile.get("training_experience"),
            "preferences": training_profile.get("preferences"),
            "health": training_profile.get("health"),
            "training_types": training_profile.get("training_types"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    return user_details

@router.get("/users")
async def get_all_users_summary(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of users per page"),
    current_user: dict = Depends(get_current_user)
):
    """Get paginated list of all users with basic information"""
    
    total_users = len(fake_users_db)
    all_users = list(fake_users_db.items())
    
    # Apply pagination
    offset = (page - 1) * limit
    paginated_users = all_users[offset:offset + limit]
    
    users_summary = []
    user_id = offset + 1
    
    for username, user_data in paginated_users:
        has_training_profile = user_data.get("training_profile") is not None
        
        users_summary.append({
            "id": user_id,
            "username": username,
            "email": user_data.get("email"),
            "full_name": user_data.get("full_name"),
            "is_active": True,
            "has_training_profile": has_training_profile,
            "created_at": datetime.utcnow().isoformat()
        })
        user_id += 1
    
    return {
        "users": users_summary,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_users,
            "pages": (total_users + limit - 1) // limit
        }
    } 