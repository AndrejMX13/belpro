# Community 86

> 5 nodes · cohesion 0.40

## Key Concepts

- **NGOInfo** (6 connections) — `api/services/report_pdf.py`
- **test_ngo_header_html_with_logo()** (5 connections) — `api/tests/test_reports.py`
- **NGO identity shown in every PDF header.** (1 connections) — `api/services/report_pdf.py`
- **ngo_header_html must not include an img tag when logo_path is None.** (1 connections) — `api/tests/test_reports.py`
- **ngo_header_html must include an img tag with data URI src when logo_path is set.** (1 connections) — `api/tests/test_reports.py`

## Relationships

- [[Community 54]] (2 shared connections)
- [[Community 68]] (1 shared connections)
- [[Community 69]] (1 shared connections)
- [[Community 53]] (1 shared connections)
- [[Community 32]] (1 shared connections)

## Source Files

- `api/services/report_pdf.py`
- `api/tests/test_reports.py`

## Audit Trail

- EXTRACTED: 8 (57%)
- INFERRED: 6 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*