"""PDF report storage — disk write and upsert of MonthlyReport rows."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.monthly_report import MonthlyReport

REPORTS_DIR = Path("/app/photos/reports")


def report_path(year: int, month: int, filename: str) -> Path:
    """Return the canonical filesystem path for a report PDF."""
    return REPORTS_DIR / str(year) / f"{month:02d}" / filename


async def persist_report(
    db: AsyncSession,
    year: int,
    month: int,
    filename: str,
    pdf_bytes: bytes,
    volunteer_id: uuid.UUID | None = None,
) -> MonthlyReport:
    """Write pdf_bytes to disk and upsert a MonthlyReport row.

    If a row already exists for (volunteer_id, year, month), it is updated
    in place — the file is overwritten and pdf_path/sent_at/generated_at
    are refreshed. No duplicate rows are ever inserted.
    """
    path = report_path(year, month, filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pdf_bytes)

    now = datetime.now(timezone.utc)

    if volunteer_id is not None:
        existing_stmt = select(MonthlyReport).where(
            MonthlyReport.volunteer_id == volunteer_id,
            MonthlyReport.period_year == year,
            MonthlyReport.period_month == month,
        )
    else:
        existing_stmt = select(MonthlyReport).where(
            MonthlyReport.volunteer_id.is_(None),
            MonthlyReport.period_year == year,
            MonthlyReport.period_month == month,
        )

    row = (await db.execute(existing_stmt)).scalar_one_or_none()

    if row is not None:
        old_path = Path(row.pdf_path)
        if old_path != path:
            old_path.unlink(missing_ok=True)
        row.pdf_path = str(path)
        row.sent_at = now
        row.generated_at = now
        await db.flush()
        return row

    row = MonthlyReport(
        volunteer_id=volunteer_id,
        period_year=year,
        period_month=month,
        pdf_path=str(path),
        sent_at=now,
        generated_at=now,
    )
    db.add(row)
    await db.flush()
    return row
