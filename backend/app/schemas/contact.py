# backend/app/schemas/contact.py
"""Contact schemas"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ContactCreate(BaseModel):
    contact_type: str = Field(..., pattern=r"^(applicant|patient)$")
    industry: str = Field(..., pattern=r"^(immigration|healthcare)$")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    phone_secondary: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = "Canada"
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    notes: Optional[str] = None
    industry_fields: Dict[str, Any] = {}
    tags: List[str] = []
    assigned_to: Optional[str] = None
    source: Optional[str] = None


class ContactResponse(BaseModel):
    id: str
    tenant_id: str
    contact_type: str
    industry: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    industry_fields: Dict[str, Any] = {}
    tags: List[str] = []
    assigned_to: Optional[str] = None
    status: str
    created_at: datetime


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    industry_fields: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
