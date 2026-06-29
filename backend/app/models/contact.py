# backend/app/models/contact.py
"""
Contact Model - Unified Applicants (Immigration) and Patients (Healthcare)
Industry-specific fields stored in embedded industry_fields dict
"""

from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class ContactType(str, Enum):
    APPLICANT = "applicant"
    PATIENT = "patient"


class ContactStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class Contact(Document):
    """Unified contact entity - Applicants or Patients."""

    tenant_id: str = Field(..., index=True)
    contact_type: ContactType
    industry: str = Field(..., description="immigration or healthcare")

    # === Base Fields ===
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    phone_secondary: Optional[str] = None

    # Address
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "Canada"

    # Profile
    avatar_url: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    notes: Optional[str] = None

    # Industry-specific fields (flexible schema)
    industry_fields: Dict[str, Any] = Field(default_factory=dict)

    # === Immigration-specific (stored in industry_fields) ===
    # passport_number, ircc_case_id, language_scores, rcic_assigned, etc.

    # === Healthcare-specific (stored in industry_fields) ===
    # health_card_number, allergies, primary_physician, insurance_provider, etc.

    # Metadata
    tags: List[str] = Field(default_factory=list)
    assigned_to: Optional[str] = None  # User ID
    status: ContactStatus = ContactStatus.ACTIVE
    source: Optional[str] = None  # How they were acquired

    created_by: Optional[str] = None  # User ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Settings:
        name = "contacts"
        indexes = [
            "tenant_id",
            "contact_type",
            "industry",
            "assigned_to",
            "status",
        ]
