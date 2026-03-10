from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    """Helper to register and login, returns JWT token"""
    client.post("/auth/register", json={
        "email": "logstest@example.com",
        "password": "TestPassword123"
    })
    response = client.post("/auth/login", json={
        "email": "logstest@example.com",
        "password": "TestPassword123"
    })
    return response.json()["access_token"]


def test_create_log():
    token = get_token()
    response = client.post("/logs/", json={
        "title": "Built JWT auth system",
        "description": "Implemented login and register endpoints",
        "language": "python",
        "duration_minutes": 90,
        "mood": "focused",
        "tags": "auth, jwt, fastapi"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == "Built JWT auth system"


def test_get_logs():
    token = get_token()
    response = client.get("/logs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_logs_with_pagination():
    token = get_token()
    response = client.get("/logs/?page=1&limit=5", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) <= 5


def test_get_logs_filter_by_language():
    token = get_token()
    client.post("/logs/", json={
        "title": "Python project",
        "language": "python"
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/logs/?language=python", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    for log in response.json():
        assert "python" in log["language"].lower()


def test_update_log():
    token = get_token()
    create = client.post("/logs/", json={
        "title": "Original title",
        "language": "python"
    }, headers={"Authorization": f"Bearer {token}"})
    log_id = create.json()["id"]

    response = client.patch(f"/logs/{log_id}", json={
        "title": "Updated title"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


def test_delete_log():
    token = get_token()
    create = client.post("/logs/", json={
        "title": "Log to delete",
        "language": "java"
    }, headers={"Authorization": f"Bearer {token}"})
    log_id = create.json()["id"]

    response = client.delete(f"/logs/{log_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204


def test_get_nonexistent_log():
    token = get_token()
    response = client.get("/logs/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_unauthorized_access():
    response = client.get("/logs/")
    assert response.status_code == 403