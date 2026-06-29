# backend/app/models/workflow.py
"""
Workflow Model - Automation rules and triggers
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class Workflow(Document):
    """Workflow automation entity."""

    tenant_id: str = Field(..., index=True)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

    # Trigger configuration
    trigger: Dict[str, Any] = Field(default_factory=dict)
    # Example: {"type": "status_change", "entity": "case", "from": "intake", "to": "document_collection"}

    # Actions to execute
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    # Example: [{"type": "send_email", "template": "welcome"}, {"type": "assign_user", "user_id": "..."}]

    is_active: bool = True
    execution_count: int = 0
    last_executed_at: Optional[datetime] = None

    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "workflows"
        indexes = [
            "tenant_id",
            "is_active",
        ]
