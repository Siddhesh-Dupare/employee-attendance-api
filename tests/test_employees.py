from fastapi.testclient import TestClient

from app.main import app, db

client = TestClient(app)


def test_uses_test_database():
    assert "attendance_test_db" in str(db.name)


# def test_create_employee():
#     employee_data = {
#         "emp_code": "E001",
#         "name": "Test Employee",
#         "email": "test@gmail.com",
#         "department": "Engineering",
#         "joined_on": "2026-10-10",
#     }
#
#     response = client.post("/employees", json=employee_data)
#
#     assert response.status_code == 201
#
#     response_data = response.json()
#     assert response_data["emp_code"] == employee_data["emp_code"]
#     assert response_data["name"] == employee_data["name"]
#     assert response_data["email"] == employee_data["email"]
#     assert response_data["department"] == employee_data["department"]
#     assert response_data["joined_on"] == employee_data["joined_on"]


def test_duplicate_employee():
    employee_data = {
        "emp_code": "E002",
        "name": "Test Employee",
        "email": "test@gmail.com",
        "department": "Engineering",
        "joined_on": "2026-10-10",
    }

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["emp_code"] == employee_data["emp_code"]
    assert response_data["name"] == employee_data["name"]
    assert response_data["email"] == employee_data["email"]
    assert response_data["department"] == employee_data["department"]
    assert response_data["joined_on"] == employee_data["joined_on"]

    new_employee_data = {
        "emp_code": "E002",
        "name": "Test Employee 2",
        "email": "test@gmail.com",
        "department": "Engineering",
        "joined_on": "2026-10-10",
    }

    response = client.post("/employees", json=new_employee_data)
    assert response.status_code == 409
