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
    #   python3 -c "import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
    emso_encryption_key: str

    # ── FastAPI ───────────────────────────────────────────────────────────────
    api_secret_key: str
    manager_password: str

    # ── NGO identity (used in PDFs and manager profile defaults) ─────────────
    ngo_name: str = ""
    ngo_address: str = ""

    # ── Gmail (outgoing email) ────────────────────────────────────────────────
    gmail_address: str = ""
    gmail_app_password: str = ""

    # ── Internal service URLs ─────────────────────────────────────────────────
    whisper_service_url: str = "http://whisper:8001"
    evolution_api_url: str = "http://evolution-api:8080"
    evolution_api_key: str = ""
    evolution_instance_name: str = "belpro"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (constructed once per process)."""
    return Settings()
