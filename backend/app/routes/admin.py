from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import json

# Import database and CRUD functions
from app.database import get_db
from app.crud import (
    get_user_by_username, get_user_by_id, get_training_profile, 
    get_user_active_sessions, cleanup_expired_sessions
)
from app.models.database_models import User as DBUser, TrainingProfile
from app.routes.auth import get_current_user

router = APIRouter()

@router.get("/stats")
async def get_admin_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system statistics for admin dashboard"""
    
    try:
        from sqlalchemy import func
        
        # Get total users
        total_users = db.query(func.count(DBUser.id)).scalar() or 0
        
        # Get users with completed training profiles
        completed_profiles = db.query(func.count(TrainingProfile.id)).filter(
            TrainingProfile.training_level.isnot(None)
        ).scalar() or 0
        
        # Get users created in the last week
        last_week = datetime.utcnow() - timedelta(days=7)
        last_week_signups = db.query(func.count(DBUser.id)).filter(
            DBUser.created_at >= last_week
        ).scalar() or 0
        
        # Get active users (users who have logged in recently)
        # For now, consider all users as active since we don't track last login
        active_users = total_users
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "completed_profiles": completed_profiles,
            "last_week_signups": last_week_signups
        }
        
    except Exception as e:
        print(f"Error getting admin stats: {e}")
        return {
            "total_users": 0,
            "active_users": 0,
            "completed_profiles": 0,
            "last_week_signups": 0
        }

@router.get("/users/export")
async def export_users(
    basic: bool = Query(False, description="Export only basic user information"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export all users data in JSON format"""
    
    try:
        # Get all users
        users = db.query(DBUser).all()
        
        exported_data = []
        
        for user in users:
            user_export = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "hashed_password": user.hashed_password  # Include password hash for admin export
            }
            
            if not basic:
                # Include training profile data if not basic export
                profile = get_training_profile(db, user.id)
                if profile:
                    user_export["training_profile"] = {
                        "basic_information": {
                            "gender": profile.gender,
                            "age": profile.age,
                            "height_cm": profile.height_cm,
                            "weight_kg": profile.weight_kg
                        },
                        "training_goals": profile.training_goals,
                        "training_experience": {
                            "level": profile.training_level,
                            "frequency_last_3_months": profile.frequency_last_3_months
                        },
                        "preferences": {
                            "training_location": profile.training_location,
                            "location_details": profile.location_details,
                            "session_duration": profile.session_duration
                        },
                        "health": {
                            "joint_back_problems": profile.joint_back_problems,
                            "chronic_conditions": profile.chronic_conditions,
                            "health_details": profile.health_details
                        },
                        "training_types": {
                            "strength_training": profile.strength_training,
                            "cardio": profile.cardio,
                            "hiit": profile.hiit,
                            "yoga_pilates": profile.yoga_pilates,
                            "functional_training": profile.functional_training,
                            "stretching": profile.stretching
                        },
                        "created_at": profile.created_at.isoformat() if profile.created_at else None,
                        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None
                    }
                else:
                    user_export["training_profile"] = None
            
            exported_data.append(user_export)
        
        return {
            "export_type": "basic" if basic else "complete",
            "export_date": datetime.utcnow().isoformat(),
            "total_users": len(exported_data),
            "users": exported_data
        }
        
    except Exception as e:
        print(f"Error exporting users: {e}")
        raise HTTPException(status_code=500, detail="Failed to export users")

@router.get("/activity")
async def get_recent_activity(
    limit: int = Query(10, description="Number of recent activities to return"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent user activity"""
    
    try:
        activities = []
        
        # Get recent user registrations
        recent_users = db.query(DBUser).order_by(DBUser.created_at.desc()).limit(limit).all()
        
        for user in recent_users:
            # User registration activity
            activities.append({
                "action": "User Registration",
                "user_email": user.email,
                "timestamp": user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat(),
                "details": f"New user {user.full_name} registered"
            })
            
            # Profile update activity if user has training profile
            profile = get_training_profile(db, user.id)
            if profile and profile.updated_at and profile.updated_at != profile.created_at:
                activities.append({
                    "action": "Profile Update",
                    "user_email": user.email,
                    "timestamp": profile.updated_at.isoformat(),
                    "details": f"User {user.full_name} updated training profile"
                })
        
        # Sort activities by timestamp (most recent first)
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return activities[:limit]
        
    except Exception as e:
        print(f"Error getting recent activity: {e}")
        return []

@router.get("/users/{user_id}")
async def get_user_details(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific user"""
    
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_details = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "training_profile": None
        }
        
        # Get training profile
        profile = get_training_profile(db, user.id)
        if profile:
            user_details["training_profile"] = {
                "basic_information": {
                    "gender": profile.gender,
                    "age": profile.age,
                    "height_cm": profile.height_cm,
                    "weight_kg": profile.weight_kg
                },
                "training_goals": profile.training_goals,
                "training_experience": {
                    "level": profile.training_level,
                    "frequency_last_3_months": profile.frequency_last_3_months
                },
                "preferences": {
                    "training_location": profile.training_location,
                    "location_details": profile.location_details,
                    "session_duration": profile.session_duration
                },
                "health": {
                    "joint_back_problems": profile.joint_back_problems,
                    "chronic_conditions": profile.chronic_conditions,
                    "health_details": profile.health_details
                },
                "training_types": {
                    "strength_training": profile.strength_training,
                    "cardio": profile.cardio,
                    "hiit": profile.hiit,
                    "yoga_pilates": profile.yoga_pilates,
                    "functional_training": profile.functional_training,
                    "stretching": profile.stretching
                },
                "created_at": profile.created_at.isoformat() if profile.created_at else None,
                "updated_at": profile.updated_at.isoformat() if profile.updated_at else None
            }
        
        # Get active sessions
        active_sessions = get_user_active_sessions(db, user.id)
        user_details["active_sessions_count"] = len(active_sessions)
        
        return user_details
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting user details: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user details")

@router.get("/users")
async def get_all_users_summary(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Number of users per page"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of all users with basic information"""
    
    try:
        from sqlalchemy import func
        
        # Get total users count
        total_users = db.query(func.count(DBUser.id)).scalar() or 0
        
        # Apply pagination
        offset = (page - 1) * limit
        users = db.query(DBUser).offset(offset).limit(limit).all()
        
        users_summary = []
        
        for user in users:
            # Check if user has training profile
            profile = get_training_profile(db, user.id)
            has_training_profile = profile is not None and profile.training_level is not None
            
            users_summary.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "has_training_profile": has_training_profile,
                "created_at": user.created_at.isoformat() if user.created_at else None
            })
        
        return {
            "users": users_summary,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_users,
                "pages": (total_users + limit - 1) // limit if total_users > 0 else 0
            }
        }
        
    except Exception as e:
        print(f"Error getting users summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get users summary")

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)"""
    
    try:
        # Check if current user is admin
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admin privileges required")
        
        # Check if user exists
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Don't allow deleting the current admin user
        if user.id == current_user["id"]:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        # Delete user (cascading will handle related records)
        db.delete(user)
        db.commit()
        
        return {"message": f"User {user.username} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user")

@router.post("/cleanup-sessions")
async def cleanup_expired_sessions_endpoint(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clean up expired sessions (admin only)"""
    
    try:
        # Check if current user is admin
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admin privileges required")
        
        cleaned_count = cleanup_expired_sessions(db)
        
        return {
            "message": f"Cleaned up {cleaned_count} expired sessions",
            "cleaned_sessions": cleaned_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error cleaning up sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to clean up sessions") 