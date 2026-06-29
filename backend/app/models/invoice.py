# backend/app/models/invoice.py
"""
Invoice Model - Billing and payment tracking
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(Document):
    """Invoice entity."""

    tenant_id: str = Field(..., index=True)
    contact_id: Optional[str] = Field(default=None, index=True)

    invoice_number: str = Field(...)
    stripe_invoice_id: Optional[str] = None
    amount: float = 0.0
    currency: str = "CAD"
    status: InvoiceStatus = InvoiceStatus.DRAFT

    # Line items
    line_items: List[Dict[str, Any]] = Field(default_factory=list)

    # Dates
    due_date: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None

    # Notes
    notes: Optional[str] = None
    footer_text: Optional[str] = None

    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "invoices"
        indexes = [
            "tenant_id",
            "contact_id",
            "invoice_number",
            "status",
        ]
