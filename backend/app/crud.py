from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.database_models import User, TrainingProfile, ActiveSession, Course, UserCourseProgress, Training
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


def create_user(db: Session, username: str, email: str, password: str, full_name: str, is_admin: bool = False, trainer_profile: Dict[str, Any] = None) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
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
    """Создать новую тренировку"""
    # Если пользователь является тренером, заполняем информацию о тренере в metadata
    metadata = training_data.get("metadata", {})
    if user_id:
        user = get_user_by_id(db, user_id)
        if user and user.trainer_profile:
            trainer_profile = user.trainer_profile
            metadata["trainer_name"] = trainer_profile.get("name")
            metadata["certification"] = trainer_profile.get("certification")
            metadata["experience"] = trainer_profile.get("experience")
    
    db_training = Training(
        user_id=user_id,
        training_metadata=metadata,
        training_data=training_data.get("training_data"),
        title=training_data.get("title"),
        description=training_data.get("description")
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
    
    # Обновляем поля
    for field, value in training_data.items():
        if field == "metadata":
            # Специальная обработка для metadata - сохраняем в training_metadata
            training.training_metadata = value
        elif hasattr(training, field) and value is not None:
            setattr(training, field, value)
    
    # Если обновляется metadata и пользователь является тренером, обновляем информацию о тренере
    if "metadata" in training_data and training.user_id:
        user = get_user_by_id(db, training.user_id)
        if user and user.trainer_profile:
            trainer_profile = user.trainer_profile
            metadata = training_data["metadata"]
            metadata["trainer_name"] = trainer_profile.get("name")
            metadata["certification"] = trainer_profile.get("certification")
            metadata["experience"] = trainer_profile.get("experience")
            training.training_metadata = metadata
    
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
    """Поиск тренировок по названию или описанию"""
    search_filter = f"%{query}%"
    return db.query(Training).filter(
        and_(
            Training.is_active == True,
            (Training.title.ilike(search_filter) | Training.description.ilike(search_filter))
        )
    ).offset(skip).limit(limit).all()


def get_training_with_trainer_info(db: Session, training_id: int) -> Optional[Training]:
    """Получить тренировку с заполненной информацией о тренере"""
    training = get_training_by_id(db, training_id)
    if not training:
        return None
    
    # Если у тренировки есть пользователь и у пользователя есть trainer_profile
    if training.user_id:
        user = get_user_by_id(db, training.user_id)
        if user and user.trainer_profile:
            # Создаем копию metadata для модификации
            metadata = training.training_metadata.copy() if training.training_metadata else {}
            trainer_profile = user.trainer_profile
            
            # Заполняем данные тренера
            metadata["trainer_name"] = trainer_profile.get("name", "")
            metadata["certification"] = trainer_profile.get("certification", {})
            metadata["experience"] = trainer_profile.get("experience", {})
            
            # Обновляем metadata в объекте тренировки
            training.training_metadata = metadata
    
    return training


def merge_trainer_info_to_metadata(metadata: Dict[str, Any], trainer_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Объединить metadata тренировки с данными trainer_profile"""
    if not trainer_profile:
        return metadata
    
    updated_metadata = metadata.copy()
    
    # Заполняем поля тренера
    updated_metadata["trainer_name"] = trainer_profile.get("name", "")
    updated_metadata["certification"] = trainer_profile.get("certification", {})
    updated_metadata["experience"] = trainer_profile.get("experience", {})
    
    return updated_metadata 