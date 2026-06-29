# backend/app/models/case.py
"""
Case Model - Immigration case management
RCIC-aligned case tracking with status pipeline
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class CaseType(str, Enum):
    EXPRESS_ENTRY = "express_entry"
    PROVINCIAL_NOMINEE = "pnp"
    LMIA = "lmia"
    STUDY_PERMIT = "study_permit"
    WORK_PERMIT = "work_permit"
    VISITOR_VISA = "visitor_visa"
    SPONSORSHIP = "sponsorship"
    OTHER = "other"


class CaseStatus(str, Enum):
    INTAKE = "intake"
    DOCUMENT_COLLECTION = "document_collection"
    APPLICATION_PREPARATION = "application_preparation"
    SUBMITTED = "submitted"
    IN_PROCESS = "in_process"
    ADDITIONAL_DOCS_REQUESTED = "additional_docs_requested"
    APPROVED = "approved"
    REFUSED = "refused"
    WITHDRAWN = "withdrawn"


class Case(Document):
    """Immigration case entity."""

    tenant_id: str = Field(..., index=True)
    contact_id: str = Field(..., index=True)
    case_type: CaseType
    status: CaseStatus = CaseStatus.INTAKE

    # RCIC Information
    rcic_number: Optional[str] = None
    rcic_name: Optional[str] = None

    # Case Details
    program: Optional[str] = None
    stream: Optional[str] = None
    visa_office: Optional[str] = None

    # Processing
    uci_number: Optional[str] = None
    application_number: Optional[str] = None
    submission_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    # Documents and timeline
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    timeline: List[Dict[str, Any]] = Field(default_factory=list)
    notes: List[Dict[str, Any]] = Field(default_factory=list)

    # Scoring
    crs_score: Optional[int] = None

    assigned_to: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "cases"
        indexes = [
            "tenant_id",
            "contact_id",
            "case_type",
            "status",
        ]
