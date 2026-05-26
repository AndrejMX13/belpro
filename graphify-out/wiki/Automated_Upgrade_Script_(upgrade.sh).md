# Automated Upgrade Script (upgrade.sh)

> 13 nodes

## Key Concepts

- **loadAnalytics()** (8 connections) — `frontend/js/analytics.js`
- **analytics.js** (7 connections) — `frontend/js/analytics.js`
- **renderAnalytics()** (5 connections) — `frontend/js/analytics.js`
- **renderAnalyticsContent()** (3 connections) — `frontend/js/analytics.js`
- **_renderCharts()** (3 connections) — `frontend/js/analytics.js`
- **loadAnalytics()** (3 connections) — `frontend/js/analytics.js`
- **GET /analytics/summary** (3 connections) — `api/routers/analytics.py`
- **_destroyCharts()** (2 connections) — `frontend/js/analytics.js`
- **API.analytics.summary()** (2 connections) — `frontend/js/api.js`
- **AnalyticsSummary shape (total_hours, active_volunteer_count, hours_per_volunteer[], hours_per_location[], monthly_trend[])** (2 connections) — `api/routers/analytics.py`
- **analyticsState** (1 connections) — `frontend/js/analytics.js`
- **exportAnalyticsCsv()** (1 connections) — `frontend/js/analytics.js`
- **renderAnalytics() — analytics page** (1 connections) — `frontend/js/analytics.js`

## Relationships

- [[test_auth.py]] (6 shared connections)
- [[path]] (1 shared connections)

## Source Files

- `api/routers/analytics.py`
- `frontend/js/analytics.js`
- `frontend/js/api.js`

## Audit Trail

- EXTRACTED: 34 (83%)
- INFERRED: 7 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*