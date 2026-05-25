# merge_semantic.py

> 13 nodes

## Key Concepts

- **send_monthly_reports()** (15 connections) — `api/routers/reports.py`
- **EvolutionClient** (7 connections) — `api/services/evolution.py`
- **n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)** (7 connections) — `n8n/workflows/monthly_reports.json`
- **.send_document()** (4 connections) — `api/services/evolution.py`
- **.get_connected_phone()** (3 connections) — `api/services/evolution.py`
- **POST /api/reports/send-monthly (send_monthly_reports)** (3 connections) — `api/routers/reports.py`
- **evolution.py** (2 connections) — `api/services/evolution.py`
- **BelPro - Mesecna Porocila (Monthly Reports Workflow)** (2 connections) — `n8n/workflows/monthly_reports.json`
- **Generate monthly PDFs and deliver them via email and/or WhatsApp.      Default** (1 connections) — `api/routers/reports.py`
- **.__init__()** (1 connections) — `api/services/evolution.py`
- **Async HTTP client for the Evolution API WhatsApp gateway.** (1 connections) — `api/services/evolution.py`
- **Return (normalized_phone, state) for the configured instance.          States: "** (1 connections) — `api/services/evolution.py`
- **Send a PDF document to a WhatsApp number via Evolution API sendMedia.** (1 connections) — `api/services/evolution.py`

## Relationships

- [[GET /logo]] (4 shared connections)
- [[Community 434]] (3 shared connections)
- [[Community 543]] (2 shared connections)
- [[Reject tax numbers that fail the Modulus 11 check digit.]] (2 shared connections)
- [[test_auth.py]] (2 shared connections)
- [[volunteers.js]] (1 shared connections)
- [[BelPro System Specification]] (1 shared connections)
- [[006_whatsapp_and_smtp_config.py]] (1 shared connections)
- [[HTTP: Fetch Media]] (1 shared connections)
- [[scripts/gen_diagrams_sl.py]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/services/evolution.py`
- `n8n/workflows/monthly_reports.json`

## Audit Trail

- EXTRACTED: 30 (62%)
- INFERRED: 18 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*