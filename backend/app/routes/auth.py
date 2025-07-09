from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
import re

from app.database import get_db
from app.crud import (
    authenticate_user, get_user_by_username, get_user_by_email, create_user,
    create_active_session, get_active_session, revoke_session,
    cleanup_expired_sessions, get_user_by_id, update_user_trainer_profile
)
from app.models.training import TrainerProfile

router = APIRouter()

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours = 24 * 60 minutes

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=100, description="Valid email address")
    password: str = Field(..., min_length=1, description="Password")
    
    @validator('email')
    def validate_email(cls, v):
        # Check if email is empty or whitespace only
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        
        # Remove whitespace
        v = v.strip()
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Please enter a valid email address')
        
        return v.lower()  # Convert to lowercase for consistency

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_info: dict

class LogoutResponse(BaseModel):
    message: str

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name (2-100 characters)")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    email: str = Field(..., min_length=5, max_length=100, description="Valid email address")
    
    @validator('email')
    def validate_email(cls, v):
        # Check if email is empty or whitespace only
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        
        # Remove whitespace
        v = v.strip()
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Please enter a valid email address')
        
        return v.lower()  # Convert to lowercase for consistency

class RegisterResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    expires_in: int
    user_info: dict

class UpdateTrainerProfileRequest(BaseModel):
    trainer_profile: TrainerProfile

class TrainerProfileResponse(BaseModel):
    message: str
    trainer_profile: Optional[TrainerProfile] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Clean up expired sessions periodically
        cleanup_expired_sessions(db)
        
        # Get active session from database
        session = get_active_session(db, credentials.credentials)
        if not session:
            raise credentials_exception
        
        # Get user from session
        user = get_user_by_id(db, session.user_id)
        if not user:
            raise credentials_exception
            
        # Convert user to dict format for backward compatibility
        user_dict = {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "country": user.country,
            "city": user.city,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
        
        return user_dict
        
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(f"Error in get_current_user: {e}")
        raise credentials_exception

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    """Register a new user account"""
    
    # Validate username availability
    if get_user_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    
    # Validate email availability
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        user = create_user(db, data.username, data.full_name, data.email, data.password)
        
        # Create access token (same as login)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}, 
            expires_delta=access_token_expires
        )
        
        # Store token in database (same as login)
        expires_at = datetime.utcnow() + access_token_expires
        user_agent = request.headers.get("user-agent", "")
        ip_address = request.client.host if request.client else ""
        
        create_active_session(db, user.id, access_token, expires_at, user_agent, ip_address)
        
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user_info": {
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "is_admin": user.is_admin
            }
        }
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    # Store token in database
    expires_at = datetime.utcnow() + access_token_expires
    user_agent = request.headers.get("user-agent", "")
    ip_address = request.client.host if request.client else ""
    
    create_active_session(db, user.id, access_token, expires_at, user_agent, ip_address)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user_info": {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }

