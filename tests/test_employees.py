import uuid

import pytest

from app.main import db


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


def test_create_employee(client, employee_data):

    response = client.post("/employees", json=employee_data)

    assert db.employees.find_one({"emp_code": employee_data["emp_code"]}) is not None

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["emp_code"] == employee_data["emp_code"]
    assert response_data["name"] == employee_data["name"]
    assert response_data["email"] == employee_data["email"]
    assert response_data["department"] == employee_data["department"]
    assert response_data["joined_on"] == employee_data["joined_on"]


def test_duplicate_employee(client, employee_data):

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


def test_missing_field(client, missing_field_employee_data):

    response = client.post("/employees", json=missing_field_employee_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
