from decimal import Decimal
from datetime import date
from httpx import AsyncClient

from models.log_entry import EntryStatus


_REQUIRED_KEYS = {
    "year", "month", "total_hours", "active_volunteer_count",
    "entries_pending", "entries_approved", "entries_rejected",
    "hours_per_volunteer", "hours_per_location", "monthly_trend",
}


async def test_analytics_summary_default_month(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.get("/api/analytics/summary", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert _REQUIRED_KEYS.issubset(data.keys())


async def test_analytics_summary_explicit_month(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.get("/api/analytics/summary?year=2026&month=1", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["year"] == 2026
    assert data["month"] == 1


async def test_analytics_summary_counts_approved_hours(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 10), hours=Decimal("5.0"),
        status=EntryStatus.APPROVED,
    )
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 11), hours=Decimal("3.0"),
        status=EntryStatus.PENDING_MANAGER,
    )
    r = await client.get("/api/analytics/summary?year=2026&month=3", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert float(data["total_hours"]) == 5.0
    assert data["entries_pending"] == 1
    assert data["entries_approved"] == 1


async def test_analytics_summary_active_volunteer_count(
    client: AsyncClient, auth: dict, volunteer_factory
) -> None:
    await volunteer_factory(active=True)
    await volunteer_factory(active=False)
    r = await client.get("/api/analytics/summary", headers=auth)
    assert r.status_code == 200
    assert r.json()["active_volunteer_count"] == 1


async def test_analytics_summary_monthly_trend_has_6_points(
    client: AsyncClient, auth: dict
) -> None:
    r = await client.get("/api/analytics/summary?year=2026&month=6", headers=auth)
    assert r.status_code == 200
    assert len(r.json()["monthly_trend"]) == 6
