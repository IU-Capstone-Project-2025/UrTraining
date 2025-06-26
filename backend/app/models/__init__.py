from .database_models import User, TrainingProfile, ActiveSession, Course, UserCourseProgress, Training
from .user import (
    User as UserModel, 
    UserCreate, 
    UserUpdate, 
    UserResponse,
    Gender,
    TrainingLevel,
    FrequencyLastThreeMonths,
    TrainingLocation,
    LocationDetails,
    SessionDuration,
    TrainingGoal,
    PersonalData,
    BasicInformation,
    TrainingExperience,
    Preferences,
    Health,
    TrainingTypes,
    Country,
    City,
    CITY_COUNTRY_MAP
)
from .training import (
    Training as TrainingModel,
    TrainingCreate,
    TrainingUpdate,
    TrainingResponse,
    Certification,
    Experience,
    Exercise,
    TrainingDay,
    TrainerProfile,
    # Legacy models for backward compatibility
    Badge,
    HeaderBadges,
    CourseInfo,
    CoachData,
    TrainingMetadata,
    LegacyTraining,
    # Aliases for backward compatibility
    TrainerCertification,
    TrainerExperience
)

__all__ = [
    # Database models
    "User",
    "TrainingProfile", 
    "ActiveSession",
    "Course",
    "UserCourseProgress",
    "Training",
    
    # Pydantic models for User
    "UserModel",
    "UserCreate",
    "UserUpdate", 
    "UserResponse",
    "Gender",
    "TrainingLevel",
    "FrequencyLastThreeMonths",
    "TrainingLocation",
    "LocationDetails",
    "SessionDuration",
    "TrainingGoal",
    "PersonalData",
    "BasicInformation",
    "TrainingExperience",
    "Preferences",
    "Health",
    "TrainingTypes",
    "Country",
    "City",
    "CITY_COUNTRY_MAP",
    
    # New Training models
    "TrainingModel",
    "TrainingCreate",
    "TrainingUpdate",
    "TrainingResponse",
    "Certification",
    "Experience",
    "Exercise",
    "TrainingDay",
    "TrainerProfile",
    
    # Legacy Training models (deprecated)
    "Badge",
    "HeaderBadges",
    "CourseInfo",
    "CoachData",
    "TrainingMetadata",
    "LegacyTraining",
    "TrainerCertification",
    "TrainerExperience"
] 