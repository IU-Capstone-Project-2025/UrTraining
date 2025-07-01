import sys
import os
import pytest
import random
from fastapi.testclient import TestClient
import pytest
from fastapi import status

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """Фикстура для получения auth headers"""
    # Регистрируем тестового пользователя
    suffix = random.randint(1000, 9999)
    user_data = {
        "full_name": f"Тестовый Пользователь {suffix}",
        "email": f"test{suffix}@example.com",
        "username": f"test_user{suffix}",
        "password": "testpassword"
    }
    client.post("/auth/register", json=user_data)
    
    # Логинимся и получаем токен
    login_response = client.post("/auth/login", 
        data={"username": user_data["username"], "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def trainer_headers(client, auth_headers):
    """Фикстура для получения headers тренера"""
    # Создаем профиль тренера
    trainer_data = {
        "specialization": "fitness",
        "experience_years": 3,
        "certification": "ACE Certified",
        "bio": "Professional trainer"
    }
    client.post("/trainer-profile", json=trainer_data, headers=auth_headers)
    return auth_headers


# Тесты для регистрации и аутентификации
def test_register_user_success(client):
    """Успешная регистрация пользователя"""
    suffix = random.randint(1000, 9999)
    response = client.post("/auth/register", json={
        "full_name": f"Иван Иванов {suffix}",
        "email": f"ivan{suffix}@example.com",
        "username": f"ivan{suffix}",
        "password": "securepassword123"
    })
    
    assert response.status_code in [200, 201]
    response_data = response.json()
    assert "message" in response_data or "detail" in response_data
    if "message" in response_data:
        assert "success" in response_data["message"].lower()
    assert "user_info" in response_data or "id" in response_data

def test_register_existing_username(client):
    """Регистрация с существующим username"""
    client.post("/auth/register", json={
        "full_name": "Тест",
        "email": "test1@example.com",
        "username": "testuser",
        "password": "password"
    })
    
    response = client.post("/auth/register", json={
        "full_name": "Тест",
        "email": "test2@example.com",
        "username": "testuser",
        "password": "password"
    })
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "username already exists" in response.json()["detail"]

def test_register_existing_email(client):
    """Регистрация с существующим email"""
    client.post("/auth/register", json={
        "full_name": "Тест",
        "email": "test@example.com",
        "username": "test1",
        "password": "password"
    })
    
    response = client.post("/auth/register", json={
        "full_name": "Тест",
        "email": "test@example.com",
        "username": "test2",
        "password": "password"
    })
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Email already registered" in response.json()["detail"]

def test_register_invalid_data(client):
    """Регистрация с неполными данными"""
    response = client.post("/auth/register", json={
        "full_name": "Тест",
        "username": "testuser",
        "password": "password"
    })
    
    assert response.status_code in [400, 422]



def test_login_wrong_password(client):
    """Неверный пароль"""
    suffix = random.randint(1000, 9999)
    user_data = {
        "full_name": f"Тестовый Пользователь {suffix}",
        "email": f"wrong_pass_test{suffix}@example.com",
        "username": f"wrong_pass_user{suffix}",
        "password": "correctpassword"
    }
    
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/login",
        data={"username": user_data["username"], "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()

def test_login_nonexistent_user(client):
    """Попытка входа несуществующего пользователя"""
    response = client.post("/auth/login",
        data={"username": "nonexistent_user_12345", "password": "anypassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()



# Тесты для профиля тренера


# Исправленные тесты для профиля тренера (синхронные)



def test_get_trainer_profile_not_found(client, auth_headers):
    """Профиль тренера не найден"""
    response = client.get("/trainer-profile", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json().get("detail", "").lower()




def test_update_trainer_profile_unauthorized(client):
    """Попытка обновления без авторизации"""
    response = client.put("/trainer-profile", json={"trainer_profile": {}})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_trainer_profile_twice(client, trainer_headers):
    """Повторное удаление уже удаленного профиля"""
    # Первое удаление
    client.delete("/trainer-profile", headers=trainer_headers)
    
    # Второе удаление
    response = client.delete("/trainer-profile", headers=trainer_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_trainer_profile_unauthorized(client):
    """Попытка удаления без авторизации"""
    response = client.delete("/trainer-profile")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_training_unauthorized(client):
    """Попытка создания без авторизации"""
    response = client.post("/trainings/", json={"course_title": "Test"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_nonexistent_training(client, auth_headers):
    """Попытка обновления несуществующей программы"""
    response = client.put(
        "/trainings/nonexistent-id",
        json={"course_title": "Test"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Тесты для удаления программы
def test_delete_training_twice(client, auth_headers):
    """Повторное удаление программы"""
    create_resp = client.post("/trainings/", json={"course_title": "Test"}, headers=auth_headers)
    training_id = create_resp.json()
    
    # Первое удаление
    client.delete(f"/trainings/{training_id}", headers=auth_headers)
    
    # Второе удаление
    response = client.delete(f"/trainings/{training_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Тесты для проверки прав создания


def test_can_create_training_unauthorized(client):
    """Проверка прав создания без авторизации"""
    response = client.get("/trainings/can-create")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Фикстуры для тестов
@pytest.fixture
def another_auth_headers(client):
    """Фикстура для headers другого пользователя"""
    user_data = {
        "full_name": "Another User",
        "email": "another@example.com",
        "username": "anotheruser",
        "password": "anotherpass"
    }
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
