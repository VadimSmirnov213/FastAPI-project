from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import settings
from app.database import init_db
from app.api import projects, contacts, health, telegram_test


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Инициализация приложения
app = FastAPI(
    title="Dev Studio API",
    description="Backend API for Dev Studio website",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация БД при старте
@app.on_event("startup")
async def startup_event():
    init_db()


# Подключение роутеров
app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(projects.router, prefix=settings.api_v1_prefix)
app.include_router(contacts.router, prefix=settings.api_v1_prefix)
app.include_router(telegram_test.router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "Dev Studio API",
        "version": "1.0.0",
        "docs": "/docs"
    }

