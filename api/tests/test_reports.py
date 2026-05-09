import uuid
from decimal import Decimal
from datetime import date
from httpx import AsyncClient

from models.log_entry import EntryStatus


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
