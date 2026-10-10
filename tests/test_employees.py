import uuid
from concurrent.futures import ThreadPoolExecutor

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


def test_invalid_shift_time_format(client, employee_data):
    employee_data["shift_start"] = "9:30"

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 422
    assert db.employees.find_one({"emp_code": employee_data["emp_code"]}) is None


def test_shift_start_and_end_same(client, employee_data):
    employee_data["shift_start"] = "09:30"
    employee_data["shift_end"] = "09:30"

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 422
    assert db.employees.find_one({"emp_code": employee_data["emp_code"]}) is None


def test_duplicate_employee_creates_exactly_one_success(client, employee_data):
    number_of_requests = 10

    def create_employee(_):
        response = client.post("/employees", json=employee_data)
        return response.status_code

    try:
        with ThreadPoolExecutor(max_workers=number_of_requests) as executor:
            statuses = list(executor.map(create_employee, range(number_of_requests)))

        assert statuses.count(201) == 1
        assert statuses.count(409) == number_of_requests - 1

        assert (
            db.employees.count_documents({"emp_code": employee_data["emp_code"]}) == 1
        )

    finally:
        db.employees.delete_many({"emp_code": employee_data["emp_code"]})
