# report_pdf.py

> 11 nodes · cohesion 0.33

## Key Concepts

- **report_pdf.py** (10 connections) — `api/services/report_pdf.py`
- **render_volunteer_pdf()** (9 connections) — `api/services/report_pdf.py`
- **ngo_header_html()** (8 connections) — `api/services/report_pdf.py`
- **render_summary_pdf()** (7 connections) — `api/services/report_pdf.py`
- **_esc()** (4 connections) — `api/services/report_pdf.py`
- **_generated_line()** (3 connections) — `api/services/report_pdf.py`
- **_fmt_date()** (2 connections) — `api/services/report_pdf.py`
- **PDF rendering for monthly volunteer reports using WeasyPrint.** (1 connections) — `api/services/report_pdf.py`
- **Render the NGO header block as an HTML string.** (1 connections) — `api/services/report_pdf.py`
- **Render a single-volunteer monthly report PDF and return raw bytes.** (1 connections) — `api/services/report_pdf.py`
- **Render an all-volunteer summary PDF and return raw bytes.** (1 connections) — `api/services/report_pdf.py`

## Relationships

- [[send_monthly_reports()]] (5 shared connections)
- [[NGOInfo]] (3 shared connections)
- [[render_consent_pdf()]] (2 shared connections)
- [[n8n: POST /api/reports/send-monthly (Trigger Monthly Report Delivery)]] (1 shared connections)

## Source Files

- `api/services/report_pdf.py`

## Audit Trail

- EXTRACTED: 39 (83%)
- INFERRED: 8 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*