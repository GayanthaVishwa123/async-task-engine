import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tasks import celery_app

client = TestClient(app)

# Force Celery to run synchronously during testing phases
celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_critical_notification_success():
    payload = {"email": "gayantha@example.com", "message": "Critical Alert!"}
    response = client.post("/notify/critical", json=payload)
    assert response.status_code == 200
    assert "Queued in high_priority" in response.json()["status"]


def test_critical_notification_invalid_email():
    payload = {"email": "invalid-email-format", "message": "Alert!"}
    response = client.post("/notify/critical", json=payload)
    # Pydantic EmailStr triggers 422 automatically
    assert response.status_code == 422


def test_bulk_notification_success():
    payload = {
        "emails": ["user1@example.com", "user2@example.com"],
        "message": "Weekly Newsletter",
    }
    response = client.post("/notify/bulk", json=payload)
    assert response.status_code == 200
    assert "Queued in low_priority" in response.json()["status"]