@router.post("/logout", response_model=LogoutResponse)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Logout user and revoke access token"""
    try:
        revoke_session(db, credentials.credentials)
        return {"message": "Successfully logged out"}
    except Exception as e:
        print(f"Logout error: {e}")
        return {"message": "Logout completed"}

@router.get("/trainer-profile", response_model=TrainerProfileResponse)
async def get_trainer_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить профиль тренера текущего пользователя"""
    try:
        user = get_user_by_id(db, current_user["id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return TrainerProfileResponse(
            message="Trainer profile retrieved successfully",
            trainer_profile=user.trainer_profile
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting trainer profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trainer profile"
        )


@router.put("/trainer-profile", response_model=TrainerProfileResponse)
async def update_trainer_profile(
    data: UpdateTrainerProfileRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить профиль тренера текущего пользователя"""
    try:
        # Преобразуем TrainerProfile в словарь
        trainer_profile_dict = data.trainer_profile.model_dump()
        
        # Обновляем профиль тренера
        updated_user = update_user_trainer_profile(db, current_user["id"], trainer_profile_dict)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return TrainerProfileResponse(
            message="Trainer profile updated successfully",
            trainer_profile=updated_user.trainer_profile
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating trainer profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update trainer profile"
        )


@router.delete("/trainer-profile", response_model=TrainerProfileResponse)
async def delete_trainer_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить профиль тренера текущего пользователя"""
    try:
        # Удаляем профиль тренера (устанавливаем в None)
        updated_user = update_user_trainer_profile(db, current_user["id"], None)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return TrainerProfileResponse(
            message="Trainer profile deleted successfully",
            trainer_profile=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting trainer profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete trainer profile"
        )


@router.get("/validation/trainer-profile")
async def get_trainer_profile_validation():
    """Получить информацию о валидационных ограничениях для профиля тренера"""
    
    # Импортируем enums для получения допустимых значений
    from app.models.training import CertificationType, CertificationLevel, TrainerSpecialization
    
    validation_rules = {
        "profile_picture": {
            "type": "string",
            "required": False,
            "nullable": True,
            "max_length": 500,
            "format": "url",
            "supported_protocols": ["http", "https"],
            "supported_formats": ["jpg", "jpeg", "png", "webp", "gif"],
            "pattern": r"^https?://[^\s/$.?#].[^\s]*$",
            "description": "URL ссылка на фото профиля тренера",
            "example": "https://example.com/trainer-photo.jpg"
        },
        
        "certification": {
            "type": "object",
            "required": True,
            "properties": {
                "Type": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [cert_type.value for cert_type in CertificationType],
                    "description": "Тип сертификации тренера"
                },
                "Level": {
                    "type": "enum", 
                    "required": True,
                    "allowed_values": [level.value for level in CertificationLevel],
                    "description": "Уровень сертификации"
                }
            },
            "description": "Информация о сертификации тренера"
        },
        
        "experience": {
            "type": "object",
            "required": True,
            "properties": {
                "Years": {
                    "type": "integer",
                    "required": True,
                    "min_value": 0,
                    "max_value": 50,
                    "description": "Количество лет опыта в тренерской деятельности"
                },
                "Specialization": {
                    "type": "string",
                    "required": True,
                    "min_length": 2,
                    "max_length": 200,
                    "max_specializations": 5,
                    "allowed_values": [spec.value for spec in TrainerSpecialization],
                    "format": "comma_separated",
                    "pattern": r"^[a-zA-Zа-яА-Я0-9\s\-,\.]+$",
                    "description": "Специализация тренера (можно указать до 5 через запятую)",
                    "example": "Strength Training, Functional Training"
                },
                "Courses": {
                    "type": "integer",
                    "required": True,
                    "min_value": 0,
                    "max_value": 10000,
                    "description": "Количество созданных/проведенных курсов"
                },
                "Rating": {
                    "type": "float",
                    "required": True,
                    "min_value": 0.0,
                    "max_value": 5.0,
                    "decimal_places": 1,
                    "description": "Рейтинг тренера по 5-балльной шкале",
                    "cross_validation": {
                        "rule": "Если Years < 1, то Rating не должен быть > 3.0",
                        "message": "Новички не могут иметь рейтинг выше 3.0"
                    }
                }
            },
            "description": "Информация об опыте тренера"
        },
        
        "badges": {
            "type": "array",
            "required": False,
            "max_items": 20,
            "items": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "required": True,
                        "min_length": 1,
                        "max_length": 50,
                        "description": "Текст значка"
                    },
                    "color": {
                        "type": "string",
                        "required": True,
                        "format": "hex_color",
                        "pattern": r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                        "description": "Цвет значка в hex формате",
                        "example": "#FF5733"
                    }
                }
            },
            "unique_items": True,
            "uniqueness_field": "text",
            "description": "Массив значков тренера (максимум 20, без дубликатов)"
        },
        
        "reviews_count": {
            "type": "integer",
            "required": False,
            "default": 0,
            "min_value": 0,
            "max_value": 100000,
            "read_only": True,
            "description": "Количество отзывов о тренере (устанавливается системой)"
        },
        
        "bio": {
            "type": "string",
            "required": False,
            "nullable": True,
            "min_length": 10,
            "max_length": 1000,
            "content_filter": True,
            "blocked_words": ["spam", "fake", "scam"],
            "pattern": r"^[^\x00-\x1f\x7f-\x9f]*$",
            "description": "Биография тренера (краткое описание опыта и подхода)",
            "example": "Опытный тренер с 5-летним стажем, специализируюсь на силовых тренировках и функциональном тренинге."
        }
    }
    
    return {
        "message": "Validation rules for trainer profile",
        "model": "TrainerProfile",
        "validation_rules": validation_rules,
        "general_rules": {
            "encoding": "UTF-8",
            "case_sensitivity": "case_insensitive_enums",
            "cross_field_validations": [
                {
                    "fields": ["experience.Years", "experience.Rating"],
                    "rule": "Years < 1 AND Rating > 3.0 = Invalid",
                    "message": "Новички не могут иметь рейтинг выше 3.0"
                },
                {
                    "fields": ["experience.Years", "experience.Courses"], 
                    "rule": "Courses > Years * 10 = Warning",
                    "message": "Количество курсов кажется несоответствующим опыту"
                }
            ],
            "notes": [
                "Все enum значения проверяются регистронезависимо",
                "Специализации можно указывать через запятую",
                "URL изображений должны содержать поддерживаемые расширения",
                "Значки должны быть уникальными по тексту"
            ]
        }
    }


