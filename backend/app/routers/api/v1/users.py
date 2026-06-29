# backend/app/routers/api/v1/users.py
"""User management routes"""

from fastapi import APIRouter, HTTPException, Depends
from app.middleware.auth import get_current_user
from app.utils.rbac import require_permission, require_role
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=dict)
async def list_users(
    current_user: dict = Depends(require_permission("users:read")),
):
    """List users in the tenant."""
    # TODO: Fetch users from database filtered by tenant_id
    return {"users": [], "message": "Not yet implemented"}


@router.post("/", response_model=dict, status_code=201)
async def create_user(
    request: dict,
    current_user: dict = Depends(require_permission("users:create")),
):
    """Create/invite a new user to the tenant."""
    # TODO: Create user with invitation
    # TODO: Send invitation email
    return {"message": "User invitation sent"}


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_permission("users:read")),
):
    """Get user by ID."""
    return {"user_id": user_id, "message": "Not yet implemented"}


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    request: dict,
    current_user: dict = Depends(require_permission("users:update")),
):
    """Update user."""
    return {"user_id": user_id, "message": "Not yet implemented"}


@router.delete("/{user_id}", response_model=dict)
async def deactivate_user(
    user_id: str,
    current_user: dict = Depends(require_permission("users:delete")),
):
    """Deactivate user."""
    return {"user_id": user_id, "message": "User deactivated"}


@router.get("/me/permissions", response_model=dict)
async def get_my_permissions(
    current_user: dict = Depends(get_current_user),
):
    """Get current user's permissions."""
    role = current_user.get("role", "user")
    return {
        "role": role,
        "permissions": [],  # TODO: Return actual permissions based on role
    }
