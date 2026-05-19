"""Tests for PDF report persistence and history endpoints."""
from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.monthly_report import MonthlyReport


async def test_persist_report_creates_file_and_row(
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    volunteer_factory,
) -> None:
    """persist_report() must write bytes to disk and insert a MonthlyReport row."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")

    from services.report_storage import persist_report

    v = await volunteer_factory()
    row = await persist_report(
        db_session, year=2026, month=3, filename="test.pdf",
        pdf_bytes=b"%PDF-1.4 test", volunteer_id=v.id,
    )

    expected = tmp_path / "reports" / "2026" / "03" / "test.pdf"
    assert expected.exists(), "PDF file must be written to disk"
    assert expected.read_bytes() == b"%PDF-1.4 test"
    assert row.period_year == 2026
    assert row.period_month == 3
    assert row.volunteer_id == v.id
    assert row.pdf_path == str(expected)
    assert row.sent_at is not None


async def test_persist_report_consolidated_has_null_volunteer(
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Consolidated report rows must have volunteer_id=None."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")

    from services.report_storage import persist_report

    row = await persist_report(
        db_session, year=2026, month=3, filename="skupno.pdf",
        pdf_bytes=b"%PDF consolidated", volunteer_id=None,
    )
    assert row.volunteer_id is None


async def test_persist_report_overwrites_on_resend(
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    volunteer_factory,
) -> None:
    """Second persist_report() for same (volunteer, year, month) must overwrite — no new DB row."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")

    from services.report_storage import persist_report

    v = await volunteer_factory()

    row1 = await persist_report(
        db_session, 2026, 5, "first.pdf", b"%PDF first", volunteer_id=v.id,
    )
    first_id = row1.id

    row2 = await persist_report(
        db_session, 2026, 5, "second.pdf", b"%PDF second", volunteer_id=v.id,
    )

    # Same DB row (same id), updated content
    assert row2.id == first_id, "Must reuse the existing row, not insert a new one"
    assert row2.pdf_path.endswith("second.pdf"), "pdf_path must be updated"

    # Only one row in DB for this volunteer+period
    all_rows = (await db_session.execute(
        select(MonthlyReport).where(
            MonthlyReport.volunteer_id == v.id,
            MonthlyReport.period_year == 2026,
            MonthlyReport.period_month == 5,
        )
    )).scalars().all()
    assert len(all_rows) == 1

    # New file must exist with updated content
    new_path = Path(row2.pdf_path)
    assert new_path.exists()
    assert new_path.read_bytes() == b"%PDF second"


async def test_persist_report_consolidated_overwrites_on_resend(
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Second persist_report() for consolidated (volunteer_id=None, year, month) must overwrite."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")

    from services.report_storage import persist_report

    row1 = await persist_report(db_session, 2026, 5, "skupno_v1.pdf", b"%PDF v1", volunteer_id=None)
    first_id = row1.id

    row2 = await persist_report(db_session, 2026, 5, "skupno_v2.pdf", b"%PDF v2", volunteer_id=None)

    assert row2.id == first_id
    all_rows = (await db_session.execute(
        select(MonthlyReport).where(
            MonthlyReport.volunteer_id.is_(None),
            MonthlyReport.period_year == 2026,
            MonthlyReport.period_month == 5,
        )
    )).scalars().all()
    assert len(all_rows) == 1

    new_path = Path(row2.pdf_path)
    assert new_path.exists()
    assert new_path.read_bytes() == b"%PDF v2"


async def test_get_history_empty(client: AsyncClient, auth: dict) -> None:
    """GET /reports/history with no rows returns empty list."""
    r = await client.get("/api/reports/history", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["items"] == []
    assert data["total"] == 0


async def test_get_history_returns_items(
    client: AsyncClient, auth: dict,
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    volunteer_factory,
) -> None:
    """GET /reports/history returns one item per MonthlyReport row."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")
    from services.report_storage import persist_report

    v = await volunteer_factory()
    await persist_report(db_session, 2026, 1, f"porocilo_{v.last_name}_2026_01.pdf", b"%PDF", volunteer_id=v.id)
    await persist_report(db_session, 2026, 1, "porocilo_skupno_2026_01.pdf", b"%PDF", volunteer_id=None)

    r = await client.get("/api/reports/history", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    names = [item["volunteer_name"] for item in data["items"]]
    assert f"{v.last_name} {v.first_name}" in names
    assert None in names


async def test_get_history_filter_by_year_month(
    client: AsyncClient, auth: dict,
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """year/month query params filter history rows correctly."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")
    from services.report_storage import persist_report

    await persist_report(db_session, 2026, 1, "jan.pdf", b"%PDF")
    await persist_report(db_session, 2026, 2, "feb.pdf", b"%PDF")

    r = await client.get("/api/reports/history?year=2026&month=1", headers=auth)
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["period_month"] == 1


async def test_get_history_pdf_streams_file(
    client: AsyncClient, auth: dict,
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GET /reports/history/{id}/pdf returns 200 with application/pdf content-type."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")
    from services.report_storage import persist_report

    row = await persist_report(db_session, 2026, 1, "report.pdf", b"%PDF-1.4 test content")

    r = await client.get(f"/api/reports/history/{row.id}/pdf", headers=auth)
    assert r.status_code == 200
    assert "application/pdf" in r.headers["content-type"]
    assert r.content == b"%PDF-1.4 test content"


async def test_get_history_pdf_missing_file_returns_404(
    client: AsyncClient, auth: dict,
    db_session: AsyncSession, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GET /reports/history/{id}/pdf returns 404 when the file is deleted from disk."""
    import services.report_storage as rs
    monkeypatch.setattr(rs, "REPORTS_DIR", tmp_path / "reports")
    from services.report_storage import persist_report

    row = await persist_report(db_session, 2026, 1, "gone.pdf", b"%PDF")
    Path(row.pdf_path).unlink()   # simulate deleted file

    r = await client.get(f"/api/reports/history/{row.id}/pdf", headers=auth)
    assert r.status_code == 404


async def test_get_history_pdf_unknown_id_returns_404(
    client: AsyncClient, auth: dict,
) -> None:
    """GET /reports/history/{id}/pdf returns 404 for a nonexistent report ID."""
    r = await client.get(f"/api/reports/history/{uuid.uuid4()}/pdf", headers=auth)
    assert r.status_code == 404
