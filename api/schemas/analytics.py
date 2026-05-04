"""Pydantic schemas for the analytics summary endpoint."""
from __future__ import annotations

import uuid
from decimal import Decimal

from pydantic import BaseModel


class HoursPerVolunteer(BaseModel):
    """Per-volunteer approved hours for a given month."""

    volunteer_id: uuid.UUID
    full_name: str
    total_hours: Decimal


class HoursPerLocation(BaseModel):
    """Approved hours grouped by location for a given month."""

    location: str
    total_hours: Decimal


class MonthlyTrendPoint(BaseModel):
    """Total approved hours for a single calendar month."""

    year: int
    month: int
    total_hours: Decimal


class AnalyticsSummary(BaseModel):
    """Aggregated analytics data for a given month."""

    year: int
    month: int
    total_hours: Decimal
    active_volunteer_count: int
    entries_pending: int
    entries_approved: int
    entries_rejected: int
    hours_per_volunteer: list[HoursPerVolunteer]
    hours_per_location: list[HoursPerLocation]
    monthly_trend: list[MonthlyTrendPoint]
