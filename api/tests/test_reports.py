import uuid
from decimal import Decimal
from datetime import date
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from sqlalchemy import select

from models.error_log import ErrorLog
from models.log_entry import EntryStatus
from services.email import SmtpNotConfiguredError
from services.report_pdf import NGOInfo, ngo_header_html


async def test_monthly_summary_empty(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/reports/monthly?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["year"] == 2026
    assert data["month"] == 1
    assert data["total_entries"] == 0
    assert float(data["total_hours"]) == 0.0


async def test_monthly_summary_counts_only_approved_entries(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(
        v.id, work_date=date(2026, 1, 15), hours=Decimal("3.0"),
        status=EntryStatus.APPROVED,
    )
    await log_entry_factory(
        v.id, work_date=date(2026, 1, 20), hours=Decimal("2.0"),
        status=EntryStatus.PENDING_MANAGER,
    )
    r = await client.get("/api/reports/monthly?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["total_entries"] == 1
    assert float(data["total_hours"]) == 3.0


async def test_monthly_summary_missing_params_returns_422(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.get("/api/reports/monthly", headers=auth)
    assert r.status_code == 422


async def test_monthly_pdf_empty_month_returns_pdf_content_type(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.post("/api/reports/monthly/pdf?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    assert "application/pdf" in r.headers["content-type"]


async def test_monthly_pdf_for_unknown_volunteer_returns_404(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.post(
        f"/api/reports/monthly/pdf?year=2026&month=1&volunteer_id={uuid.uuid4()}",
        headers=auth,
    )
    assert r.status_code == 404


async def test_with_entries_only_excludes_volunteers_with_no_entries(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v_with = await volunteer_factory()
    _v_without = await volunteer_factory()
    await log_entry_factory(v_with.id, work_date=date(2026, 2, 10), status=EntryStatus.PENDING_MANAGER)

    r = await client.get(
        "/api/reports/monthly?year=2026&month=2&with_entries_only=true", headers=auth
    )
    assert r.status_code == 200
    ids = [item["volunteer_id"] for item in r.json()["items"]]
    assert str(v_with.id) in ids
    assert str(_v_without.id) not in ids


async def test_with_entries_only_includes_any_status_not_only_approved(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(v.id, work_date=date(2026, 2, 5), status=EntryStatus.PENDING_MANAGER)

    r = await client.get(
        "/api/reports/monthly?year=2026&month=2&with_entries_only=true", headers=auth
    )
    assert r.status_code == 200
    ids = [item["volunteer_id"] for item in r.json()["items"]]
    assert str(v.id) in ids


async def test_with_entries_only_false_includes_all_active_volunteers(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    v1 = await volunteer_factory()
    v2 = await volunteer_factory()

    r = await client.get(
        "/api/reports/monthly?year=2026&month=2&with_entries_only=false", headers=auth
    )
    assert r.status_code == 200
    ids = [item["volunteer_id"] for item in r.json()["items"]]
    assert str(v1.id) in ids
    assert str(v2.id) in ids



# ── logo in PDF header ────────────────────────────────────────────────────────

def test_ngo_header_html_without_logo():
    """ngo_header_html must not include an img tag when logo_path is None."""
    ngo = NGOInfo(name="Test NGO", street="Testna 1", postal_code="1000", city="Ljubljana")
    html = ngo_header_html(ngo)
    assert "<img" not in html


def test_ngo_header_html_with_logo():
    """ngo_header_html must include an img tag with data URI src when logo_path is set."""
    ngo = NGOInfo(
        name="Test NGO",
        street="Testna 1",
        postal_code="1000",
        city="Ljubljana",
        logo_path="data:image/png;base64,FAKE",
    )
    html = ngo_header_html(ngo)
    assert "<img" in html
    assert "data:image/png;base64,FAKE" in html


# ── report delivery error logging ─────────────────────────────────────────────


async def test_send_monthly_email_failure_logged(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """Email delivery failure writes an ErrorLog row and appears in response errors."""
    v = await volunteer_factory(report_email=True, email="vol@test.si")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 1), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    with patch("routers.reports.send_email", new_callable=AsyncMock,
               side_effect=Exception("SMTP connection refused")):
        r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("e-pošta" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
    assert any("e-pošta" in (row.detail or "") for row in rows)


async def test_send_monthly_whatsapp_failure_logged(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """WhatsApp delivery failure writes an ErrorLog row and appears in response errors."""
    v = await volunteer_factory(report_whatsapp=True, phone="+38641111222")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 2), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    with patch(
        "services.evolution.EvolutionClient.send_document",
        new_callable=AsyncMock,
        side_effect=Exception("Evolution 500"),
    ):
        r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("WhatsApp" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
    assert any("WhatsApp" in (row.detail or "") for row in rows)


async def test_send_monthly_smtp_not_configured_does_not_abort_batch(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """SmtpNotConfiguredError must NOT abort the batch — response is 200 with error in list."""
    v = await volunteer_factory(report_email=True, email="vol@test.si")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 3), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    with patch("routers.reports.send_email", new_callable=AsyncMock,
               side_effect=SmtpNotConfiguredError("SMTP ni konfiguriran")):
        r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("e-pošta" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
    assert any("e-pošta" in (row.detail or "") for row in rows)


async def test_send_monthly_invalid_phone_logged(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """Volunteer with WhatsApp enabled but invalid phone gets an error log entry."""
    v = await volunteer_factory(report_whatsapp=True, phone="not-a-phone")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 4), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("WhatsApp" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
