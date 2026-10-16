import sqlite3

import pytest

import app


@pytest.fixture
def client(monkeypatch):
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT,
            location TEXT,
            role TEXT
        )
        """
    )
    connection.commit()

    monkeypatch.setattr(app, "conn", connection)
    monkeypatch.setattr(app, "cursor", cursor)

    with app.app.test_client() as test_client:
        yield test_client

    connection.close()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_get_employees_returns_empty_list(client):
    response = client.get("/employees")

    assert response.status_code == 200
    assert response.get_json() == []


def test_post_employee_and_get_employee(client):
    employee = {
        "name": "Alex Smith",
        "start_date": "2026-01-01",
        "location": "London",
        "role": "Barista",
    }

    post_response = client.post("/employees", json=employee)
    get_response = client.get("/employees")

    assert post_response.status_code == 201
    assert (
        post_response.get_data(as_text=True)
        == "Employee added successfully"
    )
    assert get_response.get_json() == [
        [1, "Alex Smith", "2026-01-01", "London", "Barista"]
    ]
