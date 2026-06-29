# backend/app/routers/api/v1/communications.py
"""Communication hub routes - Send emails/SMS, view history"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.services.communication_service import communication_service
from app.services.email_service import ses_service
from app.services.sms_service import sms_service
from app.middleware.auth import get_current_user
from app.utils.rbac import require_permission
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/communications", tags=["Communications"])


class SendEmailRequest(BaseModel):
    to: str
    subject: str
    html_body: str
    text_body: Optional[str] = None
    contact_id: Optional[str] = None


class SendSMSRequest(BaseModel):
    to: str
    message: str
    contact_id: Optional[str] = None


class LogCallRequest(BaseModel):
    contact_id: str
    direction: str  # "inbound" or "outbound"
    duration_seconds: int
    notes: Optional[str] = None


class LogNoteRequest(BaseModel):
    contact_id: str
    content: str


@router.post("/email", response_model=dict)
async def send_email(
    request: SendEmailRequest,
    current_user: dict = Depends(require_permission("communications:send")),
):
    """Send an email and log to communication hub."""
    tenant_id = current_user.get("tenant_id", "")
    user_id = current_user.get("user_id", "")

    result = await communication_service.send_email_and_log(
        tenant_id=tenant_id,
        contact_id=request.contact_id or "",
        to=request.to,
        subject=request.subject,
        html_body=request.html_body,
        text_body=request.text_body,
        sent_by=user_id,
    )

    return result


@router.post("/sms", response_model=dict)
async def send_sms(
    request: SendSMSRequest,
    current_user: dict = Depends(require_permission("communications:send")),
):
    """Send an SMS and log to communication hub."""
    tenant_id = current_user.get("tenant_id", "")
    user_id = current_user.get("user_id", "")

    result = await communication_service.send_sms_and_log(
        tenant_id=tenant_id,
        contact_id=request.contact_id or "",
        to=request.to,
        message=request.message,
        sent_by=user_id,
    )

    return result


@router.post("/call-log", response_model=dict)
async def log_call(
    request: LogCallRequest,
    current_user: dict = Depends(require_permission("communications:read")),
):
    """Log a call."""
    tenant_id = current_user.get("tenant_id", "")
    user_id = current_user.get("user_id", "")

    comm = await communication_service.log_call(
        tenant_id=tenant_id,
        contact_id=request.contact_id,
        direction=request.direction,
        duration_seconds=request.duration_seconds,
        sent_by=user_id,
        notes=request.notes,
    )

    return {"id": str(comm.id), "message": "Call logged"}


@router.post("/note", response_model=dict)
async def log_note(
    request: LogNoteRequest,
    current_user: dict = Depends(require_permission("communications:read")),
):
    """Log an internal note."""
    tenant_id = current_user.get("tenant_id", "")
    user_id = current_user.get("user_id", "")

    comm = await communication_service.log_note(
        tenant_id=tenant_id,
        contact_id=request.contact_id,
        content=request.content,
        sent_by=user_id,
    )

    return {"id": str(comm.id), "message": "Note logged"}


@router.get("/history/{contact_id}", response_model=dict)
async def get_history(
    contact_id: str,
    page: int = 1,
    page_size: int = 20,
    current_user: dict = Depends(require_permission("communications:read")),
):
    """Get communication history for a contact."""
    tenant_id = current_user.get("tenant_id", "")
    result = await communication_service.get_communication_history(
        tenant_id=tenant_id,
        contact_id=contact_id,
        page=page,
        page_size=page_size,
    )
    return result
