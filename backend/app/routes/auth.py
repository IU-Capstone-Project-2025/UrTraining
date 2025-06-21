from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import (
    authenticate_user, get_user_by_username, get_user_by_email, create_user,
    create_active_session, get_active_session, revoke_session,
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