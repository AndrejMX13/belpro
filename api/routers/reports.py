"""Reports router — monthly aggregation and PDF export endpoints."""
from __future__ import annotations

import io
import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pathlib import Path
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_manager
from core.settings import get_settings
from db.session import get_db
from models.log_entry import EntryStatus, LogEntry
from models.manager import Manager
from models.monthly_report import MonthlyReport
from models.volunteer import Volunteer
from schemas.report import MonthlyReportSummary, ReportHistoryItem, ReportHistoryList, VolunteerMonthlySummary
from services.email import SmtpNotConfiguredError, send_email
from services.evolution import EvolutionClient
from services.logo import logo_src
from services.report_pdf import NGOInfo, render_summary_pdf, render_volunteer_pdf
from services.report_storage import persist_report
from utils.phone import normalize_phone

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
        logo_path=logo_src(),
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
        items = [i for i in await _summary_items(db, year, month) if i.entry_count > 0]
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
    """Generate monthly PDFs and deliver them via email and/or WhatsApp.

    Defaults to the current calendar month when year/month are omitted.
    Per-volunteer: sends via email if report_email=True and email is set;
    sends via WhatsApp if report_whatsapp=True and phone is set.
    Consolidated PDF to the manager via the same channel logic.
    Returns a JSON summary of what was sent.
    """
    today = date.today()
    y = year or today.year
    m = month or today.month

    settings = get_settings()

    manager = (await db.execute(select(Manager))).scalar_one_or_none()
    if manager is None:
        raise HTTPException(status_code=503, detail="Upravljalec ni konfiguriran.")

    wa_client = EvolutionClient(
        base_url=settings.evolution_api_url,
        api_key=settings.authentication_api_key,
        instance_name=settings.evolution_instance_name,
    )

    ngo = NGOInfo(
        name=manager.ngo_name,
        street=manager.ngo_street,
        postal_code=manager.ngo_postal_code,
        city=manager.ngo_city,
        phone=manager.phone,
        email=manager.email,
        ngo_davcna=manager.ngo_davcna,
        logo_path=logo_src(),
    )

    volunteers: list[Volunteer] = list(
        (await db.execute(select(Volunteer).where(Volunteer.active.is_(True)))).scalars().all()
    )

    sent_via_email: list[str] = []
    sent_via_whatsapp: list[str] = []
    skipped_no_entries: list[str] = []
    skipped_no_channel: list[str] = []
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
                    ).order_by(LogEntry.work_date)
                )
            )
            .scalars()
            .all()
        )

        if not entries:
            skipped_no_entries.append(f"{vol.first_name} {vol.last_name}")
            continue

        will_email = bool(vol.report_email and vol.email)
        will_whatsapp = bool(vol.report_whatsapp and vol.phone)

        if not will_email and not will_whatsapp:
            skipped_no_channel.append(f"{vol.first_name} {vol.last_name}")
            continue

        pdf_bytes = render_volunteer_pdf(vol.first_name, vol.last_name, y, m, entries, ngo=ngo)
        filename = f"porocilo_{vol.last_name}_{vol.first_name}_{y}_{m:02d}.pdf"
        caption = f"BelPro — mesečno poročilo {m:02d}/{y}"
        await persist_report(db, y, m, filename, pdf_bytes, volunteer_id=vol.id)

        if will_email:
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
                    subject=caption,
                    body_html=body,
                    attachment_bytes=pdf_bytes,
                    attachment_filename=filename,
                )
                sent_via_email.append(f"{vol.first_name} {vol.last_name} <{vol.email}>")
            except SmtpNotConfiguredError as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{vol.first_name} {vol.last_name} (e-pošta): {exc}")

        if will_whatsapp:
            normalized = normalize_phone(vol.phone)
            if normalized:
                try:
                    await wa_client.send_document(normalized, pdf_bytes, filename, caption)
                    sent_via_whatsapp.append(f"{vol.first_name} {vol.last_name}")
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{vol.first_name} {vol.last_name} (WhatsApp): {exc}")

    # Consolidated PDF → manager
    manager_email_sent = False
    manager_whatsapp_sent = False
    manager_will_email = bool(manager.report_email and manager.email)
    manager_will_whatsapp = bool(manager.report_whatsapp and manager.phone)

    if manager_will_email or manager_will_whatsapp:
        mgr_items = [i for i in await _summary_items(db, y, m) if i.entry_count > 0]
        consolidated_bytes = render_summary_pdf(y, m, mgr_items, ngo=ngo)
        consolidated_filename = f"porocilo_skupno_{y}_{m:02d}.pdf"
        mgr_caption = f"BelPro — skupno mesečno poročilo {m:02d}/{y}"
        await persist_report(db, y, m, consolidated_filename, consolidated_bytes, volunteer_id=None)

        if manager_will_email:
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
                    subject=mgr_caption,
                    body_html=manager_body,
                    attachment_bytes=consolidated_bytes,
                    attachment_filename=consolidated_filename,
                )
                manager_email_sent = True
            except SmtpNotConfiguredError as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc
            except Exception as exc:  # noqa: BLE001
                errors.append(f"Upravljalec (e-pošta): {exc}")

        if manager_will_whatsapp:
            normalized_mgr = normalize_phone(manager.phone)
            if normalized_mgr:
                try:
                    await wa_client.send_document(
                        normalized_mgr, consolidated_bytes, consolidated_filename, mgr_caption
                    )
                    manager_whatsapp_sent = True
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"Upravljalec (WhatsApp): {exc}")

    await db.commit()

    return JSONResponse(
        {
            "year": y,
            "month": m,
            "sent_via_email": sent_via_email,
            "sent_via_whatsapp": sent_via_whatsapp,
            "skipped_no_entries": skipped_no_entries,
            "skipped_no_channel": skipped_no_channel,
            "manager_email_sent": manager_email_sent,
            "manager_whatsapp_sent": manager_whatsapp_sent,
            "errors": errors,
        }
    )


