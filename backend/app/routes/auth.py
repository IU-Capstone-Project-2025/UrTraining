from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, List

router = APIRouter()

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# In-memory storage for active tokens (use Redis in production)
active_tokens: Dict[str, dict] = {}

# Sample users (use database in production)
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("123"),
        "email": "admin@example.com",
        "full_name": "Administrator",
        "training_profile": {
            "basic_information": {
                "gender": "male",
                "age": 30,
                "height_cm": 180,
                "weight_kg": 75.0
            },
            "training_goals": ["maintain_fitness", "muscle_gain"],
            "training_experience": {
                "level": "intermediate",
                "frequency_last_3_months": "3_4_times_week"
            },
            "preferences": {
                "training_location": "gym",
                "location_details": "full_fitness_center",
                "session_duration": "45_60_min"
            },
            "health": {
                "joint_back_problems": False,
                "chronic_conditions": False,
                "health_details": None
            },
            "training_types": {
                "strength_training": 4,
                "cardio": 3,
                "hiit": 3,
                "yoga_pilates": 2,
                "functional_training": 4,
                "stretching": 3
            }
        }
    },
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("password"),
        "email": "user@example.com",
        "full_name": "Regular User",
        "training_profile": {
            "basic_information": {
                "gender": "female",
                "age": 25,
                "height_cm": 165,
                "weight_kg": 60.0
            },
            "training_goals": ["weight_loss", "improve_flexibility"],
            "training_experience": {
                "level": "beginner",
                "frequency_last_3_months": "1_2_times_week"
            },
            "preferences": {
                "training_location": "home",
                "location_details": "no_equipment",
                "session_duration": "30_45_min"
            },
            "health": {
                "joint_back_problems": False,
                "chronic_conditions": False,
                "health_details": None
            },
            "training_types": {
                "strength_training": 2,
                "cardio": 4,
                "hiit": 2,
                "yoga_pilates": 5,
                "functional_training": 3,
                "stretching": 5
            }
        }
    }
}

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

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def is_username_taken(username: str):
    return username in fake_users_db

def is_email_taken(email: str):
    for user in fake_users_db.values():
        if user.get("email") == email:
            return True
    return False

