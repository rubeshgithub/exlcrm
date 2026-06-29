# backend/app/services/sms_service.py
"""InfoBIP SMS service - Send and receive SMS messages"""

import httpx
from typing import Optional, List, Dict
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class InfoBIPService:
    """InfoBIP SMS service."""

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.infobip_api_key
        self.base_url = settings.infobip_base_url
        self.headers = {
            "Authorization": f"App {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def send_sms(
        self,
        to: str,
        message: str,
        from_number: str = "EXL-CRM",
    ) -> Dict:
        """Send a single SMS."""
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/sms/2/text/advanced",
                headers=self.headers,
                json={
                    "messages": [
                        {
                            "destinations": [{"to": to}],
                            "text": message,
                            "from": from_number,
                        }
                    ]
                },
            )
            result = response.json()
            logger.info(f"SMS sent to {to}: {result}")
            return result

    async def send_bulk(
        self, recipients: List[str], message: str, from_number: str = "EXL-CRM"
    ) -> Dict:
        """Send SMS to multiple recipients."""
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/sms/2/text/advanced",
                headers=self.headers,
                json={
                    "messages": [
                        {
                            "destinations": [{"to": phone} for phone in recipients],
                            "text": message,
                            "from": from_number,
                        }
                    ]
                },
            )
            result = response.json()
            logger.info(f"Bulk SMS sent to {len(recipients)} recipients")
            return result

    async def send_appointment_reminder(
        self, to: str, contact_name: str, date: str, time: str
    ) -> Dict:
        """Send appointment reminder SMS."""
        message = (
            f"Hi {contact_name}, this is a reminder about your "
            f"appointment on {date} at {time}. Reply CONFIRM to confirm."
        )
        return await self.send_sms(to, message)

    async def send_form_request(
        self, to: str, contact_name: str, form_name: str, form_link: str
    ) -> Dict:
        """Send form completion request SMS."""
        message = (
            f"Hi {contact_name}, please complete the form: {form_name}. "
            f"Fill it out here: {form_link}"
        )
        return await self.send_sms(to, message)

    async def get_delivery_status(self, message_id: str) -> Dict:
        """Check delivery status of a sent message."""
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{self.base_url}/sms/2/reports?messageId={message_id}",
                headers=self.headers,
            )
            return response.json()


# Singleton
sms_service = InfoBIPService()
