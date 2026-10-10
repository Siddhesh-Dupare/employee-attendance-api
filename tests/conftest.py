import os
import uuid

import pytest
from fastapi.testclient import TestClient

os.environ["MONGO_DB"] = "attendance_test_db"


@pytest.fixture
def client():
    from app.main import app

    return TestClient(app)


@pytest.fixture
def employee_data():
    from app.main import db

    data = {
        "emp_code": str(uuid.uuid4()),
        "name": "Test Employee",
        "email": "test@gmail.com",
        "department": "Engineering",
        "joined_on": "2026-10-10",
    }

    yield data
    db.employees.delete_one({"emp_code": data["emp_code"]})
    db.attendance_logs.delete_many({"emp_code": data["emp_code"]})
