# Code: Check Pending (Manual)

> 16 nodes

## Key Concepts

- **analytics_summary()** (7 connections) — `api/routers/analytics.py`
- **analytics.py** (6 connections) — `api/schemas/analytics.py`
- **analytics.py** (4 connections) — `api/routers/analytics.py`
- **HoursPerVolunteer** (4 connections) — `api/schemas/analytics.py`
- **HoursPerLocation** (4 connections) — `api/schemas/analytics.py`
- **MonthlyTrendPoint** (4 connections) — `api/schemas/analytics.py`
- **AnalyticsSummary** (4 connections) — `api/schemas/analytics.py`
- **_preceding_months()** (3 connections) — `api/routers/analytics.py`
- **Analytics router — aggregated summary for the dashboard analytics page.** (1 connections) — `api/routers/analytics.py`
- **Return aggregated analytics data scoped to the given month.      Defaults to t** (1 connections) — `api/routers/analytics.py`
- **Return `count` consecutive (year, month) tuples ending at (year, month).** (1 connections) — `api/routers/analytics.py`
- **Pydantic schemas for the analytics summary endpoint.** (1 connections) — `api/schemas/analytics.py`
- **Per-volunteer approved hours for a given month.** (1 connections) — `api/schemas/analytics.py`
- **Approved hours grouped by location for a given month.** (1 connections) — `api/schemas/analytics.py`
- **Total approved hours for a single calendar month.** (1 connections) — `api/schemas/analytics.py`
- **Aggregated analytics data for a given month.** (1 connections) — `api/schemas/analytics.py`

## Relationships

- [[test_app_settings.py]] (4 shared connections)

## Source Files

- `api/routers/analytics.py`
- `api/schemas/analytics.py`

## Audit Trail

- EXTRACTED: 34 (77%)
- INFERRED: 10 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*