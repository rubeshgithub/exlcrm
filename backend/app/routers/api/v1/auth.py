# backend/app/routers/api/v1/auth.py
"""Authentication routes - Login, Register, Token management"""

from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
)
from app.middleware.auth import create_access_token, create_refresh_token, get_current_user
from app.config import get_settings
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register", response_model=dict, status_code=201)
async def register(request: RegisterRequest):
    """Register a new user."""
    # TODO: Check if email already exists
    # TODO: Create tenant if tenant_name provided
    # TODO: Create user with hashed password

    hashed_password = get_password_hash(request.password)

    return {
        "message": "User registered successfully",
        "email": request.email,
        "next_step": "check-email-for-verification",
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return tokens."""
    # TODO: Look up user by email
    # TODO: Verify password
    # TODO: Generate and return tokens

    # Placeholder - replace with actual DB lookup
    raise HTTPException(status_code=501, detail="Login not yet implemented - Phase 0 scaffold")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token using refresh token."""
    settings = get_settings()
    # TODO: Validate refresh token
    # TODO: Issue new access token

    raise HTTPException(status_code=501, detail="Refresh not yet implemented - Phase 0 scaffold")


@router.get("/me", response_model=dict)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info."""
    # TODO: Fetch full user details from database
    return {
        "user_id": current_user.get("user_id"),
        "email": current_user.get("email"),
        "role": current_user.get("role"),
        "tenant_id": current_user.get("tenant_id"),
    }


@router.post("/logout")
async def logout():
    """Logout (client should discard tokens)."""
    # TODO: Add token to blacklist in Redis
    return {"message": "Logged out successfully"}
