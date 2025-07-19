from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    country = Column(String(3), nullable=True)  # Country code (kz, ru, us)
    city = Column(String(100), nullable=True)   # City name
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Trainer profile (JSON field for trainer information)
    trainer_profile = Column(JSON, nullable=True)
    
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
    SQLAlchemy модель для тренировки в базе данных, соответствующая новой JSON структуре
    """
    __tablename__ = "trainings"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Основная информация о курсе
    activity_type = Column(String, default="")
    program_goal = Column(JSON, default=list)
    training_environment = Column(JSON, default=list)
    difficulty_level = Column(String, default="")
    course_duration_weeks = Column(Integer, default=0)
    weekly_training_frequency = Column(String, default="")
    average_workout_duration = Column(String, default="")
    age_group = Column(JSON, default=list)
    gender_orientation = Column(String, default="")
    physical_limitations = Column(JSON, default=list)
    required_equipment = Column(JSON, default=list)
    course_language = Column(String, default="")
    visual_content = Column(JSON, default=list)
    trainer_feedback_options = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    
    # Рейтинги и статистика
    average_course_rating = Column(Float, default=0.0)
    active_participants = Column(Integer, default=0)
    number_of_reviews = Column(Integer, default=0)
    
    # Данные о тренере (могут быть NULL)
    certification = Column(JSON, nullable=True)
    experience = Column(JSON, nullable=True)
    trainer_name = Column(String, default="")
    
    # Информация о курсе
    course_title = Column(String, default="")
    program_description = Column(Text, default="")
    
    # План тренировок
    training_plan = Column(JSON, default=list)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с пользователем
    user = relationship("User", back_populates="trainings")


class SavedProgram(Base):
    """
    SQLAlchemy модель для сохраненных программ тренировок
    """
    __tablename__ = "saved_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    training_id = Column(Integer, ForeignKey("trainings.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User")
    training = relationship("Training")
    
    # Уникальная комбинация пользователя и тренировки
    __table_args__ = (
        UniqueConstraint('user_id', 'training_id', name='unique_user_training'),
    )


class TrainingProgress(Base):
    """
    SQLAlchemy модель для прогресса пользователей по тренировкам
    """
    __tablename__ = "training_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    training_id = Column(Integer, ForeignKey("trainings.id"), nullable=False)
    completed_items = Column(JSON, default=list)  # Список номеров выполненных items [0, 1, 3, ...]
    total_items = Column(Integer, default=0)  # Общее количество items в training_plan
    progress_percentage = Column(Float, default=0.0)  # Процент прогресса (0.0 - 100.0)
    last_completed_item = Column(Integer, nullable=True)  # Номер последнего выполненного item
    started_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User")
    training = relationship("Training")
    
    # Уникальная комбинация пользователя и тренировки
    __table_args__ = (
        UniqueConstraint('user_id', 'training_id', name='unique_user_training_progress'),
    ) 


class TrainingSchedule(Base):
    """
    SQLAlchemy модель для расписания тренировок пользователей
    """
    __tablename__ = "training_schedule"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(String, nullable=False)  # ID тренировочного плана
    date = Column(String(10), nullable=False)   # формат "ДД.ММ.ГГГГ" 
    training_index = Column(Integer, nullable=False)  # номер в training_plan (0, 1, 2...)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User")
    
    # Составной индекс для быстрого поиска
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date'),
        Index('idx_user_course', 'user_id', 'course_id'),
    ) 