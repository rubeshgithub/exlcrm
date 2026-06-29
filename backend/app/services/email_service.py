# backend/app/services/email_service.py
"""AWS SES email service - Transactional emails with templates"""

import boto3
from botocore.exceptions import ClientError
from typing import Optional, List, Dict
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class EmailTemplate:
    """Email template definitions."""

    WELCOME = {
        "subject": "Welcome to {app_name}",
        "html": "<h1>Welcome, {first_name}!</h1><p>Your account has been created.</p>",
        "text": "Welcome, {first_name}! Your account has been created.",
    }

    CONTACT_ASSIGNED = {
        "subject": "New contact assigned: {contact_name}",
        "html": "<p>A new contact <strong>{contact_name}</strong> has been assigned to you.</p>",
        "text": "A new contact {contact_name} has been assigned to you.",
    }

    APPOINTMENT_REMINDER = {
        "subject": "Appointment reminder: {appointment_date}",
        "html": "<p>This is a reminder for your appointment on <strong>{appointment_date}</strong>.</p>",
        "text": "Reminder: You have an appointment on {appointment_date}.",
    }

    FORM_REQUEST = {
        "subject": "Please complete: {form_name}",
        "html": '<p>Please complete the form: <strong>{form_name}</strong></p><p><a href="{form_link}">Click here to fill the form</a></p>',
        "text": "Please complete the form: {form_name}. Link: {form_link}",
    }

    PASSWORD_RESET = {
        "subject": "Reset your password",
        "html": '<p>Click <a href="{reset_link}">here</a> to reset your password. This link expires in 1 hour.</p>',
        "text": "Reset your password: {reset_link} (expires in 1 hour)",
    }

    INVITATION = {
        "subject": "You've been invited to {app_name}",
        "html": '<p>{inviter_name} has invited you to join {app_name}.</p><p><a href="{invite_link}">Accept invitation</a></p>',
        "text": "{inviter_name} invited you to {app_name}. Accept: {invite_link}",
    }


class SESService:
    """AWS SES email service."""

    def __init__(self):
        settings = get_settings()
        self.client = boto3.client(
            "ses",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.from_email = settings.ses_from_email

    async def send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
    ) -> str:
        """Send an email via SES."""
        destinations = {"ToAddresses": [to] if isinstance(to, str) else to}
        if cc:
            destinations["CcAddresses"] = cc
        if bcc:
            destinations["BccAddresses"] = bcc

        message = {
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {
                "Html": {"Data": html_body, "Charset": "UTF-8"},
            },
        }
        if text_body:
            message["Body"]["Text"] = {"Data": text_body, "Charset": "UTF-8"}

        kwargs = {
            "Source": self.from_email,
            "Destination": destinations,
            "Message": message,
        }
        if reply_to:
            kwargs["ReplyToAddresses"] = [reply_to]

        try:
            response = self.client.send_email(**kwargs)
            message_id = response["MessageId"]
            logger.info(f"Email sent to {to}: {message_id}")
            return message_id
        except ClientError as e:
            logger.error(f"Failed to send email to {to}: {e}")
            raise

    async def send_template_email(
        self,
        to: str,
        template_name: str,
        variables: Dict[str, str],
    ) -> str:
        """Send an email using a predefined template."""
        template = getattr(EmailTemplate, template_name.upper(), None)
        if not template:
            raise ValueError(f"Unknown template: {template_name}")

        subject = template["subject"].format(**variables)
        html_body = template["html"].format(**variables)
        text_body = template["text"].format(**variables)

        return await self.send_email(to, subject, html_body, text_body)

    async def send_bulk(
        self, recipients: List[str], subject: str, html_body: str, text_body: Optional[str] = None
    ) -> List[str]:
        """Send the same email to multiple recipients (individual emails)."""
        message_ids = []
        for recipient in recipients:
            try:
                msg_id = await self.send_email(recipient, subject, html_body, text_body)
                message_ids.append(msg_id)
            except Exception as e:
                logger.error(f"Failed to send bulk email to {recipient}: {e}")
        return message_ids

    async def verify_email_identity(self, email: str) -> bool:
        """Verify an email address for sending."""
        try:
            self.client.verify_email_identity(EmailAddress=email)
            return True
        except ClientError:
            return False


# Singleton
ses_service = SESService()
