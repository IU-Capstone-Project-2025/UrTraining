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
    TrainingGoal
)
from .training import (
    Training as TrainingModel,
    TrainingCreate,
    TrainingUpdate,
    TrainingResponse,
    Badge,
    HeaderBadges,
    CourseInfo,
    Exercise,
    TrainingDay,
    CoachData,
    TrainingMetadata,
    TrainerCertification,
    TrainerExperience,
    TrainerProfile
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
    
    # Pydantic models for Training
    "TrainingModel",
    "TrainingCreate",
    "TrainingUpdate",
    "TrainingResponse",
    "Badge",
    "HeaderBadges",
    "CourseInfo",
    "Exercise",
    "TrainingDay",
    "CoachData",
    "TrainingMetadata",
    "TrainerCertification",
    "TrainerExperience",
    "TrainerProfile"
] 