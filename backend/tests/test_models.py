import sys
import os
from datetime import datetime  # Добавьте этот импорт в начало файла

# Добавляем корень проекта (backend) в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Теперь импортируем модели
from app.models.database_models import (
    User,
    TrainingProfile,
    ActiveSession,
    Course,
    UserCourseProgress,
    Training
)

def test_user_model(test_db):
    # Тестируем создание пользователя
    user = User(
        username="testuser",
        full_name="Test User",
        email="test@example.com",
        hashed_password="hashed123",
        country="kz",
        city="Almaty"
    )
    
    test_db.add(user)
    test_db.commit()
    
    assert user.id is not None
    assert user.is_active is True
    assert user.is_admin is False
    assert "testuser" in user.username

def test_training_profile_model(test_db):
    # Сначала создаем пользователя
    user = User(
        username="profile_test",
        full_name="Profile Test",
        email="profile@test.com",
        hashed_password="hashed456"
    )
    test_db.add(user)
    test_db.commit()
    
    # Тестируем профиль тренировок
    profile = TrainingProfile(
        user_id=user.id,
        gender="male",
        age=30,
        height_cm=180,
        weight_kg=75.5,
        training_level="intermediate"
    )
    
    test_db.add(profile)
    test_db.commit()
    
    assert profile.id is not None
    assert profile.user_id == user.id
    assert profile.age == 30

def test_active_session_model(test_db):
    # Создаем тестового пользователя
    user = User(
        username="session_test",
        full_name="Session Test",
        email="session@test.com",
        hashed_password="hashed789"
    )
    test_db.add(user)
    test_db.commit()
    
    # Создаем сессию с корректным временем
    session = ActiveSession(
        user_id=user.id,
        token="test_token_123",
        expires_at=datetime(2025, 12, 31)  # Теперь datetime доступен
    )
    
    test_db.add(session)
    test_db.commit()
    
    assert session.id is not None
    assert session.token == "test_token_123"

def test_course_model(test_db):
    course = Course(
        title="Python Programming",
        description="Learn Python basics",
        duration_minutes=120,
        difficulty_level="beginner"
    )
    
    test_db.add(course)
    test_db.commit()
    
    assert course.id is not None
    assert course.is_active is True

def test_user_course_progress_model(test_db):
    user = User(
        username="progress_test",
        full_name="Progress Test",
        email="progress@test.com",
        hashed_password="hashed000"
    )
    course = Course(
        title="Advanced SQL",
        description="SQL for professionals"
    )
    test_db.add_all([user, course])
    test_db.commit()
    
    progress = UserCourseProgress(
        user_id=user.id,
        course_id=course.id,
        progress_percentage=25.0
    )
    
    test_db.add(progress)
    test_db.commit()
    
    assert progress.id is not None
    assert progress.progress_percentage == 25.0

def test_training_model(test_db):
    user = User(
        username="training_test",
        full_name="Training Test",
        email="training@test.com",
        hashed_password="hashed111"
    )
    test_db.add(user)
    test_db.commit()
    
    training = Training(
        course_id="course_123",
        user_id=user.id,
        activity_type="strength",
        difficulty_level="intermediate",
        course_duration_weeks=4,
        program_goal=["muscle_gain"]
    )
    
    test_db.add(training)
    test_db.commit()
    
    assert training.id is not None
    assert "strength" in training.activity_type
    assert "muscle_gain" in training.program_goal

    
