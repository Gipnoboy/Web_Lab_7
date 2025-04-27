from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    """Базова схема для книги"""
    title: str = Field(..., min_length=3, max_length=50, description="Назва книги")
    author: str = Field(..., min_length=3, max_length=50, description="Автор книги")

class BookCreate(BookBase):
    """Схема для створення книги"""
    pass

class Book(BookBase):
    """Схема для повернення книги з ID"""
    id: int

    class Config:
        from_attributes = True

class ReaderBase(BaseModel):
    """Базова схема для читача"""
    name: str = Field(..., min_length=3, max_length=50, description="Ім'я читача")
    email: EmailStr = Field(..., description="Email-адреса читача")

class ReaderCreate(ReaderBase):
    """Схема для створення читача"""
    pass

class Reader(ReaderBase):
    """Схема для повернення читача з ID"""
    id: int

    class Config:
        from_attributes = True

class IssueBase(BaseModel):
    """Базова схема для видачі книги"""
    book_id: int = Field(..., description="ID книги")
    reader_id: int = Field(..., description="ID читача")
    issue_date: date = Field(..., description="Дата видачі")
    return_date: Optional[date] = Field(None, description="Дата повернення")
    fine: int = Field(0, description="Штраф за прострочення")

class IssueCreate(IssueBase):
    """Схема для створення видачі"""
    pass

class Issue(IssueBase):
    """Схема для повернення видачі з ID"""
    id: int

    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    """Базова схема для резервування"""
    book_id: int = Field(..., description="ID книги")
    reader_id: int = Field(..., description="ID читача")
    reservation_date: date = Field(..., description="Дата резервування")

class ReservationCreate(ReservationBase):
    """Схема для створення резервування"""
    pass

class Reservation(ReservationBase):
    """Схема для повернення резервування з ID"""
    id: int

    class Config:
        from_attributes = True