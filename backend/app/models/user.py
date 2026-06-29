# backend/app/models/user.py
"""
User Model - System users belonging to a tenant
Supports RBAC with roles and permissions
"""

from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"  # Platform owner
    TENANT_ADMIN = "tenant_admin"  # Admin within a tenant
    SUPERVISOR = "supervisor"  # Supervisor within a tenant
    USER = "user"  # Regular user (consultant, staff)


class User(Document):
    """User entity - belongs to a tenant."""

    tenant_id: str = Field(..., index=True)
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER
    permissions: List[str] = Field(default_factory=list)
    is_active: bool = True
    is_verified: bool = False

    # Profile
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    timezone: str = "America/Toronto"

    # Tracking
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self) -> bool:
        return self.role in (UserRole.TENANT_ADMIN, UserRole.SUPER_ADMIN)

    @property
    def is_supervisor_or_above(self) -> bool:
        return self.role in (UserRole.SUPER_ADMIN, UserRole.TENANT_ADMIN, UserRole.SUPERVISOR)

    class Settings:
        name = "users"
        indexes = [
            "tenant_id",
            "email",
            "role",
        ]