@router.get("/validation/user-profile")
async def get_user_profile_validation():
    """Получить информацию о валидационных ограничениях для профиля тренирующегося"""
    
    # Импортируем enums для получения допустимых значений
    from app.models.user import (
        Country, City, Gender, TrainingLevel, FrequencyLastThreeMonths,
        TrainingLocation, LocationDetails, SessionDuration, TrainingGoal,
        CITY_COUNTRY_MAP
    )
    
    validation_rules = {
        "personal_data": {
            "type": "object",
            "required": True,
            "properties": {
                "username": {
                    "type": "string",
                    "required": True,
                    "min_length": 3,
                    "max_length": 50,
                    "pattern": r"^[a-zA-Z0-9_-]+$",
                    "description": "Уникальное имя пользователя",
                    "example": "fitness_user123"
                },
                "full_name": {
                    "type": "string",
                    "required": True,
                    "min_length": 2,
                    "max_length": 100,
                    "pattern": r"^[a-zA-Zа-яА-Я\s\-']+$",
                    "description": "Полное имя пользователя",
                    "example": "Иван Петров"
                },
                "country": {
                    "type": "enum",
                    "required": False,
                    "nullable": True,
                    "allowed_values": [country.value for country in Country],
                    "description": "Страна проживания"
                },
                "city": {
                    "type": "enum",
                    "required": False,
                    "nullable": True,
                    "allowed_values": [city.value for city in City],
                    "description": "Город проживания",
                    "cross_validation": {
                        "rule": "Город должен соответствовать выбранной стране",
                        "mapping": CITY_COUNTRY_MAP
                    }
                }
            },
            "description": "Персональные данные пользователя"
        },
        
        "basic_information": {
            "type": "object",
            "required": True,
            "properties": {
                "gender": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [gender.value for gender in Gender],
                    "description": "Пол пользователя"
                },
                "age": {
                    "type": "integer",
                    "required": True,
                    "min_value": 13,
                    "max_value": 100,
                    "description": "Возраст в годах"
                },
                "height_cm": {
                    "type": "integer",
                    "required": True,
                    "min_value": 100,
                    "max_value": 250,
                    "description": "Рост в сантиметрах"
                },
                "weight_kg": {
                    "type": "float",
                    "required": True,
                    "min_value": 30.0,
                    "max_value": 300.0,
                    "decimal_places": 1,
                    "description": "Вес в килограммах"
                }
            },
            "description": "Базовая физическая информация"
        },
        
        "training_goals": {
            "type": "array",
            "required": True,
            "min_items": 1,
            "max_items": 5,
            "items": {
                "type": "enum",
                "allowed_values": [goal.value for goal in TrainingGoal],
                "description": "Цель тренировок"
            },
            "unique_items": True,
            "description": "Цели тренировок (от 1 до 5)",
            "examples": ["weight_loss", "muscle_gain", "improve_endurance"]
        },
        
        "training_experience": {
            "type": "object",
            "required": True,
            "properties": {
                "level": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [level.value for level in TrainingLevel],
                    "description": "Уровень подготовки"
                },
                "frequency_last_3_months": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [freq.value for freq in FrequencyLastThreeMonths],
                    "description": "Частота тренировок за последние 3 месяца"
                }
            },
            "description": "Опыт и частота тренировок"
        },
        
        "preferences": {
            "type": "object",
            "required": True,
            "properties": {
                "training_location": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [loc.value for loc in TrainingLocation],
                    "description": "Предпочитаемое место тренировок"
                },
                "location_details": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [detail.value for detail in LocationDetails],
                    "description": "Детали места тренировок"
                },
                "session_duration": {
                    "type": "enum",
                    "required": True,
                    "allowed_values": [duration.value for duration in SessionDuration],
                    "description": "Предпочитаемая продолжительность тренировки"
                }
            },
            "description": "Предпочтения по тренировкам"
        },
        
        "health": {
            "type": "object",
            "required": True,
            "properties": {
                "joint_back_problems": {
                    "type": "boolean",
                    "required": True,
                    "description": "Наличие проблем с суставами или спиной"
                },
                "chronic_conditions": {
                    "type": "boolean",
                    "required": True,
                    "description": "Наличие хронических заболеваний"
                },
                "health_details": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                    "max_length": 500,
                    "description": "Дополнительная информация о здоровье",
                    "example": "Проблемы с коленным суставом после травмы"
                }
            },
            "description": "Информация о здоровье и ограничениях"
        },
        
        "training_types": {
            "type": "object",
            "required": True,
            "properties": {
                "strength_training": {
                    "type": "integer",
                    "required": True,
                    "min_value": 1,
                    "max_value": 5,
                    "description": "Интерес к силовым тренировкам (1-5)"
                },
                "cardio": {
                    "type": "integer",
                    "required": True,
                    "min_value": 1,
                    "max_value": 5,
                    "description": "Интерес к кардио тренировкам (1-5)"
                },
                "hiit": {
                    "type": "integer",
                    "required": True,
                    "min_value": 1,
                    "max_value": 5,
                    "description": "Интерес к HIIT тренировкам (1-5)"
                },
                "yoga_pilates": {
                    "type": "integer",
                    "required": True,
                    "min_value": 1,
                    "max_value": 5,
                    "description": "Интерес к йоге/пилатесу (1-5)"
                },
                "functional_training": {
                    "type": "integer",
                    "required": True,
                    "min_value": 1,
                    "max_value": 5,
                    "description": "Интерес к функциональным тренировкам (1-5)"
                },
                "stretching": {
                    "type": "integer",
                    "required": True,
                    "min_value": 1,
                    "max_value": 5,
                    "description": "Интерес к растяжке (1-5)"
                }
            },
            "description": "Уровень интереса к различным типам тренировок"
        },
        
        "trainer_profile": {
            "type": "object",
            "required": False,
            "nullable": True,
            "description": "Профиль тренера (если пользователь является тренером)",
            "properties": {
                "message": "Для валидации профиля тренера используйте GET /auth/validation/trainer-profile"
            }
        }
    }
    
    return {
        "message": "Validation rules for user profile",
        "model": "User",
        "validation_rules": validation_rules,
        "general_rules": {
            "encoding": "UTF-8",
            "case_sensitivity": "case_insensitive_enums",
            "cross_field_validations": [
                {
                    "fields": ["personal_data.city", "personal_data.country"],
                    "rule": "Город должен соответствовать стране",
                    "message": "Выберите город из указанной страны или измените страну"
                },
                {
                    "fields": ["basic_information.age", "basic_information.weight_kg", "basic_information.height_cm"],
                    "rule": "BMI = weight_kg / (height_cm/100)^2 должен быть в разумных пределах",
                    "message": "Проверьте корректность введенных данных о росте и весе"
                },
                {
                    "fields": ["training_experience.level", "training_experience.frequency_last_3_months"],
                    "rule": "Продвинутый уровень должен соответствовать регулярным тренировкам",
                    "message": "Уровень подготовки должен соответствовать частоте тренировок"
                }
            ],
            "validation_order": [
                "personal_data",
                "basic_information", 
                "training_goals",
                "training_experience",
                "preferences",
                "health",
                "training_types",
                "trainer_profile"
            ],
            "required_for_recommendations": [
                "basic_information.gender",
                "basic_information.age", 
                "training_experience.level",
                "training_types"
            ],
            "notes": [
                "Все enum значения проверяются регистронезависимо",
                "Цели тренировок могут быть выбраны в количестве от 1 до 5",
                "Город автоматически валидируется на соответствие стране",
                "Типы тренировок оцениваются по шкале от 1 до 5",
                "Профиль тренера опционален и валидируется отдельно"
            ]
        }
    }