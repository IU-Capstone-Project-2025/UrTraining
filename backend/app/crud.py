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
    """Создать новую тренировку с автоматическим заполнением данных тренера"""
    
    # Получаем пользователя и его профиль тренера
    user = None
    trainer_profile = None
    if user_id:
        user = get_user_by_id(db, user_id)
        if user and hasattr(user, 'trainer_profile') and user.trainer_profile:
            trainer_profile = user.trainer_profile
    
    # Автоматически заполняем coach_data
    coach_data = {}
    if trainer_profile and user:
        # Строим полные данные тренера без дополнительных badges
        coach_data = build_coach_data_from_trainer_profile(
            user.name, 
            trainer_profile, 
            additional_badges=None  # Не добавляем дополнительные badges
        )
    
    # Автоматически заполняем course_info
    course_info = training_data.get("course_info", {})
    if user:
        course_info = build_course_info_with_trainer_data(
            course_info, 
            user.name, 
            trainer_profile
        )
    
    # Создаем тренировку с заполненными данными
    db_training = Training(
        user_id=user_id,
        header_badges=training_data.get("header_badges", {}),
        course_info=course_info,
        training_plan=training_data.get("training_plan", []),
        coach_data=coach_data,
        training_metadata=training_data.get("metadata", {})
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
        if hasattr(training, field) and value is not None:
            setattr(training, field, value)
    
    # Если обновляется coach_data или course_info и пользователь является тренером, обновляем информацию
    if training.user_id:
        user = get_user_by_id(db, training.user_id)
        if user and hasattr(user, 'trainer_profile') and user.trainer_profile:
            trainer_profile = user.trainer_profile
            
            # Обновляем coach_data с данными тренера
            if "coach_data" in training_data:
                training.coach_data = build_coach_data_from_trainer_profile(
                    user.name, 
                    trainer_profile, 
                    additional_badges=None  # Не добавляем дополнительные badges
                )
            
            # Обновляем course_info с данными тренера
            if "course_info" in training_data:
                course_info = training_data["course_info"]
                training.course_info = build_course_info_with_trainer_data(
                    course_info, 
                    user.name, 
                    trainer_profile
                )
    
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
    """Поиск тренировок по названию из course_info"""
    search_filter = f"%{query}%"
    return db.query(Training).filter(
        and_(
            Training.is_active == True,
            Training.course_info['title'].astext.ilike(search_filter)
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
            # Создаем копию coach_data для модификации
            coach_data = training.coach_data.copy() if training.coach_data else {}
            trainer_profile = user.trainer_profile
            
            # Заполняем данные тренера
            coach_data.update({
                "name": user.name,
                "profile_picture": trainer_profile.get("profile_picture"),
                "rating": trainer_profile.get("experience", {}).get("rating", 0.0),
                "reviews": trainer_profile.get("reviews_count", 0),
                "years": trainer_profile.get("experience", {}).get("years", 0),
                "badges": trainer_profile.get("badges", [])
            })
            
            # Обновляем coach_data в объекте тренировки
            training.coach_data = coach_data
    
    return training


def merge_trainer_info_to_coach_data(coach_data: Dict[str, Any], trainer_profile: Dict[str, Any], name: str) -> Dict[str, Any]:
    """Объединить coach_data тренировки с данными trainer_profile"""
    if not trainer_profile:
        return coach_data
    
    updated_coach_data = coach_data.copy()
    
    # Заполняем поля тренера
    updated_coach_data.update({
        "name": name,
        "profile_picture": trainer_profile.get("profile_picture"),
        "rating": trainer_profile.get("experience", {}).get("rating", 0.0),
        "reviews": trainer_profile.get("reviews_count", updated_coach_data.get("reviews", 0)),
        "years": trainer_profile.get("experience", {}).get("years", 0),
        "badges": trainer_profile.get("badges", [])
    })
    
    return updated_coach_data


def build_coach_data_from_trainer_profile(user_name: str, trainer_profile: Dict[str, Any], additional_badges: List[Dict] = None) -> Dict[str, Any]:
    """
    Построить полные данные тренера (coach_data) из trainer_profile пользователя
    
    Args:
        user_name: Имя пользователя
        trainer_profile: Профиль тренера из базы данных
        additional_badges: Дополнительные значки для добавления (если None, то не добавляются)
    
    Returns:
        Словарь с полными данными тренера
    """
    if not trainer_profile:
        return {}
    
    experience = trainer_profile.get("experience", {})
    badges = trainer_profile.get("badges", []).copy()  # Создаем копию для безопасности
    
    # Добавляем дополнительные значки только если они переданы
    if additional_badges:
        badges.extend(additional_badges)
    
    return {
        "name": user_name,
        "profile_picture": trainer_profile.get("profile_picture"),
        "rating": experience.get("rating", 5.0),
        "reviews": trainer_profile.get("reviews_count", 0),
        "years": experience.get("years", 0),
        "badges": badges
    }


def build_course_info_with_trainer_data(course_info: Dict[str, Any], user_name: str, trainer_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Дополнить информацию о курсе данными тренера
    
    Args:
        course_info: Базовая информация о курсе
        user_name: Имя пользователя (автор курса)
        trainer_profile: Профиль тренера для заполнения рейтинга и отзывов
    
    Returns:
        Словарь с дополненной информацией о курсе
    """
    updated_course_info = course_info.copy()
    updated_course_info["author"] = user_name
    
    # Заполняем рейтинг и отзывы из профиля тренера, если они не указаны
    if trainer_profile:
        experience = trainer_profile.get("experience", {})
        
        if "rating" not in updated_course_info or updated_course_info["rating"] is None:
            updated_course_info["rating"] = experience.get("rating", 5.0)
        
        if "reviews" not in updated_course_info or updated_course_info["reviews"] is None:
            updated_course_info["reviews"] = trainer_profile.get("reviews_count", 0)
    
    return updated_course_info 