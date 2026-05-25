# n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)

> 3 nodes · cohesion 1.00

## Key Concepts

- **n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)** (7 connections) — `n8n/workflows/monthly_reports.json`
- **POST /api/reports/send-monthly (send_monthly_reports)** (3 connections) — `api/routers/reports.py`
- **BelPro - Mesecna Porocila (Monthly Reports Workflow)** (2 connections) — `n8n/workflows/monthly_reports.json`

## Relationships

- [[send_monthly_reports()]] (1 shared connections)
- [[send_email()]] (1 shared connections)
- [[EvolutionClient]] (1 shared connections)
- [[report_pdf.py]] (1 shared connections)
- [[persist_report()]] (1 shared connections)
- [[BelPro - Odobritev Upravljalca (Manager Approval Workflow)]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `n8n/workflows/monthly_reports.json`

## Audit Trail

- EXTRACTED: 8 (67%)
- INFERRED: 4 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*