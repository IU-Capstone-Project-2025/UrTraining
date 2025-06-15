from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import (
    authenticate_user, get_user_by_username, get_user_by_email, create_user,
    create_active_session, get_active_session, revoke_session, get_user_active_sessions,
    update_user_profile, change_user_password, get_training_profile, update_training_profile,
    cleanup_expired_sessions, get_user_by_id
)

router = APIRouter()

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_info: dict

class LogoutResponse(BaseModel):
    message: str

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    email: str = Field(..., description="Valid email address")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name (2-100 characters)")

class RegisterResponse(BaseModel):
    message: str
    user_info: dict

class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Full name (2-100 characters)")
    email: Optional[str] = Field(None, description="Valid email address")

class TrainingProfileUpdate(BaseModel):
    # Basic Information
    gender: Optional[str] = Field(None, description="Gender (male/female)")
    age: Optional[int] = Field(None, ge=13, le=100, description="Age in years")
    height_cm: Optional[int] = Field(None, ge=100, le=250, description="Height in centimeters")
    weight_kg: Optional[float] = Field(None, ge=30, le=300, description="Weight in kilograms")
    
    # Training Goals
    training_goals: Optional[List[str]] = Field(None, description="Training goals")
    
    # Training Experience
    training_level: Optional[str] = Field(None, description="Training experience level")
    frequency_last_3_months: Optional[str] = Field(None, description="Training frequency")
    
    # Preferences
    training_location: Optional[str] = Field(None, description="Preferred training location")
    location_details: Optional[str] = Field(None, description="Training location details")
    session_duration: Optional[str] = Field(None, description="Preferred session duration")
    
    # Health
    joint_back_problems: Optional[bool] = Field(None, description="Joint or back problems")
    chronic_conditions: Optional[bool] = Field(None, description="Chronic health conditions")
    health_details: Optional[str] = Field(None, description="Health details")
    
    # Training Types (1-5 scale)
    strength_training: Optional[int] = Field(None, ge=1, le=5, description="Interest in strength training")
    cardio: Optional[int] = Field(None, ge=1, le=5, description="Interest in cardio")
    hiit: Optional[int] = Field(None, ge=1, le=5, description="Interest in HIIT")
    yoga_pilates: Optional[int] = Field(None, ge=1, le=5, description="Interest in yoga/pilates")
    functional_training: Optional[int] = Field(None, ge=1, le=5, description="Interest in functional training")
    stretching: Optional[int] = Field(None, ge=1, le=5, description="Interest in stretching")

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (minimum 6 characters)")

class UpdateProfileResponse(BaseModel):
    message: str
    user_info: dict

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
            "email": user.email,
            "full_name": user.full_name,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
        
        # Add training profile if exists
        profile = get_training_profile(db, user.id)
        if profile:
            user_dict["training_profile"] = {
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
                }
            }
        
        return user_dict
        
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(f"Error in get_current_user: {e}")
        raise credentials_exception

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account"""
    
    # Validate username availability
    if get_user_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Validate email availability
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        user = create_user(db, data.username, data.email, data.password, data.full_name)
        return {
            "message": "User registered successfully",
            "user_info": {
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
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
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}, 
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
            "email": user.email,
            "full_name": user.full_name,
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

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "user_info": current_user
    }

@router.get("/verify-token")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """Verify if the current token is valid"""
    return {"valid": True, "username": current_user["username"]}

@router.get("/active-sessions")
async def get_active_sessions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all active sessions for the current user"""
    try:
        sessions = get_user_active_sessions(db, current_user["id"])
        session_list = []
        for session in sessions:
            session_list.append({
                "token": session.token[:10] + "...",  # Show only first 10 characters
                "created_at": session.created_at.isoformat(),
                "expires_at": session.expires_at.isoformat(),
                "user_agent": session.user_agent,
                "ip_address": session.ip_address
            })
        return {"active_sessions": session_list}
    except Exception as e:
        print(f"Error getting active sessions: {e}")
        return {"active_sessions": []}

@router.get("/check-availability")
async def check_availability(username: Optional[str] = None, email: Optional[str] = None, db: Session = Depends(get_db)):
    """Check if username or email is available"""
    result = {"available": True}
    
    if username:
        if get_user_by_username(db, username):
            result["available"] = False
            result["message"] = "Username already exists"
    
    if email and result["available"]:
        if get_user_by_email(db, email):
            result["available"] = False
            result["message"] = "Email already registered"
    
    return result

@router.put("/profile", response_model=UpdateProfileResponse)
async def update_profile(data: UpdateProfileRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update user profile information"""
    try:
        # Check if new email is already taken by another user
        if data.email and data.email != current_user["email"]:
            existing_user = get_user_by_email(db, data.email)
            if existing_user and existing_user.id != current_user["id"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered by another user"
                )
        
        # Update user profile
        updated_user = update_user_profile(db, current_user["id"], data.full_name, data.email)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "message": "Profile updated successfully",
            "user_info": {
                "username": updated_user.username,
                "email": updated_user.email,
                "full_name": updated_user.full_name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )

@router.put("/change-password")
async def change_password(data: ChangePasswordRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Change user password"""
    try:
        # Verify current password
        user = get_user_by_id(db, current_user["id"])
        if not user or not pwd_context.verify(data.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Change password
        if change_user_password(db, current_user["id"], data.new_password):
            return {"message": "Password changed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Password change failed"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Password change error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )

@router.get("/check-email-availability")
async def check_email_availability(email: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if email is available for the current user"""
    if email == current_user["email"]:
        return {"available": True, "message": "This is your current email"}
    
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return {"available": False, "message": "Email already registered"}
    
    return {"available": True, "message": "Email is available"}

@router.put("/training-profile")
async def update_training_profile_endpoint(data: TrainingProfileUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update user training profile"""
    try:
        # Convert pydantic model to dict, excluding None values
        profile_data = {k: v for k, v in data.dict().items() if v is not None}
        
        # Update training profile
        updated_profile = update_training_profile(db, current_user["id"], profile_data)
        if not updated_profile:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Training profile update failed"
            )
        
        return {"message": "Training profile updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Training profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Training profile update failed"
        )

@router.get("/training-profile")
async def get_training_profile_endpoint(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user training profile"""
    try:
        profile = get_training_profile(db, current_user["id"])
        if not profile:
            return {"training_profile": None}
        
        return {
            "training_profile": {
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
                }
            }
        }
    except Exception as e:
        print(f"Get training profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve training profile"
        )