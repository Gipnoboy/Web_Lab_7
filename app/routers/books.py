from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Book
from schemas import Book, BookCreate
from fastapi import Path

router = APIRouter(prefix="/books", tags=["Книги"])

@router.post(
    "/",
    response_model=Book,
    summary="Створити нову книгу",
    description="Додає нову книгу до бібліотеки",
    responses={
        200: {"description": "Книга успішно створена"},
        422: {"description": "Невалідні дані"}
    }
)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Створює нову книгу в базі даних"""
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get(
    "/",
    response_model=List[Book],
    summary="Отримати список книг",
    description="Повертає список книг із підтримкою пагінації"
)
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Отримує список книг із бази даних"""
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Отримати книгу за ID",
    description="Повертає деталі книги за її унікальним ідентифікатором",
    responses={
        200: {"description": "Книга знайдена"},
        404: {"description": "Книга не знайдена"}
    }
)
def read_book(book_id: int = Path(..., description="Унікальний ID книги"), db: Session = Depends(get_db)):
    """Отримує книгу за ID"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    return book

@router.put(
    "/{book_id}",
    response_model=Book,
    summary="Оновити книгу",
    description="Оновлює дані книги за її ID",
    responses={
        200: {"description": "Книга оновлена"},
        404: {"description": "Книга не знайдена"}
    }
)
def update_book(book_id: int = Path(..., description="Унікальний ID книги"), book: BookCreate, db: Session = Depends(get_db)):
    """Оновлює дані книги"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete(
    "/{book_id}",
    summary="Видалити книгу",
    description="Видаляє книгу за її ID",
    responses={
        200: {"description": "Книга видалена"},
        404: {"description": "Книга не знайдена"}
    }
)
def delete_book(book_id: int = Path(..., description="Унікальний ID книги"), db: Session = Depends(get_db)):
    """Видаляє книгу з бази даних"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    db.delete(db_book)
    db.commit()
    return {"detail": "Книга видалена"}