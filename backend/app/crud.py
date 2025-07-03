from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.models.database_models import User, TrainingProfile, ActiveSession, Course, UserCourseProgress, Training
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid
import psycopg2.errors

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DuplicateCourseIdError(Exception):
    """Исключение для случая дублирования course_id"""
    def __init__(self, course_id: str):
        self.course_id = course_id
        super().__init__(f"Training with course_id '{course_id}' already exists")


# User CRUD operations
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, username: str, full_name: str, email: str, password: str, is_admin: bool = False, trainer_profile: Dict[str, Any] = None, country: str = None, city: str = None) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username,
        full_name=full_name,
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin,
        trainer_profile=trainer_profile,
        country=country,
        city=city
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


def update_user_profile(db: Session, user_id: int, username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, country: Optional[str] = None, city: Optional[str] = None) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if username:
        user.username = username
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if country is not None:
        user.country = country
    if city is not None:
        user.city = city
    
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
def get_training_by_id(db: Session, training_id: str) -> Optional[Training]:
    """Получить тренировку по course_id (UUID из JSON)"""
    return db.query(Training).filter(Training.course_id == training_id).first()


def get_trainings_summary(db: Session, skip: int = 0, limit: int = 100) -> List[Training]:
    """Получить список всех тренировок с краткой информацией"""
    return db.query(Training).offset(skip).limit(limit).all()


def get_trainings_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Training]:
    """Получить тренировки конкретного пользователя"""
    return db.query(Training).filter(
        Training.user_id == user_id
    ).offset(skip).limit(limit).all()


def create_training(db: Session, training_data: dict, user_id: int):
    """
    Создать новую тренировку в базе данных.
    Обрабатывает опциональные поля и устанавливает значения по умолчанию.
    """
    import uuid
    
    # Генерируем уникальный course_id если не предоставлен
    if 'id' not in training_data or not training_data['id']:
        course_id = str(uuid.uuid4())
    else:
        course_id = training_data['id']
    
    # Создаем дефолтные объекты для certification и experience если они не предоставлены
    certification = training_data.get('certification')
    if certification is None:
        certification = {
            "Type": "",
            "Level": "",
            "Specialization": ""
        }
    
    experience = training_data.get('experience')
    if experience is None:
        experience = {
            "Years": 0,
            "Specialization": "",
            "Courses": 0,
            "Rating": 0.0
        }
    
    # Создаем объект тренировки с обработкой всех полей
    db_training = Training(
        course_id=course_id,
        user_id=user_id,
        
        # Основная информация о курсе
        activity_type=training_data.get('activity_type', ''),
        program_goal=training_data.get('program_goal', []),
        training_environment=training_data.get('training_environment', []),
        difficulty_level=training_data.get('difficulty_level', ''),
        course_duration_weeks=training_data.get('course_duration_weeks', 0),
        weekly_training_frequency=training_data.get('weekly_training_frequency', ''),
        average_workout_duration=training_data.get('average_workout_duration', ''),
        age_group=training_data.get('age_group', []),
        gender_orientation=training_data.get('gender_orientation', ''),
        physical_limitations=training_data.get('physical_limitations', []),
        required_equipment=training_data.get('required_equipment', []),
        course_language=training_data.get('course_language', ''),
        visual_content=training_data.get('visual_content', []),
        trainer_feedback_options=training_data.get('trainer_feedback_options', []),
        tags=training_data.get('tags', []),
        
        # Рейтинги и статистика
        average_course_rating=training_data.get('average_course_rating', 0.0),
        active_participants=training_data.get('active_participants', 0),
        number_of_reviews=training_data.get('number_of_reviews', 0),
        
        # Данные о тренере
        certification=certification,
        experience=experience,
        trainer_name=training_data.get('trainer_name', ''),
        
        # Информация о курсе
        course_title=training_data.get('course_title', ''),
        program_description=training_data.get('program_description', ''),
        
        # План тренировок
        training_plan=training_data.get('training_plan', [])
    )
    
    try:
        db.add(db_training)
        db.commit()
        db.refresh(db_training)
        return db_training
    except IntegrityError as e:
        db.rollback()
        # Проверяем, является ли это ошибкой дублирования course_id
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            if "ix_trainings_course_id" in str(e.orig):
                print(f"Duplicate course_id detected: {course_id}")
                raise DuplicateCourseIdError(course_id)
        print(f"Integrity error creating training: {e}")
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error creating training: {e}")
        raise e


def update_training(db: Session, training_id: str, training_data: Dict[str, Any]) -> Optional[Training]:
    """Обновить существующую тренировку по course_id"""
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


def delete_training(db: Session, training_id: str) -> bool:
    """Удаление тренировки по course_id"""
    training = get_training_by_id(db, training_id)
    if not training:
        return False
    
    db.delete(training)
    db.commit()
    return True


def search_trainings(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Training]:
    """Поиск тренировок по названию курса"""
    search_filter = f"%{query}%"
    return db.query(Training).filter(
        Training.course_title.ilike(search_filter)
    ).offset(skip).limit(limit).all()


def get_training_with_trainer_info(db: Session, training_id: str) -> Optional[Training]:
    """Получить тренировку по course_id (в новом формате уже содержит всю информацию о тренере)"""
    return get_training_by_id(db, training_id) 