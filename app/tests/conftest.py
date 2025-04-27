import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base
from database import get_db

# Тестова база даних
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Перевизначення залежності для тестів
def override_get_db():
    """Надає тестову сесію бази даних"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    """Створює та очищає тестову базу даних для кожного тесту"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Надає тестовий клієнт FastAPI"""
    return TestClient(app)