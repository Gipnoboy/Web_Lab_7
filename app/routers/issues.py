from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from database import get_db
from models import Issue, Book, Reader
from schemas import Issue, IssueCreate
from fastapi import Path, Query

router = APIRouter(prefix="/issues", tags=["Видачі"])

@router.post(
    "/",
    response_model=Issue,
    summary="Створити нову видачу",
    description="Реєструє видачу книги читачу"
)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    """Створює нову видачу в базі даних"""
    book = db.query(Book).filter(Book.id == issue.book_id).first()
    reader = db.query(Reader).filter(Reader.id == issue.reader_id).first()
    if not book or not reader:
        raise HTTPException(status_code=404, detail="Книга або читач не знайдені")
    db_issue = Issue(**issue.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

@router.get(
    "/",
    response_model=List[Issue],
    summary="Отримати список видач",
    description="Повертає список усіх видач із пагінацією"
)
def read_issues(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Отримує список видач"""
    issues = db.query(Issue).offset(skip).limit(limit).all()
    return issues

@router.get(
    "/{issue_id}",
    response_model=Issue,
    summary="Отримати видачу за ID",
    description="Повертає деталі видачі за ID"
)
def read_issue(issue_id: int = Path(..., description="Унікальний ID видачі"), db: Session = Depends(get_db)):
    """Отримує видачу за ID"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if issue is None:
        raise HTTPException(status_code=404, detail="Видача не знайдена")
    return issue

@router.put(
    "/return/{issue_id}",
    response_model=Issue,
    summary="Повернути книгу",
    description="Реєструє повернення книги та розраховує штраф (150 за прострочення > 14 днів)"
)
def return_book(
    issue_id: int = Path(..., description="Унікальний ID видачі"),
    return_date: date = Query(..., description="Дата повернення книги"),
    db: Session = Depends(get_db)
):
    """Реєструє повернення книги та розраховує штраф"""
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Видача не знайдена")
    db_issue.return_date = return_date
    # Розрахунок штрафу: 150, якщо повернення > 14 днів
    if db_issue.return_date and db_issue.return_date > db_issue.issue_date + timedelta(days=14):
        db_issue.fine = 150
    else:
        db_issue.fine = 0
    db.commit()
    db.refresh(db_issue)
    return db_issue