# backend/app/schemas/tenant.py
"""Tenant schemas"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    industry: str = Field(..., pattern=r"^(immigration|healthcare)$")
    subdomain: str = Field(..., min_length=3, max_length=63, pattern=r"^[a-z0-9-]+$")
    plan: Optional[str] = "starter"


class TenantResponse(BaseModel):
    id: str
    name: str
    industry: str
    subdomain: str
    plan: str
    is_active: bool
    custom_domain: Optional[str] = None
    brand_name: Optional[str] = None
    brand_primary_color: Optional[str] = None
    settings: Dict[str, Any] = {}
    created_at: datetime


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    brand_name: Optional[str] = None
    brand_logo_url: Optional[str] = None
    brand_primary_color: Optional[str] = None
    custom_domain: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
