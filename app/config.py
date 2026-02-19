from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./dev_studio.db"
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Telegram
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    telegram_enabled: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

