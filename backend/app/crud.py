from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.database_models import User, TrainingProfile, ActiveSession, Course, UserCourseProgress
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User CRUD operations
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, username: str, email: str, password: str, full_name: str, is_admin: bool = False) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create empty training profile
    create_training_profile(db, db_user.id)
    
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user_profile(db: Session, user_id: int, full_name: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def change_user_password(db: Session, user_id: int, new_password: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    user.hashed_password = pwd_context.hash(new_password)
    user.updated_at = datetime.utcnow()
    db.commit()
    return True


# Training Profile CRUD operations
def get_training_profile(db: Session, user_id: int) -> Optional[TrainingProfile]:
    return db.query(TrainingProfile).filter(TrainingProfile.user_id == user_id).first()


def create_training_profile(db: Session, user_id: int) -> TrainingProfile:
    db_profile = TrainingProfile(user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_training_profile(db: Session, user_id: int, profile_data: Dict[str, Any]) -> Optional[TrainingProfile]:
    profile = get_training_profile(db, user_id)
    if not profile:
        profile = create_training_profile(db, user_id)
    
    # Update fields
    for field, value in profile_data.items():
        if hasattr(profile, field) and value is not None:
            setattr(profile, field, value)
    
    profile.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    return profile


# Active Session CRUD operations
def create_active_session(db: Session, user_id: int, token: str, expires_at: datetime, user_agent: str = None, ip_address: str = None) -> ActiveSession:
    db_session = ActiveSession(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_active_session(db: Session, token: str) -> Optional[ActiveSession]:
    return db.query(ActiveSession).filter(
        and_(
            ActiveSession.token == token,
            ActiveSession.expires_at > datetime.utcnow()
        )
    ).first()


def revoke_session(db: Session, token: str) -> bool:
    session = db.query(ActiveSession).filter(ActiveSession.token == token).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False


def revoke_user_sessions(db: Session, user_id: int) -> int:
    sessions = db.query(ActiveSession).filter(ActiveSession.user_id == user_id).all()
    count = len(sessions)
    for session in sessions:
        db.delete(session)
    db.commit()
    return count


def cleanup_expired_sessions(db: Session) -> int:
    expired_sessions = db.query(ActiveSession).filter(
        ActiveSession.expires_at <= datetime.utcnow()
    ).all()
    count = len(expired_sessions)
    for session in expired_sessions:
        db.delete(session)
    db.commit()
    return count


def get_user_active_sessions(db: Session, user_id: int) -> List[ActiveSession]:
    return db.query(ActiveSession).filter(
        and_(
            ActiveSession.user_id == user_id,
            ActiveSession.expires_at > datetime.utcnow()
        )
    ).all()


# Course CRUD operations
def get_course_by_id(db: Session, course_id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100, category: str = None) -> List[Course]:
    query = db.query(Course).filter(Course.is_active == True)
    if category:
        query = query.filter(Course.category == category)
    return query.offset(skip).limit(limit).all()


def create_course(db: Session, course_data: Dict[str, Any]) -> Course:
    db_course = Course(**course_data)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


# Course Progress CRUD operations
def get_user_course_progress(db: Session, user_id: int, course_id: int) -> Optional[UserCourseProgress]:
    return db.query(UserCourseProgress).filter(
        and_(
            UserCourseProgress.user_id == user_id,
            UserCourseProgress.course_id == course_id
        )
    ).first()


def update_course_progress(db: Session, user_id: int, course_id: int, progress_percentage: float) -> UserCourseProgress:
    progress = get_user_course_progress(db, user_id, course_id)
    if not progress:
        progress = UserCourseProgress(
            user_id=user_id,
            course_id=course_id,
            progress_percentage=progress_percentage
        )
        db.add(progress)
    else:
        progress.progress_percentage = progress_percentage
        if progress_percentage >= 100.0 and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    return progress 