# GET /logo

> 17 nodes

## Key Concepts

- **report_pdf.py** (10 connections) — `api/services/report_pdf.py`
- **render_volunteer_pdf()** (9 connections) — `api/services/report_pdf.py`
- **ngo_header_html()** (8 connections) — `api/services/report_pdf.py`
- **NGOInfo** (7 connections) — `api/services/report_pdf.py`
- **render_summary_pdf()** (7 connections) — `api/services/report_pdf.py`
- **_esc()** (4 connections) — `api/services/report_pdf.py`
- **test_ngo_header_html_without_logo()** (4 connections) — `api/tests/test_reports.py`
- **test_ngo_header_html_with_logo()** (4 connections) — `api/tests/test_reports.py`
- **_generated_line()** (3 connections) — `api/services/report_pdf.py`
- **_fmt_date()** (2 connections) — `api/services/report_pdf.py`
- **PDF rendering for monthly volunteer reports using WeasyPrint.** (1 connections) — `api/services/report_pdf.py`
- **NGO identity shown in every PDF header.** (1 connections) — `api/services/report_pdf.py`
- **Render the NGO header block as an HTML string.** (1 connections) — `api/services/report_pdf.py`
- **Render a single-volunteer monthly report PDF and return raw bytes.** (1 connections) — `api/services/report_pdf.py`
- **Render an all-volunteer summary PDF and return raw bytes.** (1 connections) — `api/services/report_pdf.py`
- **ngo_header_html must not include an img tag when logo_path is None.** (1 connections) — `api/tests/test_reports.py`
- **ngo_header_html must include an img tag with data URI src when logo_path is set.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[Community 434]] (4 shared connections)
- [[merge_semantic.py]] (4 shared connections)
- [[Systematic Debugging Reference]] (3 shared connections)
- [[load_key()]] (2 shared connections)

## Source Files

- `api/services/report_pdf.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 48 (74%)
- INFERRED: 17 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*