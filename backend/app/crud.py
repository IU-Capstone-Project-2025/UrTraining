from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.database_models import User, TrainingProfile, ActiveSession, Course, UserCourseProgress, Training
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User CRUD operations
def get_user_by_name(db: Session, name: str) -> Optional[User]:
    return db.query(User).filter(User.name == name).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, name: str, email: str, password: str, is_admin: bool = False, trainer_profile: Dict[str, Any] = None) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin,
        trainer_profile=trainer_profile
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create empty training profile
    create_training_profile(db, db_user.id)
    
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user_profile(db: Session, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if name:
        user.name = name
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


def update_user_trainer_profile(db: Session, user_id: int, trainer_profile: Dict[str, Any]) -> Optional[User]:
    """Обновить профиль тренера пользователя"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.trainer_profile = trainer_profile
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


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


# Training CRUD operations
def get_training_by_id(db: Session, training_id: int) -> Optional[Training]:
    """Получить тренировку по ID"""
    return db.query(Training).filter(Training.id == training_id).first()


def get_trainings_summary(db: Session, skip: int = 0, limit: int = 100) -> List[Training]:
    """Получить список всех активных тренировок с краткой информацией"""
    return db.query(Training).filter(
        Training.is_active == True
    ).offset(skip).limit(limit).all()


def get_trainings_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Training]:
    """Получить тренировки конкретного пользователя"""
    return db.query(Training).filter(
        and_(
            Training.user_id == user_id,
            Training.is_active == True
        )
    ).offset(skip).limit(limit).all()


def create_training(db: Session, training_data: Dict[str, Any], user_id: int = None) -> Training:
    """Создать новую тренировку с данными в новом формате"""
    import uuid
    
    # Получаем пользователя для заполнения данных тренера
    user = None
    trainer_profile = None
    if user_id:
        user = get_user_by_id(db, user_id)
        if user and hasattr(user, 'trainer_profile') and user.trainer_profile:
            trainer_profile = user.trainer_profile

    # Автоматически заполняем статистику и рейтинги
    average_course_rating = trainer_profile.get("experience", {}).get("rating", 0.0) if trainer_profile else 0.0
    number_of_reviews = trainer_profile.get("reviews_count", 0) if trainer_profile else 0
    
    # Генерируем уникальный ID для курса если не предоставлен
    course_id = training_data.get("id", str(uuid.uuid4()))
    
    # Создаем тренировку с новой структурой
    db_training = Training(
        user_id=user_id,
        activity_type=training_data.get("activity_type", ""),
        program_goal=training_data.get("program_goal", []),
        training_environment=training_data.get("training_environment", []),
        difficulty_level=training_data.get("difficulty_level", ""),
        course_duration_weeks=training_data.get("course_duration_weeks", 1),
        weekly_training_frequency=training_data.get("weekly_training_frequency", ""),
        average_workout_duration=training_data.get("average_workout_duration", ""),
        age_group=training_data.get("age_group", []),
        gender_orientation=training_data.get("gender_orientation", ""),
        physical_limitations=training_data.get("physical_limitations", []),
        required_equipment=training_data.get("required_equipment", []),
        course_language=training_data.get("course_language", ""),
        visual_content=training_data.get("visual_content", []),
        trainer_feedback_options=training_data.get("trainer_feedback_options", []),
        tags=training_data.get("tags", []),
        average_course_rating=average_course_rating,
        active_participants=0,  # Начинаем с 0
        number_of_reviews=number_of_reviews,
        certification=training_data.get("certification", {}),
        experience=training_data.get("experience", {}),
        trainer_name=training_data.get("trainer_name", user.name if user else ""),
        course_title=training_data.get("course_title", ""),
        program_description=training_data.get("program_description", ""),
        training_plan=training_data.get("training_plan", []),
        course_id=course_id
    )
    
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training


def update_training(db: Session, training_id: int, training_data: Dict[str, Any]) -> Optional[Training]:
    """Обновить существующую тренировку"""
    training = get_training_by_id(db, training_id)
    if not training:
        return None
    
    # Обновляем поля новой структуры
    updatable_fields = [
        'activity_type', 'program_goal', 'training_environment', 'difficulty_level',
        'course_duration_weeks', 'weekly_training_frequency', 'average_workout_duration',
        'age_group', 'gender_orientation', 'physical_limitations', 'required_equipment',
        'course_language', 'visual_content', 'trainer_feedback_options', 'tags',
        'certification', 'experience', 'trainer_name', 'course_title',
        'program_description', 'training_plan'
    ]
    
    for field in updatable_fields:
        if field in training_data and training_data[field] is not None:
            setattr(training, field, training_data[field])
    
    training.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(training)
    return training


def delete_training(db: Session, training_id: int) -> bool:
    """Мягкое удаление тренировки (деактивация)"""
    training = get_training_by_id(db, training_id)
    if not training:
        return False
    
    training.is_active = False
    training.updated_at = datetime.utcnow()
    db.commit()
    return True


def search_trainings(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Training]:
    """Поиск тренировок по названию курса"""
    search_filter = f"%{query}%"
    return db.query(Training).filter(
        and_(
            Training.is_active == True,
            Training.course_title.ilike(search_filter)
        )
    ).offset(skip).limit(limit).all()


def get_training_with_trainer_info(db: Session, training_id: int) -> Optional[Training]:
    """Получить тренировку (в новом формате уже содержит всю информацию о тренере)"""
    return get_training_by_id(db, training_id) 