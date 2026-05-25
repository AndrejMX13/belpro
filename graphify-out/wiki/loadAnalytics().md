# loadAnalytics()

> 5 nodes · cohesion 0.50

## Key Concepts

- **loadAnalytics()** (3 connections) — `frontend/js/analytics.js`
- **GET /analytics/summary** (3 connections) — `api/routers/analytics.py`
- **API.analytics.summary()** (2 connections) — `frontend/js/api.js`
- **AnalyticsSummary shape (total_hours, active_volunteer_count, hours_per_volunteer[], hours_per_location[], monthly_trend[])** (2 connections) — `api/routers/analytics.py`
- **renderAnalytics() — analytics page** (1 connections) — `frontend/js/analytics.js`

## Relationships

- [[volunteers.js]] (1 shared connections)

## Source Files

- `api/routers/analytics.py`
- `frontend/js/analytics.js`
- `frontend/js/api.js`

## Audit Trail

- EXTRACTED: 11 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*