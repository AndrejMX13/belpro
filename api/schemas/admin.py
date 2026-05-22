"""Pydantic schemas for the admin settings endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AdminSettingsResponse(BaseModel):
    """Current values of all runtime-tunable settings."""

    max_photos_per_entry: int
    photo_retention_days: int
    session_duration_hours: int
    report_auto_day: int
    report_auto_period: str
    report_auto_hour: int
    backup_hour: int
    photo_cleanup_hour: int
    backup_retention_days: int


class AdminSettingsUpdate(BaseModel):
    """Partial update for runtime-tunable settings. Only provided fields are written."""

    max_photos_per_entry: int | None = Field(None, ge=1)
    photo_retention_days: int | None = Field(None, ge=1)
    session_duration_hours: int | None = Field(None, ge=1)
    report_auto_day: int | None = Field(None, ge=1, le=28)
    report_auto_period: str | None = Field(None, pattern="^(current|previous)$")
    report_auto_hour: int | None = Field(None, ge=0, le=23)
    backup_hour: int | None = Field(None, ge=0, le=23)
    photo_cleanup_hour: int | None = Field(None, ge=0, le=23)
    backup_retention_days: int | None = Field(None, ge=1)
