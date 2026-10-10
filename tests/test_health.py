from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from pymongo.errors import PyMongoError

from app.main import app, db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_uses_test_database():
    assert "attendance_test_db" in str(db.name)


def test_health_check_mongodb_unavailable():
    mock_client = MagicMock()
    mock_client.admin.command.side_effect = PyMongoError("MongoDB is unavailable")

    with patch("app.main.client", mock_client):
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "mongodb is not available",
    }
