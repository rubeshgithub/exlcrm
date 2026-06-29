# backend/app/utils/rbac.py
"""
RBAC (Role-Based Access Control) System
Permission checks and role hierarchy
"""

from functools import wraps
from fastapi import HTTPException, Depends
from app.middleware.auth import get_current_user
from typing import List, Optional

# Role hierarchy - higher number = more permissions
ROLE_HIERARCHY = {
    "super_admin": 100,
    "tenant_admin": 80,
    "supervisor": 60,
    "user": 40,
}

# Permission definitions
PERMISSIONS = {
    # User management
    "users:create": {"min_role": "tenant_admin"},
    "users:read": {"min_role": "supervisor"},
    "users:update": {"min_role": "tenant_admin"},
    "users:delete": {"min_role": "tenant_admin"},
    "roles:manage": {"min_role": "tenant_admin"},

    # Contact management
    "contacts:create": {"min_role": "user"},
    "contacts:read": {"min_role": "user"},
    "contacts:update": {"min_role": "user"},
    "contacts:delete": {"min_role": "supervisor"},

    # Case management
    "cases:create": {"min_role": "user"},
    "cases:read": {"min_role": "user"},
    "cases:update": {"min_role": "user"},
    "cases:delete": {"min_role": "supervisor"},

    # Encounter management
    "encounters:create": {"min_role": "user"},
    "encounters:read": {"min_role": "user"},
    "encounters:update": {"min_role": "user"},
    "encounters:delete": {"min_role": "supervisor"},

    # Communication
    "communications:send": {"min_role": "user"},
    "communications:read": {"min_role": "user"},

    # Documents
    "documents:create": {"min_role": "user"},
    "documents:read": {"min_role": "user"},
    "documents:delete": {"min_role": "supervisor"},

    # Forms
    "forms:manage": {"min_role": "supervisor"},
    "forms:submit": {"min_role": "user"},

    # Workflows
    "workflows:manage": {"min_role": "supervisor"},

    # Billing
    "billing:access": {"min_role": "tenant_admin"},

    # Reports
    "reports:export": {"min_role": "supervisor"},

    # Settings
    "settings:manage": {"min_role": "tenant_admin"},

    # Audit logs
    "audit:read": {"min_role": "tenant_admin"},
}


def has_permission(role: str, permission: str) -> bool:
    """Check if a role has a specific permission."""
    if permission not in PERMISSIONS:
        return False

    required_role = PERMISSIONS[permission]["min_role"]
    user_level = ROLE_HIERARCHY.get(role, 0)
    required_level = ROLE_HIERARCHY.get(required_role, 0)

    return user_level >= required_level


def require_permission(permission: str):
    """Dependency that requires a specific permission."""
    async def permission_checker(
        current_user: dict = Depends(get_current_user),
    ):
        role = current_user.get("role", "user")
        if not has_permission(role, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied: {permission} required",
            )
        return current_user

    return permission_checker


def require_role(min_role: str):
    """Dependency that requires a minimum role level."""
    async def role_checker(
        current_user: dict = Depends(get_current_user),
    ):
        user_role = current_user.get("role", "user")
        user_level = ROLE_HIERARCHY.get(user_role, 0)
        required_level = ROLE_HIERARCHY.get(min_role, 0)

        if user_level < required_level:
            raise HTTPException(
                status_code=403,
                detail=f"Role {min_role} or higher required",
            )
        return current_user

    return role_checker