def create_user(username: str, password: str, email: str, full_name: str):
    hashed_password = pwd_context.hash(password)
    user_data = {
        "username": username,
        "hashed_password": hashed_password,
        "email": email,
        "full_name": full_name,
        "training_profile": {
            "basic_information": {
                "gender": None,
                "age": None,
                "height_cm": None,
                "weight_kg": None
            },
            "training_goals": [],
            "training_experience": {
                "level": None,
                "frequency_last_3_months": None
            },
            "preferences": {
                "training_location": None,
                "location_details": None,
                "session_duration": None
            },
            "health": {
                "joint_back_problems": None,
                "chronic_conditions": None,
                "health_details": None
            },
            "training_types": {
                "strength_training": None,
                "cardio": None,
                "hiit": None,
                "yoga_pilates": None,
                "functional_training": None,
                "stretching": None
            }
        }
    }
    fake_users_db[username] = user_data
    return user_data

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    
    # Check if token is in active tokens
    if token not in active_tokens:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest):
    """Register a new user account"""
    
    # Validate username availability
    if is_username_taken(data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Validate email availability
    if is_email_taken(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        user = create_user(data.username, data.password, data.email, data.full_name)
        return {
            "message": "User registered successfully",
            "user_info": {
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"]
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    """Authenticate user and return JWT token"""
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    # Store token in active tokens
    token_data = {
        "username": user["username"],
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + access_token_expires).isoformat()
    }
    active_tokens[access_token] = token_data
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
        "user_info": {
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    }

@router.post("/logout", response_model=LogoutResponse)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user by invalidating the token"""
    token = credentials.credentials
    
    if token in active_tokens:
        del active_tokens[token]
        return {"message": "Successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user["full_name"]
    }

@router.get("/verify-token")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """Verify if token is valid"""
    return {"valid": True, "user": current_user["username"]}

@router.get("/active-sessions")
async def get_active_sessions():
    """Get information about active sessions (admin only in production)"""
    return {
        "active_sessions": len(active_tokens),
        "sessions": [
            {
                "username": data["username"],
                "created_at": data["created_at"],
                "expires_at": data["expires_at"]
            }
            for data in active_tokens.values()
        ]
    }

@router.get("/check-availability")
async def check_availability(username: Optional[str] = None, email: Optional[str] = None):
    """Check if username or email is available for registration"""
    result = {}
    
    if username:
        result["username_available"] = not is_username_taken(username)
    
    if email:
        result["email_available"] = not is_email_taken(email)
    
    return result

@router.put("/profile", response_model=UpdateProfileResponse)
async def update_profile(data: UpdateProfileRequest, current_user: dict = Depends(get_current_user)):
    """Update user profile information"""
    username = current_user["username"]
    user_data = fake_users_db[username].copy()
    
    # Check if email is being changed and if it's available
    if data.email and data.email != user_data.get("email"):
        if is_email_taken(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user_data["email"] = data.email
    
    # Update full name if provided
    if data.full_name:
        user_data["full_name"] = data.full_name
    
    # Save updated user data
    fake_users_db[username] = user_data
    
    return {
        "message": "Profile updated successfully",
        "user_info": {
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"]
        }
    }

@router.put("/change-password")
async def change_password(data: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    """Change user password"""
    username = current_user["username"]
    user_data = fake_users_db[username]
    
    # Verify current password
    if not verify_password(data.current_password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user_data["hashed_password"] = pwd_context.hash(data.new_password)
    fake_users_db[username] = user_data
    
    return {"message": "Password changed successfully"}

@router.get("/check-email-availability")
async def check_email_availability(email: str, current_user: dict = Depends(get_current_user)):
    """Check if email is available for current user (excluding their own email)"""
    current_email = current_user.get("email")
    
    # If it's the same as current email, it's available for them
    if email == current_email:
        return {"email_available": True}
    
    # Check if email is taken by someone else
    return {"email_available": not is_email_taken(email)}

@router.put("/training-profile")
async def update_training_profile(data: TrainingProfileUpdate, current_user: dict = Depends(get_current_user)):
    """Update user's training profile information"""
    username = current_user["username"]
    user_data = fake_users_db[username].copy()
    
    # Ensure training_profile exists
    if "training_profile" not in user_data:
        user_data["training_profile"] = {
            "basic_information": {},
            "training_goals": [],
            "training_experience": {},
            "preferences": {},
            "health": {},
            "training_types": {}
        }
    
    training_profile = user_data["training_profile"]
    
    # Update basic information
    if any([data.gender, data.age, data.height_cm, data.weight_kg]):
        if "basic_information" not in training_profile:
            training_profile["basic_information"] = {}
        
        if data.gender is not None:
            training_profile["basic_information"]["gender"] = data.gender
        if data.age is not None:
            training_profile["basic_information"]["age"] = data.age
        if data.height_cm is not None:
            training_profile["basic_information"]["height_cm"] = data.height_cm
        if data.weight_kg is not None:
            training_profile["basic_information"]["weight_kg"] = data.weight_kg
    
    # Update training goals
    if data.training_goals is not None:
        training_profile["training_goals"] = data.training_goals
    
    # Update training experience
    if any([data.training_level, data.frequency_last_3_months]):
        if "training_experience" not in training_profile:
            training_profile["training_experience"] = {}
        
        if data.training_level is not None:
            training_profile["training_experience"]["level"] = data.training_level
        if data.frequency_last_3_months is not None:
            training_profile["training_experience"]["frequency_last_3_months"] = data.frequency_last_3_months
    
    # Update preferences
    if any([data.training_location, data.location_details, data.session_duration]):
        if "preferences" not in training_profile:
            training_profile["preferences"] = {}
        
        if data.training_location is not None:
            training_profile["preferences"]["training_location"] = data.training_location
        if data.location_details is not None:
            training_profile["preferences"]["location_details"] = data.location_details
        if data.session_duration is not None:
            training_profile["preferences"]["session_duration"] = data.session_duration
    
    # Update health information
    if any([data.joint_back_problems is not None, data.chronic_conditions is not None, data.health_details]):
        if "health" not in training_profile:
            training_profile["health"] = {}
        
        if data.joint_back_problems is not None:
            training_profile["health"]["joint_back_problems"] = data.joint_back_problems
        if data.chronic_conditions is not None:
            training_profile["health"]["chronic_conditions"] = data.chronic_conditions
        if data.health_details is not None:
            training_profile["health"]["health_details"] = data.health_details
    
    # Update training types
    training_type_fields = [
        'strength_training', 'cardio', 'hiit', 'yoga_pilates', 
        'functional_training', 'stretching'
    ]
    
    if any(getattr(data, field) is not None for field in training_type_fields):
        if "training_types" not in training_profile:
            training_profile["training_types"] = {}
        
        for field in training_type_fields:
            value = getattr(data, field)
            if value is not None:
                training_profile["training_types"][field] = value
    
    # Save updated user data
    fake_users_db[username] = user_data
    
    return {
        "message": "Training profile updated successfully",
        "training_profile": training_profile
    }

@router.get("/training-profile")
async def get_training_profile(current_user: dict = Depends(get_current_user)):
    """Get user's complete training profile"""
    username = current_user["username"]
    user_data = fake_users_db[username]
    
    return {
        "username": user_data["username"],
        "full_name": user_data["full_name"],
        "email": user_data["email"],
        "training_profile": user_data.get("training_profile", {})
    }