import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

def test_create_issue(client: TestClient, test_db):
    """Тестує створення видачі"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    response = client.post(
        "/issues/",
        json={
            "book_id": 1,
            "reader_id": 1,
            "issue_date": "2025-04-28",
            "return_date": None,
            "fine": 0
        }
    )
    assert response.status_code == 200
    assert response.json()["book_id"] == 1

def test_read_issues(client: TestClient, test_db):
    """Тестує отримання списку видач"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    client.post("/issues/", json={
        "book_id": 1,
        "reader_id": 1,
        "issue_date": "2025-04-28",
        "return_date": None,
        "fine": 0
    })
    response = client.get("/issues/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_return_book_with_fine(client: TestClient, test_db):
    """Тестує повернення книги з штрафом"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    client.post("/issues/", json={
        "book_id": 1,
        "reader_id": 1,
        "issue_date": "2025-04-01",
        "return_date": None,
        "fine": 0
    })
    # Повернення через 15 днів (штраф 150)
    response = client.put("/issues/return/1?return_date=2025-04-16")
    assert response.status_code == 200
    assert response.json()["fine"] == 150

def test_return_book_no_fine(client: TestClient, test_db):
    """Тестує повернення книги без штрафу"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    client.post("/readers/", json={"name": "Іван Петров", "email": "ivan@example.com"})
    client.post("/issues/", json={
        "book_id": 1,
        "reader_id": 1,
        "issue_date": "2025-04-01",
        "return_date": None,
        "fine": 0
    })
    # Повернення до 14 днів (без штрафу)
    response = client.put("/issues/return/1?return_date=2025-04-10")
    assert response.status_code == 200
    assert response.json()["fine"] == 0