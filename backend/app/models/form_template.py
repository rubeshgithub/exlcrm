# backend/app/models/form_template.py
"""
Form Template Model - Drag-and-drop form builder templates
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class FormTemplate(Document):
    """Form template entity for the form builder."""

    tenant_id: str = Field(..., index=True)
    name: str = Field(..., min_length=1, max_length=200)
    industry: str = Field(..., description="immigration or healthcare")
    description: Optional[str] = None

    # Form field definitions (drag & drop builder format)
    fields: List[Dict[str, Any]] = Field(default_factory=list)
    # Example field: {"id": "field_1", "type": "text", "label": "Full Name", "required": true, "order": 1}

    # Settings
    is_active: bool = True
    is_template: bool = True  # Distinguishes templates from submissions

    # Email settings for sending forms
    email_subject: Optional[str] = None
    email_body: Optional[str] = None

    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "form_templates"
        indexes = [
            "tenant_id",
            "industry",
            "is_active",
        ]
