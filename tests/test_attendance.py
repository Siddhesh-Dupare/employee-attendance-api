from app.main import db


def test_uses_test_database():
    assert "attendance_test_db" in str(db.name)


def test_punch_in(client, employee_data):
    employee_response = client.post("/employees", json=employee_data)
    assert employee_response.status_code == 201

    response = client.post(
        "/attendance/punch-in",
        json={
            "emp_code": employee_data["emp_code"],
        },
    )

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["emp_code"] == employee_data["emp_code"]
    assert response_data["status"] == "PRESENT"

    attendance = db.attendance_logs.find_one({"emp_code": employee_data["emp_code"]})

    assert attendance is not None
    assert attendance["status"] == "PRESENT"
