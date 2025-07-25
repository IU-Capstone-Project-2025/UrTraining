from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router, get_current_user
from app.routes.trainings import router as trainings_router
from app.routes.recommendations import router as recommendations_router
from app.routes.saved_programs import router as saved_programs_router
from app.routes.progress import router as progress_router
from app.routes.tracker import router as tracker_router
from app.database import get_db
from app.crud import get_training_profile, update_user_profile, update_training_profile, get_user_by_id
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from enum import Enum
import json
import os

# Database imports
from app.database import engine
from app.models.database_models import Base

# Enums for validation
class CountryEnum(str, Enum):
    kz = "kz"
    ru = "ru"
    us = "us"

class CityEnum(str, Enum):
    # Kazakhstan cities
    ALMATY = "Almaty"
    ASTANA = "Nur-Sultan"
    SHYMKENT = "Shymkent"
    AKTOBE = "Aktobe"
    TARAZ = "Taraz"
    
    # Russia cities
    MOSCOW = "Moscow"
    SAINT_PETERSBURG = "Saint Petersburg"
    KAZAN = "Kazan"
    INNOPOLIS = "Innopolis"
    NOVOSIBIRSK = "Novosibirsk"
    YEKATERINBURG = "Yekaterinburg"
    NIZHNY_NOVGOROD = "Nizhny Novgorod"
    ROSTOV_ON_DON = "Rostov-on-Don"
    
    # United States cities
    NEW_YORK = "New York"
    LOS_ANGELES = "Los Angeles"
    CHICAGO = "Chicago"
    HOUSTON = "Houston"
    PHOENIX = "Phoenix"
    PHILADELPHIA = "Philadelphia"
    SAN_ANTONIO = "San Antonio"
    SAN_DIEGO = "San Diego"
    DALLAS = "Dallas"
    SAN_FRANCISCO = "San Francisco"

