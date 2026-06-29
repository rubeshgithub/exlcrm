# backend/app/routers/api/v1/documents.py
"""Document management routes - Upload, download, e-signature"""

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import Optional
from app.services.storage_service import s3_service
from app.services.communication_service import communication_service
from app.middleware.auth import get_current_user
from app.utils.rbac import require_permission
import logging
import io

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=dict, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    contact_id: Optional[str] = None,
    category: Optional[str] = None,
    description: Optional[str] = None,
    current_user: dict = Depends(require_permission("documents:create")),
):
    """Upload a document to S3."""
    tenant_id = current_user.get("tenant_id", "")
    user_id = current_user.get("user_id", "")

    # Read file content
    content = await file.read()

    # Upload to S3
    result = await s3_service.upload_file(
        file_content=content,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        tenant_id=tenant_id,
        contact_id=contact_id,
    )

    # TODO: Create document record in MongoDB
    # document = Document(...)

    return {
        "message": "Document uploaded successfully",
        "filename": file.filename,
        "s3_key": result["s3_key"],
        "size": result["size"],
        "content_type": result["content_type"],
    }


@router.get("/{document_id}/download", response_model=dict)
async def get_download_url(
    document_id: str,
    expires: int = Query(3600, ge=60, max=86400),
    current_user: dict = Depends(require_permission("documents:read")),
):
    """Get a presigned download URL for a document."""
    # TODO: Look up document from database
    # s3_key = document.s3_key
    # url = await s3_service.get_presigned_url(s3_key, expires)

    return {"url": "placeholder", "expires_in": expires}


@router.delete("/{document_id}", response_model=dict)
async def delete_document(
    document_id: str,
    current_user: dict = Depends(require_permission("documents:delete")),
):
    """Delete a document."""
    # TODO: Look up and delete from S3 + MongoDB
    return {"message": "Document deleted"}


@router.post("/{document_id}/send-for-signature", response_model=dict, status_code=201)
async def send_for_signature(
    document_id: str,
    signers: list,
    current_user: dict = Depends(require_permission("documents:create")),
):
    """Send a document for e-signature via DocuSeal."""
    # TODO: Integrate with DocuSeal API
    # 1. Get document from S3
    # 2. Create DocuSeal signature request
    # 3. Send email to signers
    # 4. Update document signature_status

    return {"message": "Document sent for signature", "signers": signers}
