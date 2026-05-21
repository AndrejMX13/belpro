"""Application settings — loaded from environment variables / .env file."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configuration for the Belpro API service.

    Values are read from the process environment or a .env file in the working
    directory. Any key not listed here is silently ignored (extra="ignore").
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── PostgreSQL ────────────────────────────────────────────────────────────
    database_url: str

    # ── Encryption ───────────────────────────────────────────────────────────
    # Base64-encoded 32-byte AES-256 key.  Generate with:
    #   python -c "import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
    emso_encryption_key: str

    # ── FastAPI ───────────────────────────────────────────────────────────────
    api_secret_key: str
    manager_password: str

    # ── SMTP (outgoing email) ─────────────────────────────────────────────────
    # smtp_host, smtp_port, smtp_user, smtp_from_name are stored in DB and
    # configurable from the Settings UI.  Only the password stays here.
    smtp_password: str = ""

    # ── Internal service URLs ─────────────────────────────────────────────────
    whisper_service_url: str = "http://whisper:8001"
    evolution_api_url: str = "http://evolution-api:8080"
    evolution_api_key: str = ""
    evolution_instance_name: str = "belpro"
    authentication_api_key: str = ""
    ngo_whatsapp_phone: str = ""
    ops_url: str = "http://ops:9000"

    # ── Uploads ───────────────────────────────────────────────────────────────
    max_photos_per_entry: int = 5
    photo_retention_days: int = 730

    # ── Session ───────────────────────────────────────────────────────────────
    session_duration_hours: int = 24
    cookie_secure: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (constructed once per process)."""
    return Settings()
