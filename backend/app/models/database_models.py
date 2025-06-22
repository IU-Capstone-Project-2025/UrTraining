from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to training profile
    training_profile = relationship("TrainingProfile", back_populates="user", uselist=False)
    active_sessions = relationship("ActiveSession", back_populates="user")
    # Relationship to trainings
    trainings = relationship("Training", back_populates="user")


class TrainingProfile(Base):
    __tablename__ = "training_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Basic Information
    gender = Column(String(10))
    age = Column(Integer)
    height_cm = Column(Integer)
    weight_kg = Column(Float)
    
    # Training Goals (stored as JSON array)
    training_goals = Column(JSON)
    
    # Training Experience
    training_level = Column(String(20))
    frequency_last_3_months = Column(String(30))
    
    # Preferences
    training_location = Column(String(20))
    location_details = Column(String(30))
    session_duration = Column(String(20))
    
    # Health
    joint_back_problems = Column(Boolean)
    chronic_conditions = Column(Boolean)
    health_details = Column(Text)
    
    # Training Types (1-5 scale)
    strength_training = Column(Integer)
    cardio = Column(Integer)
    hiit = Column(Integer)
    yoga_pilates = Column(Integer)
    functional_training = Column(Integer)
    stretching = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="training_profile")


class ActiveSession(Base):
    __tablename__ = "active_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String(255))
    ip_address = Column(String(45))
    
    # Relationship to user
    user = relationship("User", back_populates="active_sessions")


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    difficulty_level = Column(String(20))
    category = Column(String(50))
    video_url = Column(String(255))
    thumbnail_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserCourseProgress(Base):
    __tablename__ = "user_course_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress_percentage = Column(Float, default=0.0)
    completed_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    course = relationship("Course")


class Training(Base):
    """
    SQLAlchemy модель для тренировки в базе данных
    """
    __tablename__ = "trainings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Основные поля согласно требуемой JSON структуре
    metainfo = Column(Text, nullable=False)
    training_data = Column(JSON, nullable=False)  # JSON структура с данными тренировки по дням
    
    # Дополнительные поля для расширенной функциональности
    title = Column(String(255))
    description = Column(Text)
    duration_weeks = Column(Integer)
    difficulty_level = Column(String(20))
    created_by = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="trainings") 