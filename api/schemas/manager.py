"""Pydantic schemas for the Manager entity."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class ManagerCreate(BaseModel):
    """Fields required for first-time manager setup."""

    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    phone: Annotated[str, Field(min_length=1, max_length=30)]
    email: EmailStr
    ngo_name: Annotated[str, Field(min_length=1, max_length=200)]
    ngo_street: Annotated[str, Field(min_length=1, max_length=255)]
    ngo_postal_code: Annotated[str, Field(pattern=r"^\d{4}$")]
    ngo_city: Annotated[str, Field(min_length=1, max_length=100)]
    ngo_davcna: Annotated[str, Field(pattern=r"^\d{8}$")] | None = None


class ManagerUpdate(BaseModel):
    """Partial update — all fields optional.  Only provided fields are written."""

    first_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    last_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    phone: Annotated[str, Field(min_length=1, max_length=30)] | None = None
    email: EmailStr | None = None
    ngo_name: Annotated[str, Field(min_length=1, max_length=200)] | None = None
    ngo_street: Annotated[str, Field(min_length=1, max_length=255)] | None = None
    ngo_postal_code: Annotated[str, Field(pattern=r"^\d{4}$")] | None = None
    ngo_city: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    ngo_davcna: Annotated[str, Field(pattern=r"^\d{8}$")] | None = None
    report_whatsapp: bool | None = None
    report_email: bool | None = None
    default_report_whatsapp: bool | None = None
    default_report_email: bool | None = None
    ngo_whatsapp_phone: Optional[str] = None
    smtp_host: Optional[str] = None

    @field_validator("ngo_whatsapp_phone", mode="before")
    @classmethod
    def normalize_wa_phone(cls, v: str | None) -> str | None:
        """Normalize to WhatsApp-native digits-only format; reject unparseable values."""
        from utils.phone import normalize_phone

        if v is None:
            return None
        normalized = normalize_phone(v)
        if v and not normalized:
            raise ValueError("Telefonska številka je prekratka ali neveljavna.")
        return normalized
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_from_name: Optional[str] = None
    evolution_api_admin_url: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    """Payload for the change-password endpoint."""

    current_password: str
    new_password: Annotated[str, Field(min_length=8)]


class ManagerResponse(BaseModel):
    """Manager profile returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    first_name: str
    last_name: str
    phone: str
    email: str
    ngo_name: str
    ngo_street: str
    ngo_postal_code: str
    ngo_city: str
    ngo_davcna: str | None = None
    created_at: datetime
    report_whatsapp: bool
    report_email: bool
    default_report_whatsapp: bool
    default_report_email: bool
    ngo_whatsapp_phone: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_from_name: Optional[str] = None
    evolution_api_admin_url: Optional[str] = None


class ConfigInfoResponse(BaseModel):
    """Response schema for GET /managers/me/config-info."""

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_from_name: str
    smtp_configured: bool
    evolution_api_admin_url: str
    wa_phone: str | None
    wa_state: str  # "open" | "connecting" | "close" | "unreachable" | "lid_unsupported"
    wa_synced: bool
    wa_env_write_ok: bool
