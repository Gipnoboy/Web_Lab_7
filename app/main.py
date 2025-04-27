from fastapi import FastAPI, Request
from database import engine, Base
from routers import books, readers, issues
import logging
from logging_config import setup_logging
from time import time

# Налаштування логування
setup_logging()
logger = logging.getLogger("api_requests")

# Ініціалізація FastAPI із назвою та описом для документації
app = FastAPI(
    title="Система управління бібліотекою",
    description="API для управління книгами, читачами, видачами та резервуваннями",
    version="1.0.0"
)

# Створення таблиць у базі даних
Base.metadata.create_all(bind=engine)

# Підключення маршрутів
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(issues.router)

# Мідлвар для логування запитів
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логує деталі HTTP-запиту та відповіді"""
    start_time = time()
    logger.info(f"Запит: {request.method} {request.url}")
    response = await call_next(request)
    duration = time() - start_time
    logger.info(f"Відповідь: статус={response.status_code}, час={duration:.3f}с")
    return response

@app.get(
    "/",
    summary="Кореневий ендпоінт",
    description="Повертає привітальне повідомлення системи"
)
async def root():
    """Повертає привітальне повідомлення"""
    return {"message": "Ласкаво просимо до системи управління бібліотекою"}