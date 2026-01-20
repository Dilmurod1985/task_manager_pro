import pytest
from httpx import AsyncClient
from app.main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker

# Создаём тестовую БД
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager Pro работает!"}
def test_register_and_login(test_client):
    # Регистрация
    response = test_client.post("/register", json={"username": "testuser", "password": "secret"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    # Логин
    response = test_client.post("/login", json={"username": "testuser", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
def test_task_crud(test_client):
    # Логин и получение токена
    login = test_client.post("/login", json={"username": "testuser", "password": "secret"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Создание задачи
    response = test_client.post("/tasks", json={"title": "Test Task", "description": "Demo"}, headers=headers)
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Получение задач
    response = test_client.get("/tasks", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Обновление задачи
    response = test_client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Changed"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

    # Удаление задачи
    response = test_client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Задача удалена"
