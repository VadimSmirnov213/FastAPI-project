import requests
import logging
from app.config import settings

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot"


def send_telegram_message(message: str) -> bool:
    """
    Отправляет сообщение в Telegram
    
    Args:
        message: Текст сообщения для отправки
        
    Returns:
        True если сообщение отправлено успешно, False в противном случае
    """
    logger.info(f"Attempting to send Telegram message. Enabled: {settings.telegram_enabled}")
    
    if not settings.telegram_enabled:
        logger.warning("Telegram notifications are disabled. Set TELEGRAM_ENABLED=true in .env file")
        return False
    
    if not settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not configured in .env file")
        return False
    
    if not settings.telegram_chat_id:
        logger.error("TELEGRAM_CHAT_ID not configured in .env file")
        return False
    
    try:
        url = f"{TELEGRAM_API_URL}{settings.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": settings.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        logger.info(f"Sending message to Telegram. URL: {url.split('/bot')[0]}/bot***/sendMessage, Chat ID: {settings.telegram_chat_id}")
        
        response = requests.post(url, json=payload, timeout=10)
        
        # Логируем ответ для отладки
        logger.info(f"Telegram API response status: {response.status_code}")
        
        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            logger.error(f"Telegram API error: {error_data}")
            return False
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            logger.info("Telegram message sent successfully")
            return True
        else:
            logger.error(f"Telegram API returned error: {result.get('description', 'Unknown error')}")
            return False
        
    except requests.exceptions.Timeout:
        logger.error("Timeout while sending Telegram message")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                logger.error(f"Telegram API error details: {error_data}")
            except:
                logger.error(f"Telegram API error response: {e.response.text}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending Telegram message: {e}", exc_info=True)
        return False


def format_contact_message(contact_data: dict) -> str:
    """
    Форматирует данные контакта в сообщение для Telegram
    
    Args:
        contact_data: Словарь с данными контакта
        
    Returns:
        Отформатированное сообщение
    """
    message = "🔔 <b>Новая заявка с сайта</b>\n\n"
    message += f"👤 <b>Имя:</b> {contact_data.get('name', 'Не указано')}\n"
    message += f"📧 <b>Email:</b> {contact_data.get('email', 'Не указано')}\n"
    
    if contact_data.get('phone'):
        message += f"📱 <b>Телефон:</b> {contact_data.get('phone')}\n"
    
    message += f"\n💬 <b>Сообщение:</b>\n{contact_data.get('message', 'Не указано')}"
    
    return message

