"""Pydantic schemas for monthly report summaries."""
from __future__ import annotations

import uuid
from decimal import Decimal

from pydantic import BaseModel


class VolunteerMonthlySummary(BaseModel):
    """Per-volunteer aggregated totals for a given month."""

    volunteer_id: uuid.UUID
    first_name: str
    last_name: str
    total_hours: Decimal
    entry_count: int


class MonthlyReportSummary(BaseModel):
    """Aggregated monthly summary across all active volunteers."""

    year: int
    month: int
    items: list[VolunteerMonthlySummary]
    total_hours: Decimal
    total_entries: int
