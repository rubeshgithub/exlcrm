# backend/app/routers/api/v1/health.py
"""Health check routes"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "EXL-CRM",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/ready")
async def readiness_check():
    """Readiness check - verifies all services are connected."""
    # TODO: Check MongoDB connection
    # TODO: Check Redis connection
    # TODO: Check S3 access
    # TODO: Check SES access

    return {
        "status": "ready",
        "checks": {
            "mongodb": "ok",      # Replace with actual check
            "redis": "ok",       # Replace with actual check
            "s3": "ok",          # Replace with actual check
            "ses": "ok",         # Replace with actual check
            "infobip": "ok",     # Replace with actual check
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/live")
async def liveness_check():
    """Liveness check - minimal response."""
    return {"status": "alive"}
