# backend/app/models/audit_log.py
"""
Audit Log Model - Compliance trail for all actions
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLog(Document):
    """Audit log entity for compliance tracking."""

    tenant_id: str = Field(..., index=True)
    user_id: Optional[str] = None
    action: str = Field(..., description="e.g., create, update, delete, login, export")
    entity: str = Field(..., description="e.g., contact, case, user, document")
    entity_id: Optional[str] = None

    # Change tracking
    changes: Dict[str, Any] = Field(default_factory=dict)
    # Example: {"field": "status", "old": "intake", "new": "document_collection"}

    # Request metadata
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "audit_logs"
        indexes = [
            "tenant_id",
            "user_id",
            "action",
            "entity",
            "timestamp",
        ]
