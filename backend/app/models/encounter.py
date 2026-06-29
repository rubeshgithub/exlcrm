# backend/app/models/encounter.py
"""
Encounter Model - Healthcare visit/appointment tracking
SOAP notes format for clinical documentation
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class EncounterType(str, Enum):
    INITIAL_VISIT = "initial_visit"
    FOLLOW_UP = "follow_up"
    CONSULTATION = "consultation"
    PROCEDURE = "procedure"
    TELEHEALTH = "telehealth"
    LAB_WORK = "lab_work"
    OTHER = "other"


class EncounterStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class Encounter(Document):
    """Healthcare encounter/visit entity."""

    tenant_id: str = Field(..., index=True)
    contact_id: str = Field(..., index=True)
    provider_id: Optional[str] = None  # User ID of the provider

    encounter_type: EncounterType
    status: EncounterStatus = EncounterStatus.SCHEDULED

    # Scheduling
    scheduled_at: Optional[datetime] = None
    duration_minutes: int = 30
    completed_at: Optional[datetime] = None

    # SOAP Notes
    subjective: Optional[str] = None
    objective: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None

    # Clinical
    diagnosis_codes: List[str] = Field(default_factory=list)
    diagnosis_notes: Optional[str] = None
    treatment_notes: Optional[str] = None
    prescriptions: List[Dict[str, Any]] = Field(default_factory=list)

    # Billing
    billing_code: Optional[str] = None
    amount: Optional[float] = None

    # Attachments
    attachments: List[Dict[str, str]] = Field(default_factory=list)

    notes: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "encounters"
        indexes = [
            "tenant_id",
            "contact_id",
            "provider_id",
            "encounter_type",
            "status",
        ]
