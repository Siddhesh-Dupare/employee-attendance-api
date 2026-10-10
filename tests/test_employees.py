import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app, db

client = TestClient(app)


@pytest.fixture
def employee_data():
    data = {
        "emp_code": str(uuid.uuid4()),
        "name": "Test Employee",
        "email": "test@gmail.com",
        "department": "Engineering",
        "joined_on": "2026-10-10",
    }

    yield data
    db.employees.delete_one({"emp_code": data["emp_code"]})


@pytest.fixture
def missing_field_employee_data():
    data = {
        "emp_code": str(uuid.uuid4()),
        "name": "Test Employee",
    }

    yield data
    db.employees.delete_one({"emp_code": data["emp_code"]})


def test_uses_test_database():

    assert "attendance_test_db" in str(db.name)


def test_create_employee(employee_data):

    print("Created employee code:", employee_data["emp_code"])

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["emp_code"] == employee_data["emp_code"]
    assert response_data["name"] == employee_data["name"]
    assert response_data["email"] == employee_data["email"]
    assert response_data["department"] == employee_data["department"]
    assert response_data["joined_on"] == employee_data["joined_on"]


def test_duplicate_employee(employee_data):

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["emp_code"] == employee_data["emp_code"]
    assert response_data["name"] == employee_data["name"]
    assert response_data["email"] == employee_data["email"]
    assert response_data["department"] == employee_data["department"]
    assert response_data["joined_on"] == employee_data["joined_on"]

    response = client.post("/employees", json=employee_data)
    assert response.status_code == 409


def test_missing_field(missing_field_employee_data):

    response = client.post("/employees", json=missing_field_employee_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
