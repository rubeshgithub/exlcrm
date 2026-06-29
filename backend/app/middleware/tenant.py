# backend/app/middleware/tenant.py
"""
Tenant Middleware - Resolves tenant from subdomain
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """Resolve tenant from subdomain and attach to request state."""

    # Paths that don't require tenant resolution
    SKIP_PATHS = [
        "/api/v1/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/register",
        "/api/v1/auth/login",
        "/api/v1/tenants/onboarding",
    ]

    async def dispatch(self, request: Request, call_next):
        # Skip tenant resolution for public paths
        if any(request.url.path.startswith(path) for path in self.SKIP_PATHS):
            return await call_next(request)

        # Extract subdomain from host
        host = request.headers.get("host", "")
        subdomain = self._extract_subdomain(host)

        if not subdomain:
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid request: no subdomain"},
            )

        # TODO: Look up tenant from database by subdomain
        # For now, attach subdomain to request state
        request.state.subdomain = subdomain
        request.state.tenant_id = None  # Will be resolved from DB

        response = await call_next(request)
        return response

    def _extract_subdomain(self, host: str) -> str:
        """Extract subdomain from host header."""
        if not host:
            return ""

        # Remove port if present
        if ":" in host:
            host = host.split(":")[0]

        parts = host.split(".")
        # For localhost or single-part hosts
        if len(parts) < 3:
            return ""

        # Extract subdomain (first part)
        subdomain = parts[0]

        # Skip www
        if subdomain == "www":
            if len(parts) >= 3:
                subdomain = parts[1] if len(parts) > 2 else ""
            else:
                subdomain = ""

        return subdomain
