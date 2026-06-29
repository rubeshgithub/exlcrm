# backend/app/models/document.py
"""
Document Model - File management with S3 storage
Supports e-signature tracking via DocuSeal
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class SignatureStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    SIGNED = "signed"
    EXPIRED = "expired"
    DECLINED = "declined"
    NOT_REQUIRED = "not_required"


class Document(Document):
    """Document entity - stored in S3, tracked in MongoDB."""

    tenant_id: str = Field(..., index=True)
    contact_id: Optional[str] = Field(default=None, index=True)

    filename: str
    original_filename: str
    s3_key: str
    s3_bucket: str = "exlcrm-documents"
    mime_type: str = "application/octet-stream"
    size_bytes: int = 0

    # Categorization
    category: Optional[str] = None  # e.g., "immigration", "medical", "consent"
    tags: List[str] = Field(default_factory=list)

    # e-Signature (DocuSeal)
    signature_status: SignatureStatus = SignatureStatus.NOT_REQUIRED
    signature_request_id: Optional[str] = None
    signers: List[Dict[str, Any]] = Field(default_factory=list)
    signed_at: Optional[datetime] = None
    signed_pdf_s3_key: Optional[str] = None

    # Versioning
    version: int = 1
    parent_document_id: Optional[str] = None

    # Related entity
    related_case_id: Optional[str] = None
    related_encounter_id: Optional[str] = None
    related_form_submission_id: Optional[str] = None

    description: Optional[str] = None
    uploaded_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "documents"
        indexes = [
            "tenant_id",
            "contact_id",
            "signature_status",
            "category",
        ]
