# backend/app/models/appointment.py
"""
Appointment Model - Shared between industries
Used for immigration consultations and healthcare visits
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class AppointmentType(str, Enum):
    INITIAL_CONSULTATION = "initial_consultation"
    FOLLOW_UP = "follow_up"
    DOCUMENT_REVIEW = "document_review"
    INTERVIEW_PREP = "interview_prep"
    CLINIC_VISIT = "clinic_visit"
    TELEHEALTH = "telehealth"
    OTHER = "other"


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    NO_SHOW = "no_show"


class Appointment(Document):
    """Appointment entity."""

    tenant_id: str = Field(..., index=True)
    contact_id: str = Field(..., index=True)
    type: AppointmentType
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

    # Timing
    scheduled_at: datetime
    duration_minutes: int = 60
    end_time: Optional[datetime] = None

    # Participants
    assigned_to: Optional[str] = None  # User ID
    provider_id: Optional[str] = None  # Healthcare provider

    # Location/Meeting
    location: Optional[str] = None
    meeting_link: Optional[str] = None  # Zoom/Teams link
    room: Optional[str] = None

    # Reminders
    reminders_sent: List[dict] = Field(default_factory=list)

    # Notes
    subject: Optional[str] = None
    description: Optional[str] = None
    internal_notes: Optional[str] = None

    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "appointments"
        indexes = [
            "tenant_id",
            "contact_id",
            "assigned_to",
            "scheduled_at",
            "status",
        ]
