import pytest
from fastapi.testclient import TestClient

def test_create_book(client: TestClient, test_db):
    """Тестує створення книги"""
    response = client.post(
        "/books/",
        json={"title": "1984", "author": "Джордж Орвелл"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "1984",
        "author": "Джордж Орвелл"
    }

def test_read_books(client: TestClient, test_db):
    """Тестує отримання списку книг"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "1984"

def test_read_book(client: TestClient, test_db):
    """Тестує отримання книги за ID"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_book(client: TestClient, test_db):
    """Тестує оновлення книги"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    response = client.put(
        "/books/1",
        json={"title": "Animal Farm", "author": "Джордж Орвелл"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Animal Farm"

def test_delete_book(client: TestClient, test_db):
    """Тестує видалення книги"""
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл"})
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Книга видалена"}