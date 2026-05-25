# test_analytics.py

> 10 nodes · cohesion 0.20

## Key Concepts

- **test_analytics.py** (7 connections) — `api/tests/test_analytics.py`
- **test_analytics_rejected_hours_excluded()** (4 connections) — `api/tests/test_analytics.py`
- **test_analytics_all_rejected_returns_zero_hours()** (4 connections) — `api/tests/test_analytics.py`
- **test_analytics_summary_counts_approved_hours()** (3 connections) — `api/tests/test_analytics.py`
- **test_analytics_summary_active_volunteer_count()** (2 connections) — `api/tests/test_analytics.py`
- **test_analytics_summary_default_month()** (1 connections) — `api/tests/test_analytics.py`
- **test_analytics_summary_explicit_month()** (1 connections) — `api/tests/test_analytics.py`
- **test_analytics_summary_monthly_trend_has_6_points()** (1 connections) — `api/tests/test_analytics.py`
- **Rejected entries don't contribute to total_hours; pending_manager entries don't** (1 connections) — `api/tests/test_analytics.py`
- **A month with only rejected entries returns total_hours=0, not an error.** (1 connections) — `api/tests/test_analytics.py`

## Relationships

- [[volunteer_factory()]] (4 shared connections)
- [[log_entry_factory()]] (3 shared connections)

## Source Files

- `api/tests/test_analytics.py`

## Audit Trail

- EXTRACTED: 18 (72%)
- INFERRED: 7 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*