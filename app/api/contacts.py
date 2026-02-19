from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from app import schemas, models
from app.api.dependencies import get_database
from app.telegram import send_telegram_message, format_contact_message

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_database)):
    """Создать новое обращение из контактной формы"""
    db_contact = models.Contact(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        message=contact.message
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    try:
        contact_data = {
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "message": contact.message
        }
        telegram_message = format_contact_message(contact_data)
        logger.info("Attempting to send Telegram notification for new contact")
        success = send_telegram_message(telegram_message)
        if success:
            logger.info("Telegram notification sent successfully")
        else:
            logger.warning("Failed to send Telegram notification (check logs above for details)")
    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        logger.error(f"Exception while sending Telegram notification: {e}", exc_info=True)
    
    return db_contact


@router.get("/", response_model=List[schemas.ContactResponse])
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    db: Session = Depends(get_database)
):
    """Получить список обращений (для админки)"""
    query = db.query(models.Contact)
    
    if unread_only:
        query = query.filter(models.Contact.is_read == False)
    
    contacts = query.order_by(models.Contact.created_at.desc()).offset(skip).limit(limit).all()
    return contacts


@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_database)):
    """Получить обращение по ID"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact


@router.patch("/{contact_id}/read", response_model=schemas.ContactResponse)
def mark_as_read(contact_id: int, db: Session = Depends(get_database)):
    """Отметить обращение как прочитанное"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    contact.is_read = True
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_database)):
    """Удалить обращение"""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    return None

