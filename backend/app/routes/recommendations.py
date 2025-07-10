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

        query_parts.append(
            f"User profile: {profile.gender}, {profile.age} years, "
            f"{profile.height_cm}cm, {profile.weight_kg}kg"
        )

        query_parts.append(f"Training goals: {', '.join(profile.training_goals)}")
        query_parts.append(
        f"{profile.training_level} level, "
        f"frequency: {profile.frequency_last_3_months} sessions/week"
        )

        preferences = [
        f"Prefers training at {profile.training_location}",
        f"Session duration: {profile.session_duration} minutes"
        ]
        if profile.location_details:
            preferences.append(f"Location details: {profile.location_details}")
        query_parts.extend(preferences)

        training_types = [
            ("strength", profile.strength_training),
            ("cardio", profile.cardio),
            ("HIIT", profile.hiit),
            ("yoga/pilates", profile.yoga_pilates),
            ("functional", profile.functional_training),
            ("stretching", profile.stretching)
        ]

        relevant_types = sorted(
            [(name, score) for name, score in training_types if score and score >= 3],
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

        health_notes = []
        if profile.joint_back_problems:
            health_notes.append("joint/back issues")
        if profile.chronic_conditions:
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

    except Exception as e:
        print(f"Error in recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate the recommendations"
        )