# list_pending_entries.py

> 19 nodes

## Key Concepts

- **report_pdf.py** (10 connections) — `api/services/report_pdf.py`
- **render_volunteer_pdf()** (9 connections) — `api/services/report_pdf.py`
- **ngo_header_html()** (8 connections) — `api/services/report_pdf.py`
- **generate_monthly_pdf()** (7 connections) — `api/routers/reports.py`
- **NGOInfo** (7 connections) — `api/services/report_pdf.py`
- **render_summary_pdf()** (7 connections) — `api/services/report_pdf.py`
- **_esc()** (4 connections) — `api/services/report_pdf.py`
- **test_ngo_header_html_without_logo()** (4 connections) — `api/tests/test_reports.py`
- **test_ngo_header_html_with_logo()** (4 connections) — `api/tests/test_reports.py`
- **_generated_line()** (3 connections) — `api/services/report_pdf.py`
- **_fmt_date()** (2 connections) — `api/services/report_pdf.py`
- **Generate a monthly PDF report for one volunteer or all active volunteers.** (1 connections) — `api/routers/reports.py`
- **PDF rendering for monthly volunteer reports using WeasyPrint.** (1 connections) — `api/services/report_pdf.py`
- **NGO identity shown in every PDF header.** (1 connections) — `api/services/report_pdf.py`
- **Render the NGO header block as an HTML string.** (1 connections) — `api/services/report_pdf.py`
- **Render a single-volunteer monthly report PDF and return raw bytes.** (1 connections) — `api/services/report_pdf.py`
- **Render an all-volunteer summary PDF and return raw bytes.** (1 connections) — `api/services/report_pdf.py`
- **ngo_header_html must not include an img tag when logo_path is None.** (1 connections) — `api/tests/test_reports.py`
- **ngo_header_html must include an img tag with data URI src when logo_path is set.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[GET /log-entries/{id}/photos/{pid}/file]] (6 shared connections)
- [[main()]] (3 shared connections)
- [[005_report_prefs.py]] (2 shared connections)
- [[loadReports()]] (1 shared connections)
- [[LoginRequest (Schema)]] (1 shared connections)

## Source Files

- `api/routers/reports.py`
- `api/services/report_pdf.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 52 (71%)
- INFERRED: 21 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*