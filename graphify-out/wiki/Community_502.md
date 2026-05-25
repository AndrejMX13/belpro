# Community 502

> 7 nodes

## Key Concepts

- **main()** (5 connections) — `ops/scripts/monthly_report_send.py`
- **monthly_report_send.py** (3 connections) — `ops/scripts/monthly_report_send.py`
- **report_error()** (3 connections) — `ops/scripts/monthly_report_send.py`
- **resolve_period()** (3 connections) — `ops/scripts/monthly_report_send.py`
- **POST failure to the API error log.** (1 connections) — `ops/scripts/monthly_report_send.py`
- **Return (year, month) for the given period label.      'current'  → today's year** (1 connections) — `ops/scripts/monthly_report_send.py`
- **Resolve target month and call the send-monthly API endpoint.** (1 connections) — `ops/scripts/monthly_report_send.py`

## Relationships

- [[005_report_prefs.py]] (1 shared connections)

## Source Files

- `ops/scripts/monthly_report_send.py`

## Audit Trail

- EXTRACTED: 16 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*