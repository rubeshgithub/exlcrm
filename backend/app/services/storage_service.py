# backend/app/services/storage_service.py
"""AWS S3 storage service - Upload/download documents"""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.config import get_settings
import logging
import uuid

logger = logging.getLogger(__name__)


class S3Service:
    """AWS S3 service for document storage."""

    def __init__(self):
        settings = get_settings()
        self.client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.bucket = settings.s3_bucket

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        tenant_id: str,
        contact_id: Optional[str] = None,
    ) -> Dict[str, str]:
        """Upload a file to S3 with tenant isolation."""
        # Generate unique key
        file_uuid = str(uuid.uuid4())
        ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
        s3_key = f"{tenant_id}/{file_uuid}.{ext}" if not contact_id else f"{tenant_id}/{contact_id}/{file_uuid}.{ext}"

        # Upload
        self.client.put_object(
            Bucket=self.bucket,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type,
            ServerSideEncryption="AES256",
            Metadata={
                "tenant-id": tenant_id,
                "original-filename": filename,
            },
        )

        logger.info(f"Uploaded file to s3://{self.bucket}/{s3_key}")

        return {
            "s3_key": s3_key,
            "bucket": self.bucket,
            "filename": filename,
            "content_type": content_type,
            "size": len(file_content),
        }

    async def get_presigned_url(
        self, s3_key: str, expires: int = 3600
    ) -> str:
        """Generate a presigned download URL."""
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": s3_key},
            ExpiresIn=expires,
        )
        return url

    async def delete_file(self, s3_key: str) -> bool:
        """Delete a file from S3."""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=s3_key)
            logger.info(f"Deleted s3://{self.bucket}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete {s3_key}: {e}")
            return False

    async def get_file_info(self, s3_key: str) -> Optional[Dict[str, Any]]:
        """Get file metadata."""
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=s3_key)
            return {
                "size": response["ContentLength"],
                "content_type": response["ContentType"],
                "last_modified": response["LastModified"].isoformat(),
                "metadata": response.get("Metadata", {}),
            }
        except ClientError:
            return None


# Singleton
s3_service = S3Service()
