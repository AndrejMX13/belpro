"""Pydantic schemas for monthly report summaries."""
from __future__ import annotations

import uuid
from datetime import datetime
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


class ReportHistoryItem(BaseModel):
    """One persisted report record in the history list."""

    id: uuid.UUID
    period_year: int
    period_month: int
    volunteer_id: uuid.UUID | None
    volunteer_name: str | None   # "Priimek Ime", or None for consolidated
    generated_at: datetime
    sent_at: datetime | None
    filename: str                # basename of pdf_path


class ReportHistoryList(BaseModel):
    """List of persisted report records."""

    items: list[ReportHistoryItem]
    total: int
