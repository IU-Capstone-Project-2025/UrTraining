from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import requests
from app.routes.trainings import get_training_details

from app.database import get_db
from app.crud import (
    get_training_by_id, 
    get_trainings_summary, 
    get_trainings_by_user,
    delete_training,
    search_trainings,
    get_training_with_trainer_info,
    get_user_by_id,
    get_training_profile
)
from app.models.training import (
    TrainingResponse
)
from app.routes.auth import get_current_user

router = APIRouter()

def _validate_profile_completeness(profile):
    """Check if profile has minimum required fields for recommendations"""
    # Only check critical fields needed for basic recommendations
    critical_fields = {
        'basic_info': ['gender', 'age'],
        'training_data': ['training_level']
    }
    
    missing_critical_fields = []
    
    for category, fields in critical_fields.items():
        for field in fields:
            value = getattr(profile, field, None)
            if value is None or (isinstance(value, list) and len(value) == 0):
                missing_critical_fields.append(field)
    
    # Check if at least one training type preference is set
    training_type_fields = ['strength_training', 'cardio', 'hiit', 'yoga_pilates', 'functional_training', 'stretching']
    has_training_preference = any(
        getattr(profile, field, None) is not None and getattr(profile, field, 0) > 0 
        for field in training_type_fields
    )
    
    if not has_training_preference:
        missing_critical_fields.append('training_type_preferences')
    
    return missing_critical_fields

@router.get("/")
async def get_user_recommendations(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get the recommendations for user considering all the training profile information"""
    try:
        # Get training profile
        print("ye")

        profile = get_training_profile(db, current_user["id"])
        print(profile)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Training profile not found"
            )
        
        # Prepare structured query with interest scores
        query_parts = []

        # Safe access to profile fields with None checks
        gender = profile.gender or "not specified"
        age = profile.age if profile.age is not None else "not specified"
        height = profile.height_cm if profile.height_cm is not None else "not specified"
        weight = profile.weight_kg if profile.weight_kg is not None else "not specified"
        
        query_parts.append(
            f"User profile: {gender}, {age} years, {height}cm, {weight}kg"
        )

        # Handle training goals safely
        training_goals = profile.training_goals if profile.training_goals else []
        if training_goals:
            query_parts.append(f"Training goals: {', '.join(training_goals)}")
        else:
            query_parts.append("Training goals: general fitness")

        # Handle training experience safely
        training_level = profile.training_level or "beginner"
        frequency = profile.frequency_last_3_months or "not specified"
        query_parts.append(f"{training_level} level, frequency: {frequency}")

        # Handle preferences safely
        training_location = profile.training_location or "any location"
        session_duration = profile.session_duration or "flexible duration"
        
        preferences = [
            f"Prefers training at {training_location}",
            f"Session duration: {session_duration}"
        ]
        if profile.location_details:
            preferences.append(f"Location details: {profile.location_details}")
        query_parts.extend(preferences)

        # Handle training types safely
        training_types = [
            ("strength", getattr(profile, 'strength_training', None)),
            ("cardio", getattr(profile, 'cardio', None)),
            ("HIIT", getattr(profile, 'hiit', None)),
            ("yoga/pilates", getattr(profile, 'yoga_pilates', None)),
            ("functional", getattr(profile, 'functional_training', None)),
            ("stretching", getattr(profile, 'stretching', None))
        ]

        relevant_types = sorted(
            [(name, score) for name, score in training_types if score is not None and score >= 3],
            key=lambda x: x[1],
            reverse=True
        )

        if relevant_types:
            types_text = ", ".join(
                [f"{name} ({score}/5)" for name, score in relevant_types]
            )
            query_parts.append(f"Preferred activities: {types_text}")
        else:
            query_parts.append("No strong preferences in training types")

        # Handle health information safely
        health_notes = []
        if getattr(profile, 'joint_back_problems', False):
            health_notes.append("joint/back issues")
        if getattr(profile, 'chronic_conditions', False):
            health_notes.append("chronic conditions")
        if health_notes:
            query_parts.append(f"Health notes: {', '.join(health_notes)}")

        query_text = ".\n".join(query_parts) + "."

        
        search_url = "http://31.129.96.182:1337/search_index"
        payload = {
            "index_name": "bm25_index",
            "query_text": query_text,
            "k": 5,  # Get top 5 recommendations
            "nprobe": 1
        }

        response = requests.post(
            search_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Vector search service unavailable"
            )
        
        search_results = response.json()
        if not search_results.get("success"):
            raise HTTPException(
                status_code=500,
                detail="Vector search failed"
            )
        
        # 5. Extract just the IDs from results
        recommended_ids = [result["id"] for result in search_results["results"]]

        recommended_trainings = []

        for training_id in recommended_ids:
            try:
                training = await get_training_details(training_id=training_id, db=db)
                recommended_trainings.append(training)
            except HTTPException as e:
                print(f"Failed to fetch training {training_id}: {e.detail}")
                continue

        return {
            "success": True,
            "count": len(recommended_trainings),
            "recommendations": recommended_trainings,
            "query_used": query_text
        }  

    except HTTPException:
        # Re-raise HTTP exceptions (400 errors from profile validation)
        raise
    except requests.exceptions.RequestException as e:
        print(f"Vector search service error for user {current_user['id']}: {e}")
        raise HTTPException(
            status_code=503,
            detail="Recommendation service temporarily unavailable. Please try again later."
        )
    except Exception as e:
        print(f"Unexpected error in recommendations for user {current_user['id']}: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate the recommendations"
        )