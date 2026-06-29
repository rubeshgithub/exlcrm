# backend/app/services/contact_service.py
"""Contact service - CRUD operations for contacts"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.contact import Contact, ContactType, ContactStatus
from app.schemas.contact import ContactCreate, ContactUpdate
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class ContactService:
    """Service layer for contact operations."""

    async def create(self, tenant_id: str, data: ContactCreate, created_by: str) -> Contact:
        """Create a new contact."""
        contact = Contact(
            tenant_id=tenant_id,
            contact_type=data.contact_type,
            industry=data.industry,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            phone_secondary=data.phone_secondary,
            address_line1=data.address_line1,
            address_line2=data.address_line2,
            city=data.city,
            province=data.province,
            postal_code=data.postal_code,
            country=data.country or "Canada",
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            notes=data.notes,
            industry_fields=data.industry_fields,
            tags=data.tags,
            assigned_to=data.assigned_to,
            source=data.source,
            created_by=created_by,
        )
        await contact.insert()
        logger.info(f"Created contact {contact.id} for tenant {tenant_id}")
        return contact

    async def get_by_id(self, tenant_id: str, contact_id: str) -> Optional[Contact]:
        """Get a contact by ID (within tenant)."""
        try:
            contact = await Contact.find_one(
                {"_id": ObjectId(contact_id), "tenant_id": tenant_id}
            )
            return contact
        except Exception:
            return None

    async def list_contacts(
        self,
        tenant_id: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        contact_type: Optional[str] = None,
        status: Optional[str] = None,
        industry: Optional[str] = None,
        assigned_to: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> Dict[str, Any]:
        """List contacts with filtering and pagination."""
        # Build query
        query = {"tenant_id": tenant_id}

        if contact_type:
            query["contact_type"] = contact_type
        if status:
            query["status"] = status
        if industry:
            query["industry"] = industry
        if assigned_to:
            query["assigned_to"] = assigned_to
        if tags:
            query["tags"] = {"$in": tags}

        # Text search
        if search:
            query["$or"] = [
                {"first_name": {"$regex": search, "$options": "i"}},
                {"last_name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"phone": {"$regex": search, "$options": "i"}},
            ]

        # Count total
        total = await Contact.find(query).count()

        # Sort
        sort_field = getattr(Contact, sort_by, Contact.created_at)
        sort_direction = -1 if sort_order == "desc" else 1

        # Paginate
        skip = (page - 1) * page_size
        contacts = (
            await Contact.find(query)
            .sort([(sort_field, sort_direction)])
            .skip(skip)
            .limit(page_size)
            .to_list()
        )

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": contacts,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        }

    async def update(
        self, tenant_id: str, contact_id: str, data: ContactUpdate
    ) -> Optional[Contact]:
        """Update a contact."""
        contact = await self.get_by_id(tenant_id, contact_id)
        if not contact:
            return None

        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        for field, value in update_data.items():
            setattr(contact, field, value)

        await contact.save()
        logger.info(f"Updated contact {contact_id}")
        return contact

    async def delete(self, tenant_id: str, contact_id: str) -> bool:
        """Soft delete a contact (set status to archived)."""
        contact = await self.get_by_id(tenant_id, contact_id)
        if not contact:
            return False

        contact.status = ContactStatus.ARCHIVED
        contact.updated_at = datetime.utcnow()
        await contact.save()
        logger.info(f"Archived contact {contact_id}")
        return True

    async def hard_delete(self, tenant_id: str, contact_id: str) -> bool:
        """Hard delete a contact."""
        try:
            contact = await Contact.find_one(
                {"_id": ObjectId(contact_id), "tenant_id": tenant_id}
            )
            if not contact:
                return False
            await contact.delete()
            return True
        except Exception:
            return False

    async def count_by_tenant(self, tenant_id: str) -> int:
        """Count active contacts for a tenant."""
        return await Contact.find(
            {"tenant_id": tenant_id, "status": ContactStatus.ACTIVE}
        ).count()

    async def search_contacts(
        self, tenant_id: str, query: str, limit: int = 20
    ) -> List[Contact]:
        """Full-text search across contact fields."""
        search_filter = {
            "tenant_id": tenant_id,
            "$or": [
                {"first_name": {"$regex": query, "$options": "i"}},
                {"last_name": {"$regex": query, "$options": "i"}},
                {"email": {"$regex": query, "$options": "i"}},
                {"phone": {"$regex": query, "$options": "i"}},
                {"tags": {"$in": [query]}},
            ],
        }
        return await Contact.find(search_filter).limit(limit).to_list()


# Singleton instance
contact_service = ContactService()
