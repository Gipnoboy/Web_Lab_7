from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    """Модель для зберігання даних про книги"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Назва книги
    author = Column(String)  # Автор книги

class Reader(Base):
    """Модель для зберігання даних про читачів"""
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # Ім'я читача
    email = Column(String, unique=True)  # Унікальна email-адреса

class Issue(Base):
    """Модель для зберігання даних про видачі книг"""
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))  # ID книги
    reader_id = Column(Integer, ForeignKey("readers.id"))  # ID читача
    issue_date = Column(Date)  # Дата видачі
    return_date = Column(Date, nullable=True)  # Дата повернення
    fine = Column(Integer, default=0)  # Штраф за прострочення

    book = relationship("Book")  # Зв'язок із книгою
    reader = relationship("Reader")  # Зв'язок із читачем

class Reservation(Base):
    """Модель для зберігання даних про резервування книг"""
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))  # ID книги
    reader_id = Column(Integer, ForeignKey("readers.id"))  # ID читача
    reservation_date = Column(Date)  # Дата резервування

    book = relationship("Book")  # Зв'язок із книгою
    reader = relationship("Reader")  # Зв'язок із читачем