@router.get("/history", response_model=ReportHistoryList, dependencies=[Depends(require_manager)])
async def get_report_history(
    year: int | None = Query(default=None, ge=2020, le=2099),
    month: int | None = Query(default=None, ge=1, le=12),
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> ReportHistoryList:
    """List persisted PDF reports, newest first. Optionally filter by year and/or month."""
    stmt = (
        select(MonthlyReport)
        .options(selectinload(MonthlyReport.volunteer))
        .order_by(MonthlyReport.generated_at.desc())
    )
    if year is not None:
        stmt = stmt.where(MonthlyReport.period_year == year)
    if month is not None:
        stmt = stmt.where(MonthlyReport.period_month == month)
    rows = (await db.execute(stmt)).scalars().all()
    items = [
        ReportHistoryItem(
            id=r.id,
            period_year=r.period_year,
            period_month=r.period_month,
            volunteer_id=r.volunteer_id,
            volunteer_name=(
                f"{r.volunteer.last_name} {r.volunteer.first_name}"
                if r.volunteer else None
            ),
            generated_at=r.generated_at,
            sent_at=r.sent_at,
            filename=Path(r.pdf_path).name,
        )
        for r in rows
    ]
    return ReportHistoryList(items=items, total=len(items))


@router.get("/history/{report_id}/pdf", response_model=None, dependencies=[Depends(require_manager)])
async def download_history_pdf(
    report_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> FileResponse:
    """Stream a previously generated PDF from disk. Returns 404 if the row or file is missing."""
    row = (
        await db.execute(select(MonthlyReport).where(MonthlyReport.id == report_id))
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Porocilo ne obstaja.")
    path = Path(row.pdf_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF datoteka ni najdena na disku.")
    return FileResponse(path=str(path), media_type="application/pdf", filename=path.name)
