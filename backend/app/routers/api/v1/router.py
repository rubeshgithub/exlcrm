# backend/app/routers/api/v1/router.py
"""API v1 Router aggregator"""

from fastapi import APIRouter
from app.routers.api.v1 import auth, health, tenants, users, contacts, documents, communications

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(tenants.router)
api_router.include_router(users.router)
api_router.include_router(contacts.router)
api_router.include_router(documents.router)
api_router.include_router(communications.router)
