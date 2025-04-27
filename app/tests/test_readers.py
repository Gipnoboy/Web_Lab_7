import pytest
from fastapi.testclient import TestClient

def test_create_reader(client: TestClient, test_db):
    """Тестує створення читача"""
    response = client.post(
        "/readers/",
        json={"name": "Іван Петров", "email": "ivan@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Іван Петров",
        "email": "ivan@example.com"
    }

def test_read_readers(client: TestClient, test_db):
    """Тестує отримання списку читачів"""
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    response = client.get("/readers/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Іван Петров"

def test_read_reader(client: TestClient, test_db):
    """Тестує отримання читача за ID"""
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    response = client.get("/readers/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_reader(client: TestClient, test_db):
    """Тестує оновлення читача"""
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    response = client.put(
        "/readers/1",
        json={"name": "Петро Іванов", "email": "petro@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Петро Іванов"

def test_delete_reader(client: TestClient, test_db):
    """Тестує видалення читача"""
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    response = client.delete("/readers/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Читач видалений"}