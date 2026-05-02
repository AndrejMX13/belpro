"""Pydantic schemas for the Volunteer entity."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.log_entry import EntryStatus


class LogEntryBrief(BaseModel):
    """Compact log entry view — used inside VolunteerDetailResponse."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    entry_date: date
    hours: Decimal
    status: EntryStatus
    location: str | None
    activity_description: str


class EmsoCheckRequest(BaseModel):
    """Plaintext EMŠO submitted for duplicate check before creating a volunteer."""

    emso: Annotated[str, Field(min_length=13, max_length=13, pattern=r"^\d{13}$")]


class EmsoCheckResponse(BaseModel):
    """Result of an EMŠO duplicate check."""

    exists: bool


class VolunteerCreate(BaseModel):
    """Fields required to register a new volunteer."""

    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    street: Annotated[str, Field(min_length=1, max_length=255)]
    # 4-digit Slovenian postal code
    postal_code: Annotated[str, Field(pattern=r"^\d{4}$")]
    city: Annotated[str, Field(min_length=1, max_length=100)]
    # Plaintext EMŠO — exactly 13 digits.  Encrypted by the service before storage.
    emso: Annotated[str, Field(min_length=13, max_length=13, pattern=r"^\d{13}$")]
    phone: Annotated[str, Field(min_length=1, max_length=30)]
    email: EmailStr | None = None


class VolunteerResponse(BaseModel):
    """Volunteer data returned to the manager dashboard.

    emso_masked is computed by the router after decryption — never exposes
    the raw ciphertext or the plaintext EMŠO.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    first_name: str
    last_name: str
    street: str
    postal_code: str
    city: str
    # Format: "**********XYZ" — last 3 digits visible, rest masked.
    emso_masked: str
    phone: str
    email: str | None
    active: bool
    registered_at: datetime
    manager_id: uuid.UUID
    hours_this_month: float = 0.0


class VolunteerDetailResponse(VolunteerResponse):
    """Volunteer with full entry history — returned by GET /volunteers/{id}."""

    log_entries: list[LogEntryBrief]


class VolunteerListResponse(BaseModel):
    """Paginated volunteer list."""

    items: list[VolunteerResponse]
    total: int
