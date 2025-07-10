from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
import re
import uuid

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
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    
    # Добавляем случайный UUID и микросекунды для обеспечения уникальности токена
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow().timestamp(),  # Время создания с микросекундами
        "jti": str(uuid.uuid4())  # Уникальный идентификатор токена
    })
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
        
        # Очищаем возможные старые сессии (для безопасности)
        from app.crud import revoke_user_sessions
        revoke_user_sessions(db, user.id)
        
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
    
    # Очищаем старые активные сессии пользователя
    from app.crud import revoke_user_sessions
    revoke_user_sessions(db, user.id)
    
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