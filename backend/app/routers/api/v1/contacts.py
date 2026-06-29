# backend/app/routers/api/v1/contacts.py
"""Contact management routes - CRUD with search and filtering"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.services.contact_service import contact_service
from app.services.communication_service import communication_service
from app.middleware.auth import get_current_user
from app.utils.rbac import require_permission
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=dict, status_code=201)
async def create_contact(
    request: ContactCreate,
    current_user: dict = Depends(require_permission("contacts:create")),
):
    """Create a new contact (applicant or patient)."""
    tenant_id = current_user.get("tenant_id", "")
    user_id = current_user.get("user_id", "")

    contact = await contact_service.create(tenant_id, request, user_id)

    return {
        "id": str(contact.id),
        "message": "Contact created successfully",
        "contact": {
            "id": str(contact.id),
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "contact_type": contact.contact_type,
            "industry": contact.industry,
        },
    }


@router.get("/", response_model=dict)
async def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    contact_type: Optional[str] = None,
    status: Optional[str] = None,
    industry: Optional[str] = None,
    assigned_to: Optional[str] = None,
    tags: Optional[str] = None,  # Comma-separated
    sort_by: str = "created_at",
    sort_order: str = "desc",
    current_user: dict = Depends(require_permission("contacts:read")),
):
    """List contacts with filtering and pagination."""
    tenant_id = current_user.get("tenant_id", "")
    tag_list = tags.split(",") if tags else None

    result = await contact_service.list_contacts(
        tenant_id=tenant_id,
        page=page,
        page_size=page_size,
        search=search,
        contact_type=contact_type,
        status=status,
        industry=industry,
        assigned_to=assigned_to,
        tags=tag_list,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return result


@router.get("/{contact_id}", response_model=dict)
async def get_contact(
    contact_id: str,
    current_user: dict = Depends(require_permission("contacts:read")),
):
    """Get a contact by ID."""
    tenant_id = current_user.get("tenant_id", "")
    contact = await contact_service.get_by_id(tenant_id, contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {
        "id": str(contact.id),
        "tenant_id": contact.tenant_id,
        "contact_type": contact.contact_type,
        "industry": contact.industry,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "email": contact.email,
        "phone": contact.phone,
        "phone_secondary": contact.phone_secondary,
        "address_line1": contact.address_line1,
        "address_line2": contact.address_line2,
        "city": contact.city,
        "province": contact.province,
        "postal_code": contact.postal_code,
        "country": contact.country,
        "date_of_birth": contact.date_of_birth,
        "gender": contact.gender,
        "notes": contact.notes,
        "industry_fields": contact.industry_fields,
        "tags": contact.tags,
        "assigned_to": contact.assigned_to,
        "status": contact.status,
        "source": contact.source,
        "created_at": contact.created_at,
    }


@router.put("/{contact_id}", response_model=dict)
async def update_contact(
    contact_id: str,
    request: ContactUpdate,
    current_user: dict = Depends(require_permission("contacts:update")),
):
    """Update a contact."""
    tenant_id = current_user.get("tenant_id", "")
    contact = await contact_service.update(tenant_id, contact_id, request)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {
        "id": str(contact.id),
        "message": "Contact updated successfully",
    }


@router.delete("/{contact_id}", response_model=dict)
async def delete_contact(
    contact_id: str,
    hard: bool = False,
    current_user: dict = Depends(require_permission("contacts:delete")),
):
    """Delete a contact (soft delete by default)."""
    tenant_id = current_user.get("tenant_id", "")

    if hard:
        success = await contact_service.hard_delete(tenant_id, contact_id)
    else:
        success = await contact_service.delete(tenant_id, contact_id)

    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Contact deleted" if hard else "Contact archived"}


@router.get("/{contact_id}/timeline", response_model=dict)
async def get_contact_timeline(
    contact_id: str,
    current_user: dict = Depends(require_permission("contacts:read")),
):
    """Get unified timeline for a contact."""
    tenant_id = current_user.get("tenant_id", "")
    timeline = await communication_service.get_timeline(tenant_id, contact_id)
    return {"items": timeline, "total": len(timeline)}


@router.get("/search/", response_model=dict)
async def search_contacts(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    current_user: dict = Depends(require_permission("contacts:read")),
):
    """Full-text search across contacts."""
    tenant_id = current_user.get("tenant_id", "")
    contacts = await contact_service.search_contacts(tenant_id, q, limit)
    return {"items": contacts, "total": len(contacts), "query": q}
