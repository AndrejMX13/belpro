"""Reports router — monthly aggregation and PDF export endpoints."""
from __future__ import annotations

import io
import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.volunteer import Volunteer
from schemas.report import MonthlyReportSummary, VolunteerMonthlySummary
from services.report_pdf import render_summary_pdf, render_volunteer_pdf

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
    items = await _summary_items(db, year, month)

    if with_entries_only:
        # Filter in Python — _summary_items always returns all active volunteers.
        # We need any-status entries, so we run a targeted EXISTS query per volunteer
        # rather than polluting _summary_items with an optional WHERE clause.
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
        stmt = (
            select(Volunteer.id)
            .where(Volunteer.active.is_(True))
            .where(any_entry)
        )
        active_ids = {row.id for row in (await db.execute(stmt)).all()}
        items = [i for i in items if i.volunteer_id in active_ids]

    total_hours = sum((i.total_hours for i in items), Decimal("0"))
    total_entries = sum(i.entry_count for i in items)
    return MonthlyReportSummary(
        year=year,
        month=month,
        items=items,
        total_hours=total_hours,
        total_entries=total_entries,
    )


async def _summary_items(
    db: AsyncSession, year: int, month: int
) -> list[VolunteerMonthlySummary]:
    """Run the monthly aggregation query and return per-volunteer summaries."""
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
    rows = (await db.execute(stmt)).all()
    return [
        VolunteerMonthlySummary(
            volunteer_id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            total_hours=row.total_hours,
            entry_count=row.entry_count,
        )
        for row in rows
    ]


@router.post("/monthly/pdf", dependencies=[Depends(require_manager)])
async def generate_monthly_pdf(
    year: int = Query(..., ge=2020, le=2099),
    month: int = Query(..., ge=1, le=12),
    volunteer_id: uuid.UUID | None = Query(default=None),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> StreamingResponse:
    """Generate a monthly PDF report for one volunteer or all active volunteers."""
    if volunteer_id:
        vol = (
            await db.execute(select(Volunteer).where(Volunteer.id == volunteer_id))
        ).scalar_one_or_none()
        if not vol:
            raise HTTPException(status_code=404, detail="Prostovoljec ne obstaja.")

        entries_stmt = (
            select(LogEntry)
            .where(
                LogEntry.volunteer_id == volunteer_id,
                func.extract("year", LogEntry.entry_date) == year,
                func.extract("month", LogEntry.entry_date) == month,
                LogEntry.status == EntryStatus.APPROVED,
            )
            .order_by(LogEntry.entry_date)
        )
        entries = (await db.execute(entries_stmt)).scalars().all()
        pdf_bytes = render_volunteer_pdf(vol.first_name, vol.last_name, year, month, entries)
        filename = f"porocilo_{vol.last_name}_{vol.first_name}_{year}_{month:02d}.pdf"
    else:
        items = await _summary_items(db, year, month)
        pdf_bytes = render_summary_pdf(year, month, items)
        filename = f"porocilo_{year}_{month:02d}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
