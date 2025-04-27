from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL бази даних для продакшену
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db"

# Створення двигуна для бази даних
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Фабрика сесій для взаємодії з базою
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()

def get_db():
    """Надає сесію бази даних для залежностей"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()