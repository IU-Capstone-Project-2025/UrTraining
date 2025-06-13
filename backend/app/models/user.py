from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class TrainingLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class FrequencyLastThreeMonths(str, Enum):
    NOT_TRAINED = "not_trained"
    ONE_TWO_TIMES_WEEK = "1_2_times_week"
    THREE_FOUR_TIMES_WEEK = "3_4_times_week"
    FIVE_SIX_TIMES_WEEK = "5_6_times_week"
    DAILY = "daily"

class TrainingLocation(str, Enum):
    GYM = "gym"
    HOME = "home"
    OUTDOOR = "outdoor"
    MIXED = "mixed"

class LocationDetails(str, Enum):
    FULL_FITNESS_CENTER = "full_fitness_center"
    BASIC_GYM = "basic_gym"
    HOME_EQUIPMENT = "home_equipment"
    NO_EQUIPMENT = "no_equipment"
    PARK_OUTDOOR = "park_outdoor"

class SessionDuration(str, Enum):
    FIFTEEN_THIRTY_MIN = "15_30_min"
    THIRTY_FOURTY_FIVE_MIN = "30_45_min"
    FOURTY_FIVE_SIXTY_MIN = "45_60_min"
    SIXTY_NINETY_MIN = "60_90_min"
    MORE_THAN_NINETY_MIN = "90+_min"

class TrainingGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTAIN_FITNESS = "maintain_fitness"
    IMPROVE_ENDURANCE = "improve_endurance"
    IMPROVE_FLEXIBILITY = "improve_flexibility"
    COMPETITION_PREPARATION = "competition_preparation"
    STRENGTH_BUILDING = "strength_building"
    REHABILITATION = "rehabilitation"

class PersonalData(BaseModel):
    full_name: str = Field(..., description="User's full name")

class BasicInformation(BaseModel):
    gender: Gender = Field(..., description="User's gender")
    age: int = Field(..., ge=13, le=100, description="User's age in years")
    height_cm: int = Field(..., ge=100, le=250, description="User's height in centimeters")
    weight_kg: float = Field(..., ge=30, le=300, description="User's weight in kilograms")

class TrainingExperience(BaseModel):
    level: TrainingLevel = Field(..., description="User's training experience level")
    frequency_last_3_months: FrequencyLastThreeMonths = Field(..., description="Training frequency in the last 3 months")

class Preferences(BaseModel):
    training_location: TrainingLocation = Field(..., description="Preferred training location")
    location_details: LocationDetails = Field(..., description="Details about the training location")
    session_duration: SessionDuration = Field(..., description="Preferred session duration")

class Health(BaseModel):
    joint_back_problems: bool = Field(..., description="Whether user has joint or back problems")
    chronic_conditions: bool = Field(..., description="Whether user has chronic health conditions")
    health_details: Optional[str] = Field(None, description="Additional health information or restrictions")

class TrainingTypes(BaseModel):
    strength_training: int = Field(..., ge=1, le=5, description="Interest level in strength training (1-5)")
    cardio: int = Field(..., ge=1, le=5, description="Interest level in cardio training (1-5)")
    hiit: int = Field(..., ge=1, le=5, description="Interest level in HIIT training (1-5)")
    yoga_pilates: int = Field(..., ge=1, le=5, description="Interest level in yoga/pilates (1-5)")
    functional_training: int = Field(..., ge=1, le=5, description="Interest level in functional training (1-5)")
    stretching: int = Field(..., ge=1, le=5, description="Interest level in stretching (1-5)")

class User(BaseModel):
    """
    User model representing a complete user profile for training recommendations.
    Based on the structure from gemma_profiles.json.
    """
    personal_data: PersonalData = Field(..., description="User's personal information")
    basic_information: BasicInformation = Field(..., description="User's basic physical information")
    training_goals: List[TrainingGoal] = Field(..., min_items=1, max_items=5, description="User's training goals")
    training_experience: TrainingExperience = Field(..., description="User's training experience and frequency")
    preferences: Preferences = Field(..., description="User's training preferences")
    health: Health = Field(..., description="User's health status and restrictions")
    training_types: TrainingTypes = Field(..., description="User's interest levels in different training types")

    class Config:
        use_enum_values = True
        json_encoders = {
            # Custom encoders if needed
        }

# Additional models for API operations
class UserCreate(User):
    """Model for creating a new user"""
    pass

class UserUpdate(BaseModel):
    """Model for updating user information - all fields optional"""
    personal_data: Optional[PersonalData] = None
    basic_information: Optional[BasicInformation] = None
    training_goals: Optional[List[TrainingGoal]] = None
    training_experience: Optional[TrainingExperience] = None
    preferences: Optional[Preferences] = None
    health: Optional[Health] = None
    training_types: Optional[TrainingTypes] = None

class UserResponse(User):
    """Model for user response with additional fields if needed"""
    id: Optional[str] = Field(None, description="User ID (if using database)")
    created_at: Optional[str] = Field(None, description="User creation timestamp")
    updated_at: Optional[str] = Field(None, description="User last update timestamp") 