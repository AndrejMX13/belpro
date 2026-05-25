# NGOInfo

> 6 nodes · cohesion 0.33

## Key Concepts

- **NGOInfo** (7 connections) — `api/services/report_pdf.py`
- **test_ngo_header_html_without_logo()** (4 connections) — `api/tests/test_reports.py`
- **test_ngo_header_html_with_logo()** (4 connections) — `api/tests/test_reports.py`
- **NGO identity shown in every PDF header.** (1 connections) — `api/services/report_pdf.py`
- **ngo_header_html must not include an img tag when logo_path is None.** (1 connections) — `api/tests/test_reports.py`
- **ngo_header_html must include an img tag with data URI src when logo_path is set.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[report_pdf.py]] (3 shared connections)
- [[send_monthly_reports()]] (2 shared connections)
- [[test_reports.py]] (2 shared connections)
- [[render_consent_pdf()]] (1 shared connections)

## Source Files

- `api/services/report_pdf.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 9 (50%)
- INFERRED: 9 (50%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*