# backend/app/models/form_submission.py
"""
Form Submission Model - Completed form responses
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class FormSubmission(Document):
    """Form submission entity."""

    tenant_id: str = Field(..., index=True)
    template_id: str = Field(..., index=True)
    contact_id: Optional[str] = Field(default=None, index=True)

    # Form responses
    responses: Dict[str, Any] = Field(default_factory=dict)

    # e-Signature
    signature_status: str = "not_required"
    signature_request_id: Optional[str] = None
    signed_at: Optional[datetime] = None
    signed_pdf_s3_key: Optional[str] = None

    # Submission
    submitted_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "form_submissions"
        indexes = [
            "tenant_id",
            "template_id",
            "contact_id",
        ]