# City-to-country mapping for validation
CITY_COUNTRY_MAP: Dict[str, str] = {
    # Kazakhstan
    "Almaty": "kz",
    "Nur-Sultan": "kz", 
    "Shymkent": "kz",
    "Aktobe": "kz",
    "Taraz": "kz",
    
    # Russia
    "Moscow": "ru",
    "Saint Petersburg": "ru",
    "Kazan": "ru",
    "Innopolis": "ru", 
    "Novosibirsk": "ru",
    "Yekaterinburg": "ru",
    "Nizhny Novgorod": "ru",
    "Rostov-on-Don": "ru",
    
    # United States
    "New York": "us",
    "Los Angeles": "us",
    "Chicago": "us",
    "Houston": "us",
    "Phoenix": "us",
    "Philadelphia": "us",
    "San Antonio": "us",
    "San Diego": "us",
    "Dallas": "us",
    "San Francisco": "us",
}

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class TrainingLevelEnum(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class FrequencyEnum(str, Enum):
    one_two_times = "1_2_times_week"
    three_four_times = "3_4_times_week"
    five_plus_times = "5+_times_week"
    not_trained = "not_trained"

class TrainingLocationEnum(str, Enum):
    gym = "gym"
    outdoors = "outdoors"
    pool = "pool"
    home = "home"

class LocationDetailsEnum(str, Enum):
    full_equipment = "full_equipment"
    basic_equipment = "basic_equipment"
    no_equipment = "no_equipment"
    outdoor_park = "outdoor_park"
    running_track = "running_track"
    swimming_pool = "swimming_pool"
    home_gym = "home_gym"
    bodyweight_only = "bodyweight_only"

class SessionDurationEnum(str, Enum):
    under_30_min = "under_30_min"
    thirty_45_min = "30_45_min"
    fourty5_60_min = "45_60_min"
    over_60_min = "over_60_min"

class TrainingGoalEnum(str, Enum):
    muscle_gain = "muscle_gain"
    maintain_fitness = "maintain_fitness"
    weight_loss = "weight_loss"
    improve_endurance = "improve_endurance"
    improve_flexibility = "improve_flexibility"
    stress_reduction = "stress_reduction"
    competitions_preparation = "competitions_preparation"
    none = "none"

# Pydantic models for user data update
class BasicInformation(BaseModel):
    gender: Optional[GenderEnum] = None
    age: Optional[int] = Field(None, ge=13, le=100)
    height_cm: Optional[int] = Field(None, ge=100, le=250)
    weight_kg: Optional[float] = Field(None, ge=30, le=300)

class TrainingExperience(BaseModel):
    level: Optional[TrainingLevelEnum] = None
    frequency_last_3_months: Optional[FrequencyEnum] = None

class Preferences(BaseModel):
    training_location: Optional[TrainingLocationEnum] = None
    location_details: Optional[LocationDetailsEnum] = None
    session_duration: Optional[SessionDurationEnum] = None

class Health(BaseModel):
    joint_back_problems: Optional[bool] = None
    chronic_conditions: Optional[bool] = None
    health_details: Optional[str] = Field(None, max_length=1000)

class TrainingTypes(BaseModel):
    strength_training: Optional[int] = Field(None, ge=1, le=5)
    cardio: Optional[int] = Field(None, ge=1, le=5)
    hiit: Optional[int] = Field(None, ge=1, le=5)
    yoga_pilates: Optional[int] = Field(None, ge=1, le=5)
    functional_training: Optional[int] = Field(None, ge=1, le=5)
    stretching: Optional[int] = Field(None, ge=1, le=5)

class TrainingProfileUpdate(BaseModel):
    basic_information: Optional[BasicInformation] = None
    training_goals: Optional[List[TrainingGoalEnum]] = Field(None, max_items=2)
    training_experience: Optional[TrainingExperience] = None
    preferences: Optional[Preferences] = None
    health: Optional[Health] = None
    training_types: Optional[TrainingTypes] = None

class UserDataUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    country: Optional[CountryEnum] = None
    city: Optional[CityEnum] = None
    training_profile: Optional[TrainingProfileUpdate] = None
    
    @validator('city')
    def validate_city_country_match(cls, city, values):
        """Validate that city belongs to the specified country"""
        if city is None:
            return city
            
        country = values.get('country')
        if country is None:
            # If no country specified, city can be any valid city
            return city
            
        # Check if city belongs to the specified country
        expected_country = CITY_COUNTRY_MAP.get(city)
        if expected_country and expected_country != country:
            city_name = city
            country_name = country
            
            # Get readable country names
            country_names = {"kz": "Kazakhstan", "ru": "Russia", "us": "United States"}
            country_display = country_names.get(country, country)
            expected_country_display = country_names.get(expected_country, expected_country)
            
            raise ValueError(
                f"City '{city_name}' belongs to {expected_country_display}, "
                f"but country is set to {country_display}. "
                f"Please choose a city from {country_display} or change the country."
            )
        
        return city

app = FastAPI(
    title="UrTraining Backend API",
    description="A comprehensive training platform API for fitness courses and user management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Error creating database tables: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FRONTEND DOMEN!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(trainings_router, prefix="/trainings", tags=["Trainings"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(saved_programs_router, prefix="/saved-programs", tags=["Saved Programs"])
app.include_router(progress_router, prefix="/progress", tags=["Training Progress"])
app.include_router(tracker_router, prefix="/tracker", tags=["Training Tracker"])


@app.get("/survey-data")
def get_survey_data():
    """Return survey data from JSON file"""
    try:
        file_path = "data/survey_data.json"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Survey data file not found")
        
        with open(file_path, "r", encoding="utf-8") as file:
            survey_data = json.load(file)
        
        return survey_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in survey data file")
    except Exception as e:
        print(f"Error reading survey data: {e}")
        raise HTTPException(status_code=500, detail="Failed to load survey data")
    

@app.get("/trainer-survey-data")
def get_survey_data():
    """Return authentication data for coach from JSON file"""
    try:
        file_path = "data/coach_auth_data.json"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Coach auth data file not found")
        
        with open(file_path, "r", encoding="utf-8") as file:
            survey_data = json.load(file)
        
        return survey_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in coach auth data file")
    except Exception as e:
        print(f"Error reading coach auth data: {e}")
        raise HTTPException(status_code=500, detail="Failed to load coach auth data")


@app.get("/user-data")
def get_user_data(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all user data including profile and training information"""
    try:
        # Get basic user information (already available in current_user)
        user_data = {
            "id": current_user["id"],
            "username": current_user["username"],
            "full_name": current_user["full_name"],
            "email": current_user["email"],
            "country": current_user.get("country"),
            "city": current_user.get("city"),
            "is_admin": current_user["is_admin"],
            "created_at": current_user["created_at"],
            "updated_at": current_user["updated_at"]
        }
        
        # Get trainer profile
        user = get_user_by_id(db, current_user["id"])
        if user and user.trainer_profile:
            user_data["trainer_profile"] = user.trainer_profile
        else:
            user_data["trainer_profile"] = None
        
        # Get training profile
        profile = get_training_profile(db, current_user["id"])
        if profile:
            user_data["training_profile"] = {
                "basic_information": {
                    "gender": profile.gender,
                    "age": profile.age,
                    "height_cm": profile.height_cm,
                    "weight_kg": profile.weight_kg
                },
                "training_goals": profile.training_goals or [],
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
            user_data["training_profile"] = None
        
        return user_data
        
    except Exception as e:
        print(f"Error getting user data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user data")

@app.post("/user-data")
def update_user_data(
    data: UserDataUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update all user data including profile and training information"""
    try:
        updated_user = None
        
        # Update basic user information if provided
        if data.username is not None or data.full_name is not None or data.email is not None or data.country is not None or data.city is not None:
            # Check if new email is already taken by another user
            if data.email and data.email != current_user["email"]:
                from app.crud import get_user_by_email
                existing_user = get_user_by_email(db, data.email)
                if existing_user and existing_user.id != current_user["id"]:
                    raise HTTPException(
                        status_code=400,
                        detail="Email already registered by another user"
                    )
            
            # Check if new username is already taken by another user
            if data.username and data.username != current_user["username"]:
                from app.crud import get_user_by_username
                existing_user = get_user_by_username(db, data.username)
                if existing_user and existing_user.id != current_user["id"]:
                    raise HTTPException(
                        status_code=400,
                        detail="Username already taken by another user"
                    )
            
            updated_user = update_user_profile(
                db, 
                current_user["id"], 
                data.username, 
                data.full_name,
                data.email,
                data.country.value if data.country else None,
                data.city.value if data.city else None
            )
            
            if not updated_user:
                raise HTTPException(status_code=404, detail="User not found")
        
        # Update training profile if provided
        if data.training_profile:
            profile_data = {}
            
            # Basic information
            if data.training_profile.basic_information:
                basic = data.training_profile.basic_information
                if basic.gender is not None:
                    profile_data["gender"] = basic.gender.value
                if basic.age is not None:
                    profile_data["age"] = basic.age
                if basic.height_cm is not None:
                    profile_data["height_cm"] = basic.height_cm
                if basic.weight_kg is not None:
                    profile_data["weight_kg"] = basic.weight_kg
            
            # Training goals
            if data.training_profile.training_goals is not None:
                profile_data["training_goals"] = [goal.value for goal in data.training_profile.training_goals]
            
            # Training experience
            if data.training_profile.training_experience:
                exp = data.training_profile.training_experience
                if exp.level is not None:
                    profile_data["training_level"] = exp.level.value
                if exp.frequency_last_3_months is not None:
                    profile_data["frequency_last_3_months"] = exp.frequency_last_3_months.value
            
            # Preferences
            if data.training_profile.preferences:
                pref = data.training_profile.preferences
                if pref.training_location is not None:
                    profile_data["training_location"] = pref.training_location.value
                if pref.location_details is not None:
                    profile_data["location_details"] = pref.location_details.value
                if pref.session_duration is not None:
                    profile_data["session_duration"] = pref.session_duration.value
            
            # Health
            if data.training_profile.health:
                health = data.training_profile.health
                if health.joint_back_problems is not None:
                    profile_data["joint_back_problems"] = health.joint_back_problems
                if health.chronic_conditions is not None:
                    profile_data["chronic_conditions"] = health.chronic_conditions
                if health.health_details is not None:
                    profile_data["health_details"] = health.health_details
            
            # Training types
            if data.training_profile.training_types:
                types = data.training_profile.training_types
                if types.strength_training is not None:
                    profile_data["strength_training"] = types.strength_training
                if types.cardio is not None:
                    profile_data["cardio"] = types.cardio
                if types.hiit is not None:
                    profile_data["hiit"] = types.hiit
                if types.yoga_pilates is not None:
                    profile_data["yoga_pilates"] = types.yoga_pilates
                if types.functional_training is not None:
                    profile_data["functional_training"] = types.functional_training
                if types.stretching is not None:
                    profile_data["stretching"] = types.stretching
            
            # Update training profile if there's data to update
            if profile_data:
                updated_profile = update_training_profile(db, current_user["id"], profile_data)
                if not updated_profile:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to update training profile"
                    )
        
        # Return success response
        return {
            "message": "User data updated successfully",
            "updated_fields": {
                "user_profile": bool(data.username is not None or data.full_name is not None or data.email is not None or data.country is not None or data.city is not None),
                "training_profile": bool(data.training_profile is not None)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating user data for user {current_user['id']}")
        raise HTTPException(status_code=500, detail="Failed to update user data")

@app.put("/user-data")
def put_user_data(
    data: UserDataUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user data including profile and training information (PUT method)"""
    try:
        updated_user = None
        
        # Update basic user information if provided
        if data.username is not None or data.full_name is not None or data.email is not None or data.country is not None or data.city is not None:
            updated_user = update_user_profile(
                db, 
                current_user["id"], 
                data.username, 
                data.full_name,
                data.email,
                data.country.value if data.country else None,
                data.city.value if data.city else None
            )
            
            if not updated_user:
                raise HTTPException(status_code=404, detail="User not found")
        
        # Update training profile if provided
        if data.training_profile:
            profile_data = {}
            
            # Basic information
            if data.training_profile.basic_information:
                basic = data.training_profile.basic_information
                if basic.gender is not None:
                    profile_data["gender"] = basic.gender.value
                if basic.age is not None:
                    profile_data["age"] = basic.age
                if basic.height_cm is not None:
                    profile_data["height_cm"] = basic.height_cm
                if basic.weight_kg is not None:
                    profile_data["weight_kg"] = basic.weight_kg
            
            # Training goals
            if data.training_profile.training_goals is not None:
                profile_data["training_goals"] = [goal.value for goal in data.training_profile.training_goals]
            
            # Training experience
            if data.training_profile.training_experience:
                exp = data.training_profile.training_experience
                if exp.level is not None:
                    profile_data["training_level"] = exp.level.value
                if exp.frequency_last_3_months is not None:
                    profile_data["frequency_last_3_months"] = exp.frequency_last_3_months.value
            
            # Preferences
            if data.training_profile.preferences:
                pref = data.training_profile.preferences
                if pref.training_location is not None:
                    profile_data["training_location"] = pref.training_location.value
                if pref.location_details is not None:
                    profile_data["location_details"] = pref.location_details.value
                if pref.session_duration is not None:
                    profile_data["session_duration"] = pref.session_duration.value
            
            # Health
            if data.training_profile.health:
                health = data.training_profile.health
                if health.joint_back_problems is not None:
                    profile_data["joint_back_problems"] = health.joint_back_problems
                if health.chronic_conditions is not None:
                    profile_data["chronic_conditions"] = health.chronic_conditions
                if health.health_details is not None:
                    profile_data["health_details"] = health.health_details
            
            # Training types
            if data.training_profile.training_types:
                types = data.training_profile.training_types
                if types.strength_training is not None:
                    profile_data["strength_training"] = types.strength_training
                if types.cardio is not None:
                    profile_data["cardio"] = types.cardio
                if types.hiit is not None:
                    profile_data["hiit"] = types.hiit
                if types.yoga_pilates is not None:
                    profile_data["yoga_pilates"] = types.yoga_pilates
                if types.functional_training is not None:
                    profile_data["functional_training"] = types.functional_training
                if types.stretching is not None:
                    profile_data["stretching"] = types.stretching
            
            # Update training profile if there's data to update
            if profile_data:
                updated_profile = update_training_profile(db, current_user["id"], profile_data)
                if not updated_profile:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to update training profile"
                    )
        
        # Commit changes
        db.commit()
        
        # Return success response
        return {
            "message": "User data updated successfully",
            "updated_fields": {
                "user_profile": bool(data.username is not None or data.full_name is not None or data.email is not None or data.country is not None or data.city is not None),
                "training_profile": bool(data.training_profile is not None)
            }
        }
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower() if hasattr(e, 'orig') else str(e).lower()
        if "email" in error_msg and "unique" in error_msg:
            raise HTTPException(
                status_code=400,
                detail="Email already registered by another user"
            )
        elif "username" in error_msg and "unique" in error_msg:
            raise HTTPException(
                status_code=400,
                detail="Username already taken by another user"
            )
        else:
            print(f"Database integrity error for user {current_user['id']}: {e}")
            raise HTTPException(status_code=400, detail="Data validation error")
    except Exception as e:
        db.rollback()
        print(f"Error updating user data for user {current_user['id']}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user data")