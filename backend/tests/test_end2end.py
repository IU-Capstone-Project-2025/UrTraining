import os
import sys
import pytest
import random
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Setting up paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Importing models and applications
from app.models.database_models import User, TrainingProfile
from app.database import Base
from main import app

# Test DATABASE setup - используем PostgreSQL из контейнера
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://uruser:urpassword@db:5432/urtraining"
)

print(f"🧪 Tests connecting to database: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Проверяем подключение к базе данных
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ Connected to PostgreSQL database successfully")
except Exception as e:
    print(f"❌ Failed to connect to database: {e}")
    raise

# Fixtures
@pytest.fixture(scope="module")
def test_app():
    # Создаем все таблицы для тестов
    Base.metadata.create_all(bind=engine)
    yield app
    # Очищаем данные после тестов, но не удаляем таблицы
    # (так как основное приложение может их использовать)

def clean_database_with_retry(max_retries=3, delay=0.1):
    """Очищает базу данных с повторными попытками для избежания deadlock"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                # Начинаем транзакцию
                trans = conn.begin()
                try:
                    # Используем DELETE вместо TRUNCATE для избежания deadlock
                    # Порядок важен для соблюдения внешних ключей
                    conn.execute(text("DELETE FROM user_course_progress;"))
                    conn.execute(text("DELETE FROM trainings;"))
                    conn.execute(text("DELETE FROM active_sessions;"))
                    conn.execute(text("DELETE FROM training_profiles;"))
                    conn.execute(text("DELETE FROM courses;"))
                    conn.execute(text("DELETE FROM users;"))
                    
                    # Сбрасываем последовательности для автоинкремента
                    conn.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
                    conn.execute(text("ALTER SEQUENCE training_profiles_id_seq RESTART WITH 1;"))
                    conn.execute(text("ALTER SEQUENCE active_sessions_id_seq RESTART WITH 1;"))
                    
                    trans.commit()
                    return  # Успешно выполнено
                except Exception as e:
                    trans.rollback()
                    raise e
        except OperationalError as e:
            if "deadlock detected" in str(e).lower() and attempt < max_retries - 1:
                print(f"🔄 Deadlock detected, retrying ({attempt + 1}/{max_retries})...")
                time.sleep(delay * (2 ** attempt))  # Экспоненциальная задержка
                continue
            else:
                raise e
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"🔄 Database error, retrying ({attempt + 1}/{max_retries}): {e}")
                time.sleep(delay * (2 ** attempt))
                continue
            else:
                raise e

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Очищает данные в базе данных перед каждым тестом"""
    clean_database_with_retry()

@pytest.fixture(scope="module")
def client(test_app):
    return TestClient(test_app)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def auth_headers(client):
    # Регистрация пользователя
    user_data = {
        "full_name": "Test User",
        "email": f"test{random.randint(1000, 9999)}@example.com",
        "username": f"user{random.randint(1000, 9999)}",
        "password": "Testpassword123!"
    }
    client.post("/auth/register", json=user_data)
    
    # Логин
    login_data = {"email": user_data["email"], "password": user_data["password"]}
    response = client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Тесты
class TestAuthFlow:
    def test_register_login_flow(self, client):
        # Регистрация
        user_data = {
            "full_name": "Test User",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "username": f"user{random.randint(1000, 9999)}",
            "password": "Testpassword1234!"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200
        
        # Логин
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()

class TestUserProfile:
    def test_user_data_flow(self, client):
        # 1. Регистрация нового пользователя
        user_data = {
            "full_name": "Test User",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "username": f"user{random.randint(1000, 9999)}",
            "password": "Testpassword123!"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200

        # 2. Логин пользователя
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        # Получаем токен с проверкой
        login_json = login_response.json()
        assert "access_token" in login_json, f"Token not found in response: {login_json}"
        headers = {"Authorization": f"Bearer {login_json['access_token']}"}

        # 3. Обновление профиля
        profile_data = {
            "full_name": "Updated Name",
            "country": "kz",
            "city": "Almaty",
            "training_profile": {
                "basic_information": {
                    "gender": "male",
                    "age": 30,
                    "height_cm": 180,
                    "weight_kg": 75.5
                },
                "training_goals": ["muscle_gain"]
            }
        }
        response = client.post("/user-data", json=profile_data, headers=headers)
        assert response.status_code == 200

        # 4. Проверка обновленных данных
        response = client.get("/user-data", headers=headers)
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["full_name"] == "Updated Name"
        assert user_data["training_profile"]["basic_information"]["gender"] == "male"
        
class TestTrainingEndpoints:
    def test_training_crud_flow(self, client, auth_headers):
        # Создание тренировки
        training_data = {
            "title": "Morning Routine",
            "description": "Basic exercises",
            "duration": 30,
            "difficulty": "beginner"
        }
        response = client.post("/trainings/", json=training_data, headers=auth_headers)
        assert response.status_code == 200
        training_id = response.json()["id"]
        
        # Получение тренировки
        response = client.get(f"/trainings/{training_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Удаление
        response = client.delete(f"/trainings/{training_id}", headers=auth_headers)
        assert response.status_code == 200


class TestSurveyData:
    def test_survey_data_endpoint(self, client):
        response = client.get("/survey-data")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestStaticFiles:
    def test_static_files(self, client):
        response = client.get("/static/test.txt")
        assert response.status_code in [200, 404]


class TestTrainingProfile:
    def test_complete_training_profile(self, client):
        # 1. Регистрация и логин
        user_data = {
            "full_name": "Training User",
            "email": f"training{random.randint(1000, 9999)}@example.com",
            "username": f"trainer{random.randint(1000, 9999)}",
            "password": "Trainpass123!"
        }
        client.post("/auth/register", json=user_data)
        
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

        # 2. Полное обновление профиля тренировок
        profile_data = {
            "training_profile": {
                "basic_information": {
                    "gender": "female",
                    "age": 28,
                    "height_cm": 165,
                    "weight_kg": 60.0
                },
                "training_goals": ["improve_flexibility"],
                "training_experience": {
                    "level": "intermediate",
                    "frequency_last_3_months": "3_4_times_week"
                }
            }
        }
        response = client.post("/user-data", json=profile_data, headers=headers)
        assert response.status_code == 200
        
        # 3. Checking the saved data
        response = client.get("/user-data", headers=headers)
        assert response.status_code == 200
        assert "training_profile" in response.json()
        assert response.json()["training_profile"]["training_goals"] == ["improve_flexibility"]

class TestEdgeCases:
    def test_min_max_values(self, client):
        # 1. Регистрация нового пользователя
        user_data = {
            "full_name": "Edge Case User",
            "email": f"edge{random.randint(1000, 9999)}@example.com",
            "username": f"edgeuser{random.randint(1000, 9999)}",
            "password": "Edgepass123!"
        }
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 200

        # 2. Логин и получение токена
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}

        # 3. Тестирование граничных значений
        edge_case_data = {
            "training_profile": {
                "basic_information": {
                    "age": 13,  # минимальный возраст
                    "height_cm": 250,  # максимальный рост
                    "weight_kg": 300.0  # максимальный вес
                },
                "training_types": {
                    "strength_training": 1,  # минимальный уровень интереса
                    "cardio": 5  # максимальный уровень интереса
                }
            }
        }
        response = client.post("/user-data", json=edge_case_data, headers=headers)
        assert response.status_code == 200

        # 4. Проверка сохраненных значений
        get_response = client.get("/user-data", headers=headers)
        assert get_response.status_code == 200
        profile = get_response.json()["training_profile"]
        assert profile["basic_information"]["age"] == 13
        assert profile["basic_information"]["height_cm"] == 250
        assert profile["training_types"]["cardio"] == 5

    def test_empty_optional_fields(self, client):
        # 1. Регистрация нового пользователя
        user_data = {
            "full_name": "Minimal User",
            "email": f"minimal{random.randint(1000, 9999)}@example.com",
            "username": f"minimaluser{random.randint(1000, 9999)}",
            "password": "Minpass123!"
        }
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 200

        # 2. Логин и получение токена
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}

        # 3. Отправка минимальных данных
        minimal_data = {
            "full_name": "Minimal User",
            "training_profile": {
                "basic_information": {
                    "gender": "male"  # единственное обязательное поле
                }
            }
        }
        response = client.post("/user-data", json=minimal_data, headers=headers)
        assert response.status_code == 200

        # 4. Проверка сохраненных данных
        get_response = client.get("/user-data", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()["training_profile"]["basic_information"]["gender"] == "male"

class TestTrainingTypes:
    @pytest.mark.parametrize("interest_level", [1, 3, 5])
    def test_training_interest_levels(self, client, interest_level):
        #1. Registration and login
        user_data = {
            "full_name": f"User {interest_level}",
            "email": f"interest{interest_level}_{random.randint(1000, 9999)}@example.com",
            "username": f"interest_{interest_level}_{random.randint(1000, 9999)}",
            "password": "Testpass123!"
        }
        client.post("/auth/register", json=user_data)
        
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

        #2. Setting the interest level
        data = {
            "training_profile": {
                "training_types": {
                    "strength_training": interest_level,
                    "cardio": interest_level
                }
            }
        }
        response = client.post("/user-data", json=data, headers=headers)
        assert response.status_code == 200
        
        # 3. Checking the saved data
        response = client.get("/user-data", headers=headers)
        assert response.status_code == 200
        assert response.json()["training_profile"]["training_types"]["strength_training"] == interest_level

class TestHealthInformation:
    def test_health_details_length(self, client, auth_headers):
        long_description = "a" * 1000  # max length
        data = {
            "training_profile": {
                "health": {
                    "health_details": long_description
                }
            }
        }
        response = client.post("/user-data", json=data, headers=auth_headers)
        assert response.status_code == 200

    def test_empty_health_details(self, client, auth_headers):
        data = {
            "training_profile": {
                "health": {
                    "health_details": None
                }
            }
        }
        response = client.post("/user-data", json=data, headers=auth_headers)
        assert response.status_code == 200

class TestCountryCityMapping:
    @pytest.mark.parametrize("country,city", [
        ("kz", "Almaty"),
        ("ru", "Moscow"),
        ("us", "New York")
    ])
    def test_valid_country_city_combinations(self, client, auth_headers, country, city):
        data = {
            "country": country,
            "city": city
        }
        response = client.post("/user-data", json=data, headers=auth_headers)
        assert response.status_code == 200

class TestPartialUpdates:
    def test_update_single_field(self, client):
        # 1. Регистрация нового пользователя
        user_data = {
            "full_name": "Partial Update User",
            "email": f"partial{random.randint(1000, 9999)}@example.com",
            "username": f"partialuser{random.randint(1000, 9999)}",
            "password": "Testpass123!"
        }
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 200

        # 2. Логин и получение токена
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}

        # 3. Установка первоначальных данных
        initial_data = {
            "full_name": "Original Name",
            "country": "us",
            "city": "New York",
            "training_profile": {
                "basic_information": {
                    "gender": "male",
                    "age": 30
                }
            }
        }
        response = client.post("/user-data", json=initial_data, headers=headers)
        assert response.status_code == 200

        # 4. Частичное обновление только имени
        partial_data = {
            "full_name": "Updated Name Only"
        }
        response = client.post("/user-data", json=partial_data, headers=headers)
        assert response.status_code == 200

        # 5. Проверка, что остальные данные сохранились
        get_response = client.get("/user-data", headers=headers)
        assert get_response.status_code == 200
        user_data = get_response.json()
        assert user_data["full_name"] == "Updated Name Only"
        assert user_data["country"] == "us"
        assert user_data["city"] == "New York"
        assert user_data["training_profile"]["basic_information"]["gender"] == "male"
        assert user_data["training_profile"]["basic_information"]["age"] == 30

# tests/e2e/test_ui.py
import pytest
from playwright.sync_api import sync_playwright

