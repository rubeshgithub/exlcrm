# backend/app/models/tenant.py
"""
Tenant Model - Multi-tenant organization entity
Each tenant represents a firm/clinic using EXL-CRM
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class IndustryType(str, Enum):
    IMMIGRATION = "immigration"
    HEALTHCARE = "healthcare"


class SubscriptionPlan(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class Tenant(Document):
    """Tenant organization entity."""

    name: str = Field(..., min_length=1, max_length=200)
    industry: IndustryType
    subdomain: str = Field(..., min_length=3, max_length=63, pattern=r"^[a-z0-9-]+$")
    plan: SubscriptionPlan = SubscriptionPlan.STARTER
    is_active: bool = True
    custom_domain: Optional[str] = None

    # Settings stored as flexible dict
    settings: dict = Field(default_factory=dict)

    # White-label branding
    brand_name: Optional[str] = None
    brand_logo_url: Optional[str] = None
    brand_primary_color: Optional[str] = "#2563eb"

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tenants"
        indexes = [
            "subdomain",
            "industry",
            "plan",
        ]
