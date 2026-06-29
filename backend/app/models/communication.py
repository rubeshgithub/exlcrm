# backend/app/models/communication.py
"""
Communication Model - Unified communication log
Tracks all calls, SMS, and emails
"""

from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class CommunicationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    CALL = "call"
    NOTE = "note"


class CommunicationDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Communication(Document):
    """Communication log entity."""

    tenant_id: str = Field(..., index=True)
    contact_id: Optional[str] = Field(default=None, index=True)
    type: CommunicationType
    direction: CommunicationDirection

    # Email fields
    subject: Optional[str] = None
    body: Optional[str] = None
    html_body: Optional[str] = None

    # SMS fields
    message: Optional[str] = None

    # Call fields
    call_duration_seconds: Optional[int] = None
    call_recording_url: Optional[str] = None

    # Participants
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    cc_addresses: List[str] = Field(default_factory=list)

    # Status
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None

    # Attachments
    attachments: List[Dict[str, str]] = Field(default_factory=list)

    # Related entity
    related_case_id: Optional[str] = None
    related_encounter_id: Optional[str] = None

    sent_by: Optional[str] = None  # User ID
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "communications"
        indexes = [
            "tenant_id",
            "contact_id",
            "type",
            "sent_at",
        ]
