from fastapi.testclient import TestClient

from app.main import app, db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_uses_test_database():
    assert "attendance_test_db" in str(db.name)
