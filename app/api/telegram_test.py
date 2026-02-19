from fastapi import APIRouter, HTTPException
from app.telegram import send_telegram_message
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.get("/test")
def test_telegram():
    """Тестовый эндпоинт для проверки отправки сообщений в Telegram"""
    # Проверяем настройки
    config_status = {
        "telegram_enabled": settings.telegram_enabled,
        "has_bot_token": bool(settings.telegram_bot_token),
        "has_chat_id": bool(settings.telegram_chat_id),
        "bot_token_preview": f"{settings.telegram_bot_token[:10]}..." if settings.telegram_bot_token else None,
        "chat_id": settings.telegram_chat_id
    }
    
    if not settings.telegram_enabled:
        return {
            "status": "disabled",
            "message": "Telegram notifications are disabled. Set TELEGRAM_ENABLED=true in .env",
            "config": config_status
        }
    
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return {
            "status": "not_configured",
            "message": "Telegram bot token or chat ID not configured",
            "config": config_status,
            "instructions": {
                "1": "Create a bot via @BotFather in Telegram",
                "2": "Get your chat ID via @userinfobot",
                "3": "Add to .env file:",
                "env_example": "TELEGRAM_BOT_TOKEN=your_token\nTELEGRAM_CHAT_ID=your_chat_id\nTELEGRAM_ENABLED=true"
            }
        }
    
    # Пытаемся отправить тестовое сообщение
    test_message = "🧪 <b>Тестовое сообщение</b>\n\nЭто тестовое сообщение для проверки работы Telegram интеграции."
    
    success = send_telegram_message(test_message)
    
    if success:
        return {
            "status": "success",
            "message": "Test message sent successfully! Check your Telegram.",
            "config": config_status
        }
    else:
        return {
            "status": "failed",
            "message": "Failed to send test message. Check server logs for details.",
            "config": config_status,
            "troubleshooting": {
                "1": "Verify bot token is correct",
                "2": "Verify chat ID is correct (must be numeric)",
                "3": "Make sure you started a conversation with your bot",
                "4": "Check server logs for detailed error messages"
            }
        }


@router.get("/config")
def get_telegram_config():
    """Получить текущую конфигурацию Telegram (без секретных данных)"""
    return {
        "telegram_enabled": settings.telegram_enabled,
        "has_bot_token": bool(settings.telegram_bot_token),
        "has_chat_id": bool(settings.telegram_chat_id),
        "chat_id": settings.telegram_chat_id if settings.telegram_chat_id else None
    }

