# backend/app/config.py
"""
EXL-CRM Configuration
Settings management using pydantic-settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Application ===
    app_name: str = "EXL-CRM"
    app_env: str = "development"
    app_port: int = 8000
    app_secret_key: str = "change-me-in-production"
    app_url: str = "http://localhost:8000"

    # === MongoDB Atlas (Toronto) ===
    mongodb_url: str = "mongodb://localhost:***@exlcrm.com"

    # === AWS (Montreal: ca-central-1) ===
    aws_region: str = "ca-central-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket: str = "exlcrm-documents"
    ses_from_email: str = "app@exlcrm.com"

    # === InfoBIP SMS ===
    infobip_api_key: str = ""
    infobip_base_url: str = "https://api.infobip.com"

    # === DocuSeal ===
    docuseal_url: str = "http://localhost:55017"
    docuseal_secret: str = ""

    # === Stripe ===
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_starter: str = ""
    stripe_price_professional: str = ""
    stripe_price_enterprise: str = ""

    # === Redis ===
    redis_url: str = "redis://localhost:6379/0"

    # === Frontend ===
    next_public_api_url: str = "http://localhost:8000"
    nextauth_secret: str = ""
    nextauth_url: str = "http://localhost:3000"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
