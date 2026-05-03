"""Reports router — monthly aggregation and PDF export endpoints."""
from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.volunteer import Volunteer
from schemas.report import MonthlyReportSummary, VolunteerMonthlySummary

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly", response_model=MonthlyReportSummary, dependencies=[Depends(require_manager)])
async def monthly_summary(
    year: int = Query(..., ge=2020, le=2099),
    month: int = Query(..., ge=1, le=12),
    with_entries_only: bool = Query(default=False),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> MonthlyReportSummary:
    """Return per-volunteer totals of approved entries for the given year/month.

    When with_entries_only=true, only volunteers with at least one entry (any status)
    in the selected month are included.
    """
    stmt = (
        select(
            Volunteer.id,
            Volunteer.first_name,
            Volunteer.last_name,
            func.coalesce(func.sum(LogEntry.hours), Decimal("0")).label("total_hours"),
            func.count(LogEntry.id).label("entry_count"),
        )
        .outerjoin(
            LogEntry,
            (LogEntry.volunteer_id == Volunteer.id)
            & (func.extract("year", LogEntry.entry_date) == year)
            & (func.extract("month", LogEntry.entry_date) == month)
            & (LogEntry.status == EntryStatus.APPROVED),
        )
        .where(Volunteer.active.is_(True))
        .group_by(Volunteer.id, Volunteer.first_name, Volunteer.last_name)
        .order_by(Volunteer.last_name, Volunteer.first_name)
    )

    if with_entries_only:
        any_entry = (
            select(LogEntry.id)
            .where(
                LogEntry.volunteer_id == Volunteer.id,
                func.extract("year", LogEntry.entry_date) == year,
                func.extract("month", LogEntry.entry_date) == month,
            )
            .correlate(Volunteer)
            .exists()
        )
        stmt = stmt.where(any_entry)

    rows = (await db.execute(stmt)).all()
    items = [
        VolunteerMonthlySummary(
            volunteer_id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            total_hours=row.total_hours,
            entry_count=row.entry_count,
        )
        for row in rows
    ]
    total_hours = sum((i.total_hours for i in items), Decimal("0"))
    total_entries = sum(i.entry_count for i in items)
    return MonthlyReportSummary(
        year=year,
        month=month,
        items=items,
        total_hours=total_hours,
        total_entries=total_entries,
    )


@router.post("/monthly/pdf", status_code=501, dependencies=[Depends(require_manager)])
async def generate_monthly_pdf(
    year: int = Query(..., ge=2020, le=2099),
    month: int = Query(..., ge=1, le=12),
    volunteer_id: uuid.UUID | None = Query(default=None),
) -> dict[str, str]:
    """Generate a monthly PDF report. Not yet implemented."""
    raise HTTPException(status_code=501, detail="Generiranje PDF še ni implementirano.")
