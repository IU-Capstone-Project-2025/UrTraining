from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal, Dict
from enum import Enum
from .training import TrainerProfile

class Country(str, Enum):
    KAZAKHSTAN = "kz"
    RUSSIA = "ru"
    USA = "us"

class City(str, Enum):
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
    username: str = Field(..., min_length=3, max_length=50, description="User's unique username")
    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    country: Optional[Country] = Field(None, description="User's country")
    city: Optional[City] = Field(None, description="User's city")
    
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
    trainer_profile: Optional[TrainerProfile] = Field(None, description="Trainer profile if user is a trainer")

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
    trainer_profile: Optional[TrainerProfile] = None

class UserResponse(User):
    """Model for user response with additional fields if needed"""
    id: Optional[str] = Field(None, description="User ID (if using database)")
    created_at: Optional[str] = Field(None, description="User creation timestamp")
    updated_at: Optional[str] = Field(None, description="User last update timestamp") 