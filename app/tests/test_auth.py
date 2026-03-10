from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DevLog API" in response.json()["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    import uuid
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": "TestPassword123"
    })
    assert response.status_code == 201
    assert "user_id" in response.json()


def test_register_duplicate_email():
    # Register once
    client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "TestPassword123"
    })
    # Register again with same email
    response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "TestPassword123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    client.post("/auth/register", json={
        "email": "logintest@example.com",
        "password": "TestPassword123"
    })
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "TestPassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    client.post("/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "TestPassword123"
    })
    response = client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "WrongPassword"
    })
    assert response.status_code == 401