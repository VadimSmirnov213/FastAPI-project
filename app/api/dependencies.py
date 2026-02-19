from sqlalchemy.orm import Session
from app.database import get_db


def get_database() -> Session:
    """Dependency для получения сессии БД"""
    return next(get_db())

