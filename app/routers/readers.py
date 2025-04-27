from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Reader
from schemas import Reader, ReaderCreate
from fastapi import Path

router = APIRouter(prefix="/readers", tags=["Читачі"])

@router.post(
    "/",
    response_model=Reader,
    summary="Створити нового читача",
    description="Додає нового читача до системи"
)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    """Створює нового читача в базі даних"""
    db_reader = Reader(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.get(
    "/",
    response_model=List[Reader],
    summary="Отримати список читачів",
    description="Повертає список читачів із пагінацією"
)
def read_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Отримує список читачів"""
    readers = db.query(Reader).offset(skip).limit(limit).all()
    return readers

@router.get(
    "/{reader_id}",
    response_model=Reader,
    summary="Отримати читача за ID",
    description="Повертає деталі читача за ID"
)
def read_reader(reader_id: int = Path(..., description="Унікальний ID читача"), db: Session = Depends(get_db)):
    """Отримує читача за ID"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читач не знайдений")
    return reader

@router.put(
    "/{reader_id}",
    response_model=Reader,
    summary="Оновити читача",
    description="Оновлює дані читача за ID"
)
def update_reader(reader_id: int = Path(..., description="Унікальний ID читача"), reader: ReaderCreate, db: Session = Depends(get_db)):
    """Оновлює дані читача"""
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Читач не знайдений")
    for key, value in reader.dict().items():
        setattr(db_reader, key, value)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.delete(
    "/{reader_id}",
    summary="Видалити читача",
    description="Видаляє читача за ID"
)
def delete_reader(reader_id: int = Path(..., description="Унікальний ID читача"), db: Session = Depends(get_db)):
    """Видаляє читача з бази даних"""
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Читач не знайдений")
    db.delete(db_reader)
    db.commit()
    return {"detail": "Читач видалений"}