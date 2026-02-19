from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Project Schemas
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    long_description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    year: str = Field(..., min_length=4, max_length=4)
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    github: Optional[str] = None
    is_featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    long_description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[str] = Field(None, min_length=4, max_length=4)
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    github: Optional[str] = None
    is_featured: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Contact Schemas
class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    message: str = Field(..., min_length=1)


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Health Check
class HealthResponse(BaseModel):
    status: str
    message: str

