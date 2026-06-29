# backend/app/services/communication_service.py
"""Communication hub - Unified communication log"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.communication import Communication, CommunicationType, CommunicationDirection
from app.services.email_service import ses_service
from app.services.sms_service import sms_service
import logging

logger = logging.getLogger(__name__)


class CommunicationService:
    """Unified communication hub."""

    async def send_email_and_log(
        self,
        tenant_id: str,
        contact_id: str,
        to: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        sent_by: Optional[str] = None,
        related_case_id: Optional[str] = None,
        related_encounter_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send email and log to communication hub."""
        # Send via SES
        message_id = await ses_service.send_email(
            to=to, subject=subject, html_body=html_body, text_body=text_body
        )

        # Log to communication hub
        comm = Communication(
            tenant_id=tenant_id,
            contact_id=contact_id,
            type=CommunicationType.EMAIL,
            direction=CommunicationDirection.OUTBOUND,
            subject=subject,
            body=text_body,
            html_body=html_body,
            to_address=to,
            sent_at=datetime.utcnow(),
            sent_by=sent_by,
            related_case_id=related_case_id,
            related_encounter_id=related_encounter_id,
        )
        await comm.insert()

        return {"message_id": message_id, "communication_id": str(comm.id)}

    async def send_sms_and_log(
        self,
        tenant_id: str,
        contact_id: str,
        to: str,
        message: str,
        sent_by: Optional[str] = None,
        related_case_id: Optional[str] = None,
        related_encounter_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send SMS and log to communication hub."""
        # Send via InfoBIP
        result = await sms_service.send_sms(to=to, message=message)

        # Log to communication hub
        comm = Communication(
            tenant_id=tenant_id,
            contact_id=contact_id,
            type=CommunicationType.SMS,
            direction=CommunicationDirection.OUTBOUND,
            message=message,
            to_address=to,
            sent_at=datetime.utcnow(),
            sent_by=sent_by,
            related_case_id=related_case_id,
            related_encounter_id=related_encounter_id,
        )
        await comm.insert()

        return {"sms_result": result, "communication_id": str(comm.id)}

    async def log_call(
        self,
        tenant_id: str,
        contact_id: str,
        direction: str,
        duration_seconds: int,
        call_recording_url: Optional[str] = None,
        sent_by: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Communication:
        """Log a call (calls are typically logged after they happen)."""
        comm = Communication(
            tenant_id=tenant_id,
            contact_id=contact_id,
            type=CommunicationType.CALL,
            direction=CommunicationDirection(direction),
            call_duration_seconds=duration_seconds,
            call_recording_url=call_recording_url,
            notes=notes,
            sent_at=datetime.utcnow(),
            sent_by=sent_by,
        )
        await comm.insert()
        return comm

    async def log_note(
        self,
        tenant_id: str,
        contact_id: str,
        content: str,
        sent_by: Optional[str] = None,
    ) -> Communication:
        """Log an internal note."""
        comm = Communication(
            tenant_id=tenant_id,
            contact_id=contact_id,
            type=CommunicationType.NOTE,
            direction=CommunicationDirection.INBOUND,
            body=content,
            sent_by=sent_by,
            created_at=datetime.utcnow(),
        )
        await comm.insert()
        return comm

    async def get_communication_history(
        self,
        tenant_id: str,
        contact_id: str,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get communication history for a contact."""
        from app.utils.pagination import paginate

        query = {"tenant_id": tenant_id, "contact_id": contact_id}
        total = await Communication.find(query).count()

        skip = (page - 1) * page_size
        comms = (
            await Communication.find(query)
            .sort([("created_at", -1)])
            .skip(skip)
            .limit(page_size)
            .to_list()
        )

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": comms,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        }

    async def get_timeline(
        self,
        tenant_id: str,
        contact_id: str,
    ) -> List[Dict[str, Any]]:
        """Get unified timeline (communications + encounters + notes)."""
        # Get communications
        comms = await Communication.find(
            {"tenant_id": tenant_id, "contact_id": contact_id}
        ).sort([("created_at", -1)]).to_list()

        timeline = []
        for c in comms:
            timeline.append({
                "type": "communication",
                "sub_type": c.type,
                "timestamp": c.created_at,
                "data": c,
            })

        # Sort by timestamp
        timeline.sort(key=lambda x: x["timestamp"], reverse=True)
        return timeline


# Singleton
communication_service = CommunicationService()
