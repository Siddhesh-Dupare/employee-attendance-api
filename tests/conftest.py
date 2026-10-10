import os

import pytest
from fastapi.testclient import TestClient

os.environ["MONGO_DB"] = "attendance_test_db"


@pytest.fixture
def client():
    from app.main import app

    return TestClient(app)
