"""Pydantic schemas for the LogEntry entity."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from models.log_entry import EntryStatus


class LogEntryCreate(BaseModel):
    """Fields required to create a new log entry."""

    volunteer_id: uuid.UUID
    work_date: date
    activity_description: Annotated[str, Field(min_length=1)]
    hours: Annotated[Decimal, Field(ge=Decimal("0.5"), le=Decimal("24.0"))]
    location: str | None = None
    raw_transcript: str | None = None
    # Defaults to pending_manager for dashboard / n8n-created entries.
    # n8n may override to pending_volunteer when the WhatsApp confirmation flow is active.
    status: EntryStatus = EntryStatus.PENDING_MANAGER


class LogEntryResponse(BaseModel):
    """Full log entry returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    volunteer_id: uuid.UUID
    work_date: date
    activity_description: str
    raw_transcript: str | None
    hours: Decimal
    location: str | None
    status: EntryStatus
    photos: list[PhotoResponse] = []
    volunteer_confirmed_at: datetime | None
    manager_approved_at: datetime | None
    manager_notified_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PhotoResponse(BaseModel):
    """A single photo attached to a log entry."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    log_entry_id: uuid.UUID
    photo_path: str
    photo_exif_timestamp: datetime | None
    photo_exif_lat: Decimal | None
    photo_exif_lon: Decimal | None
    uploaded_at: datetime


class PhotoBase64Request(BaseModel):
    """Base64-encoded photo upload — used by n8n workflows."""

    image_base64: str
    filename: str


class LogEntryUpdate(BaseModel):
    """Editable fields — blocked once the entry is approved."""

    activity_description: Annotated[str, Field(min_length=1)] | None = None
    hours: Annotated[Decimal, Field(ge=Decimal("0.5"), le=Decimal("24.0"))] | None = None
    location: str | None = None
    work_date: date | None = None


class LogEntryListResponse(BaseModel):
    """Paginated log entry list."""

    items: list[LogEntryResponse]
    total: int
