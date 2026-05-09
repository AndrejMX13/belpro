"""Analytics router — aggregated summary for the dashboard analytics page."""
from __future__ import annotations

import calendar
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.volunteer import Volunteer
from schemas.analytics import (
    AnalyticsSummary,
    HoursPerLocation,
    HoursPerVolunteer,
    MonthlyTrendPoint,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary, dependencies=[Depends(require_manager)])
async def analytics_summary(
    year: int | None = Query(default=None, ge=2020, le=2099),
    month: int | None = Query(default=None, ge=1, le=12),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> AnalyticsSummary:
    """Return aggregated analytics data scoped to the given month.

    Defaults to the current calendar month when year/month are omitted.
    Monthly trend covers the 6 calendar months ending at the selected month.
    """
    today = date.today()
    y: int = year if year is not None else today.year
    m: int = month if month is not None else today.month

    # 1. Active volunteer count — current state, not month-scoped
    active_count: int = (
        await db.execute(select(func.count()).where(Volunteer.active.is_(True)))
    ).scalar_one()

    # 2. Entry counts scoped to selected month
    count_rows = (
        await db.execute(
            select(LogEntry.status, func.count().label("cnt"))
            .where(
                func.extract("year", LogEntry.work_date) == y,
                func.extract("month", LogEntry.work_date) == m,
                LogEntry.status.in_(
                    [EntryStatus.PENDING_MANAGER, EntryStatus.APPROVED, EntryStatus.REJECTED]
                ),
            )
            .group_by(LogEntry.status)
        )
    ).all()
    counts = {row.status: row.cnt for row in count_rows}

    # 3. Hours per volunteer (approved only, selected month) + total
    vol_rows = (
        await db.execute(
            select(
                Volunteer.id,
                Volunteer.first_name,
                Volunteer.last_name,
                func.coalesce(func.sum(LogEntry.hours), Decimal("0")).label("total_hours"),
            )
            .outerjoin(
                LogEntry,
                (LogEntry.volunteer_id == Volunteer.id)
                & (func.extract("year", LogEntry.work_date) == y)
                & (func.extract("month", LogEntry.work_date) == m)
                & (LogEntry.status == EntryStatus.APPROVED),
            )
            .where(Volunteer.active.is_(True))
            .where(
                select(LogEntry.id)
                .where(
                    LogEntry.volunteer_id == Volunteer.id,
                    func.extract("year", LogEntry.work_date) == y,
                    func.extract("month", LogEntry.work_date) == m,
                )
                .correlate(Volunteer)
                .exists()
            )
            .group_by(Volunteer.id, Volunteer.first_name, Volunteer.last_name)
            .order_by(
                func.coalesce(func.sum(LogEntry.hours), Decimal("0")).desc(),
                Volunteer.last_name,
            )
        )
    ).all()
    hours_per_volunteer = [
        HoursPerVolunteer(
            volunteer_id=row.id,
            full_name=f"{row.first_name} {row.last_name}",
            total_hours=row.total_hours,
        )
        for row in vol_rows
    ]
    total_hours = sum((v.total_hours for v in hours_per_volunteer), Decimal("0"))

    # 4. Hours per location (approved only, selected month)
    loc_rows = (
        await db.execute(
            select(
                LogEntry.location,
                func.sum(LogEntry.hours).label("total_hours"),
            )
            .where(
                func.extract("year", LogEntry.work_date) == y,
                func.extract("month", LogEntry.work_date) == m,
                LogEntry.status == EntryStatus.APPROVED,
                LogEntry.location.isnot(None),
                LogEntry.location != "",
            )
            .group_by(LogEntry.location)
            .order_by(func.sum(LogEntry.hours).desc())
        )
    ).all()
    hours_per_location = [
        HoursPerLocation(location=row.location, total_hours=row.total_hours)
        for row in loc_rows
    ]

    # 5. Monthly trend — last 6 months ending at selected month
    trend_months = _preceding_months(y, m, count=6)
    first_y, first_m = trend_months[0]
    last_day = calendar.monthrange(y, m)[1]
    trend_rows = (
        await db.execute(
            select(
                func.extract("year", LogEntry.work_date).label("ty"),
                func.extract("month", LogEntry.work_date).label("tm"),
                func.sum(LogEntry.hours).label("total_hours"),
            )
            .where(
                LogEntry.status == EntryStatus.APPROVED,
                LogEntry.work_date >= date(first_y, first_m, 1),
                LogEntry.work_date <= date(y, m, last_day),
            )
            .group_by("ty", "tm")
            .order_by("ty", "tm")
        )
    ).all()
    trend_lookup = {(int(r.ty), int(r.tm)): r.total_hours for r in trend_rows}
    monthly_trend = [
        MonthlyTrendPoint(
            year=ty,
            month=tm,
            total_hours=trend_lookup.get((ty, tm), Decimal("0")),
        )
        for ty, tm in trend_months
    ]

    return AnalyticsSummary(
        year=y,
        month=m,
        total_hours=total_hours,
        active_volunteer_count=active_count,
        entries_pending=counts.get(EntryStatus.PENDING_MANAGER, 0),
        entries_approved=counts.get(EntryStatus.APPROVED, 0),
        entries_rejected=counts.get(EntryStatus.REJECTED, 0),
        hours_per_volunteer=hours_per_volunteer,
        hours_per_location=hours_per_location,
        monthly_trend=monthly_trend,
    )


def _preceding_months(year: int, month: int, count: int) -> list[tuple[int, int]]:
    """Return `count` consecutive (year, month) tuples ending at (year, month)."""
    result: list[tuple[int, int]] = []
    y, m = year, month
    for _ in range(count):
        result.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return list(reversed(result))
