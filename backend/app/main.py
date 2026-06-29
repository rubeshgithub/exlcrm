# backend/app/main.py
"""
EXL-CRM FastAPI Application
Multi-Tenant CRM Platform for Canadian Professional Services
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import get_settings
from app.database import connect_db, close_db
from app.middleware.tenant import TenantMiddleware
from app.routers.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    # Startup
    logger.info("🚀 Starting EXL-CRM...")
    try:
        await connect_db()
        logger.info("✅ Database connected")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.warning("⚠️ Starting without database - some endpoints may not work")

    yield

    # Shutdown
    logger.info("🛑 Shutting down EXL-CRM...")
    await close_db()
    logger.info("✅ Shutdown complete")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title="EXL-CRM",
        description="""
        EXL-CRM - Multi-Tenant CRM Platform
        
        ## Features
        - **Multi-industry**: Immigration & Healthcare modules
        - **Multi-tenant**: Secure data isolation per tenant
        - **Canadian compliant**: RCIC, PHIPA, PIPEDA aligned
        - **RBAC**: Role-based access control
        - **Document management**: S3 storage with e-signatures
        - **Communication hub**: Unified calls, SMS, emails
        
        ## Tech Stack
        - FastAPI + Python 3.12
        - MongoDB Atlas (Beanie ODM)
        - AWS S3 + SES
        - InfoBIP SMS
        - DocuSeal e-signatures
        """,
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # === Middleware (order matters) ===

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:***@exlcrm.com",
            "https://app.exlcrm.com",
            "https://exlcrm.com",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Tenant resolution (after CORS, before auth)
    app.add_middleware(TenantMiddleware)

    # === Routes ===

    # API v1
    app.include_router(api_router)

    # Root endpoint
    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "name": "EXL-CRM",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/api/v1/health",
        }

    return app


# Create the app instance
app = create_app()
