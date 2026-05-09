"""Reports router — monthly aggregation and PDF export endpoints."""
from __future__ import annotations

import io
import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.manager import Manager
from models.volunteer import Volunteer
from schemas.report import MonthlyReportSummary, VolunteerMonthlySummary
from services.email import SmtpNotConfiguredError, send_email
from services.report_pdf import NGOInfo, render_summary_pdf, render_volunteer_pdf

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
                func.extract("year", LogEntry.work_date) == year,
                func.extract("month", LogEntry.work_date) == month,
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
            & (func.extract("year", LogEntry.work_date) == year)
            & (func.extract("month", LogEntry.work_date) == month)
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
    manager = (await db.execute(select(Manager))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=503, detail="Upravljalec ni konfiguriran.")

    ngo = NGOInfo(
        name=manager.ngo_name,
        street=manager.ngo_street,
        postal_code=manager.ngo_postal_code,
        city=manager.ngo_city,
        phone=manager.phone,
        email=manager.email,
        ngo_davcna=manager.ngo_davcna,
    )

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
                func.extract("year", LogEntry.work_date) == year,
                func.extract("month", LogEntry.work_date) == month,
                LogEntry.status == EntryStatus.APPROVED,
            )
            .order_by(LogEntry.work_date)
        )
        entries = (await db.execute(entries_stmt)).scalars().all()
        pdf_bytes = render_volunteer_pdf(vol.first_name, vol.last_name, year, month, entries, ngo=ngo)
        filename = f"porocilo_{vol.last_name}_{vol.first_name}_{year}_{month:02d}.pdf"
    else:
        items = await _summary_items(db, year, month)
        pdf_bytes = render_summary_pdf(year, month, items, ngo=ngo)
        filename = f"porocilo_{year}_{month:02d}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/send-monthly", dependencies=[Depends(require_manager)])
async def send_monthly_reports(
    year: int | None = Query(default=None, ge=2020, le=2099),
    month: int | None = Query(default=None, ge=1, le=12),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> JSONResponse:
    """Generate monthly PDFs and send them via email.

    Defaults to the current calendar month when year/month are omitted.
    Sends per-volunteer PDFs to volunteers with report_email=True.
    Sends consolidated PDF to the manager if manager.report_email=True.
    Returns a JSON summary of what was sent.
    """
    today = date.today()
    y = year or today.year
    m = month or today.month

    settings = get_settings()

    manager = (await db.execute(select(Manager))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=503, detail="Upravljalec ni konfiguriran.")

    ngo = NGOInfo(
        name=manager.ngo_name,
        street=manager.ngo_street,
        postal_code=manager.ngo_postal_code,
        city=manager.ngo_city,
        phone=manager.phone,
        email=manager.email,
        ngo_davcna=manager.ngo_davcna,
    )

    volunteers: list[Volunteer] = list(
        (await db.execute(select(Volunteer).where(Volunteer.active.is_(True)))).scalars().all()
    )

    sent_to_volunteers: list[str] = []
    skipped_no_entries: list[str] = []
    skipped_no_email: list[str] = []
    errors: list[str] = []

    for vol in volunteers:
        entries = list(
            (
                await db.execute(
                    select(LogEntry).where(
                        LogEntry.volunteer_id == vol.id,
                        func.extract("year", LogEntry.work_date) == y,
                        func.extract("month", LogEntry.work_date) == m,
                        LogEntry.status == EntryStatus.APPROVED,
                    )
                )
            )
            .scalars()
            .all()
        )

        if not entries:
            skipped_no_entries.append(f"{vol.first_name} {vol.last_name}")
            continue

        if not vol.report_email or not vol.email:
            skipped_no_email.append(f"{vol.first_name} {vol.last_name}")
            continue

        pdf_bytes = render_volunteer_pdf(vol.first_name, vol.last_name, y, m, entries, ngo=ngo)
        filename = f"porocilo_{vol.last_name}_{vol.first_name}_{y}_{m:02d}.pdf"
        subject = f"BelPro — mesečno poročilo {m:02d}/{y}"
        body = (
            f"<p>Spoštovani/-a {vol.first_name},</p>"
            f"<p>v priponki najdete mesečno poročilo za {m:02d}/{y}.</p>"
            f"<p>Lep pozdrav,<br>{manager.ngo_name}</p>"
        )

        try:
            await send_email(
                smtp_host=manager.smtp_host,
                smtp_port=manager.smtp_port,
                smtp_user=manager.smtp_user,
                smtp_from_name=manager.smtp_from_name,
                smtp_password=settings.smtp_password,
                to_address=vol.email,
                subject=subject,
                body_html=body,
                attachment_bytes=pdf_bytes,
                attachment_filename=filename,
            )
            sent_to_volunteers.append(f"{vol.first_name} {vol.last_name} <{vol.email}>")
        except SmtpNotConfiguredError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{vol.first_name} {vol.last_name}: {exc}")

    # Consolidated PDF → manager
    manager_sent = False
    if manager.report_email and manager.email:
        items = await _summary_items(db, y, m)
        consolidated_bytes = render_summary_pdf(y, m, items, ngo=ngo)
        consolidated_filename = f"porocilo_skupno_{y}_{m:02d}.pdf"
        manager_subject = f"BelPro — skupno mesečno poročilo {m:02d}/{y}"
        manager_body = (
            f"<p>Spoštovani/-a {manager.first_name},</p>"
            f"<p>v priponki najdete skupno mesečno poročilo za {m:02d}/{y}.</p>"
            f"<p>BelPro</p>"
        )
        try:
            await send_email(
                smtp_host=manager.smtp_host,
                smtp_port=manager.smtp_port,
                smtp_user=manager.smtp_user,
                smtp_from_name=manager.smtp_from_name,
                smtp_password=settings.smtp_password,
                to_address=manager.email,
                subject=manager_subject,
                body_html=manager_body,
                attachment_bytes=consolidated_bytes,
                attachment_filename=consolidated_filename,
            )
            manager_sent = True
        except SmtpNotConfiguredError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Upravljalec: {exc}")

    return JSONResponse(
        {
            "year": y,
            "month": m,
            "sent_to_volunteers": sent_to_volunteers,
            "skipped_no_entries": skipped_no_entries,
            "skipped_no_email": skipped_no_email,
            "manager_sent": manager_sent,
            "errors": errors,
        }
    )
