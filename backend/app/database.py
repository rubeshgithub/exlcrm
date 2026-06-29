# backend/app/database.py
"""
EXL-CRM MongoDB Connection
Async MongoDB connection using Beanie ODM and Motor driver
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import BeanieDocument
from beanie import init_beanie
from app.config import get_settings

logger = logging.getLogger(__name__)

# Global references
motor_client: AsyncIOMotorClient = None


async def connect_db():
    """Initialize MongoDB connection and Beanie ODM."""
    settings = get_settings()

    global motor_client
    motor_client = AsyncIOMotorClient(
        settings.mongodb_url,
        tls=True,
        tlsAllowInvalidCertificates=False,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        retryWrites=True,
        retryReads=True,
    )

    # Import all models here so Beanie knows about them
    from app.models.tenant import Tenant
    from app.models.user import User
    from app.models.contact import Contact
    from app.models.case import Case
    from app.models.encounter import Encounter
    from app.models.appointment import Appointment
    from app.models.communication import Communication
    from app.models.document import Document
    from app.models.form_template import FormTemplate
    from app.models.form_submission import FormSubmission
    from app.models.workflow import Workflow
    from app.models.invoice import Invoice
    from app.models.audit_log import AuditLog

    await init_beanie(
        database=motor_client.exlcrm,
        document_models=[
            Tenant,
            User,
            Contact,
            Case,
            Encounter,
            Appointment,
            Communication,
            Document,
            FormTemplate,
            FormSubmission,
            Workflow,
            Invoice,
            AuditLog,
        ],
    )

    logger.info("✅ MongoDB connected and Beanie initialized")


async def close_db():
    """Close MongoDB connection."""
    global motor_client
    if motor_client:
        motor_client.close()
        logger.info("🔌 MongoDB connection closed")


def get_database():
    """Get the MongoDB database instance."""
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_url)
    return client.exlcrm
