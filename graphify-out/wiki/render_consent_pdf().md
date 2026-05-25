# render_consent_pdf()

> 12 nodes · cohesion 0.21

## Key Concepts

- **render_consent_pdf()** (11 connections) — `api/services/consent_pdf.py`
- **consent_pdf.py** (7 connections) — `api/services/consent_pdf.py`
- **download_consent_pdf()** (5 connections) — `api/routers/documents.py`
- **documents.py** (4 connections) — `api/routers/documents.py`
- **test_render_consent_pdf_empty_clauses_treated_as_none()** (3 connections) — `api/tests/test_documents.py`
- **_esc()** (2 connections) — `api/services/consent_pdf.py`
- **_now_str()** (2 connections) — `api/services/consent_pdf.py`
- **Documents router — downloadable compliance documents.** (1 connections) — `api/routers/documents.py`
- **Generate and stream the GDPR Article 13 consent notice PDF.** (1 connections) — `api/routers/documents.py`
- **GDPR Article 13 consent notice PDF generation.** (1 connections) — `api/services/consent_pdf.py`
- **Render the GDPR Article 13 consent notice PDF and return raw bytes.      `manage** (1 connections) — `api/services/consent_pdf.py`
- **render_consent_pdf handles empty string clauses without error.** (1 connections) — `api/tests/test_documents.py`

## Relationships

- [[app_settings.py]] (3 shared connections)
- [[test_documents.py]] (3 shared connections)
- [[report_pdf.py]] (2 shared connections)
- [[logo.py]] (1 shared connections)
- [[NGOInfo]] (1 shared connections)
- [[send_monthly_reports()]] (1 shared connections)

## Source Files

- `api/routers/documents.py`
- `api/services/consent_pdf.py`
- `api/tests/test_documents.py`

## Audit Trail

- EXTRACTED: 30 (77%)
- INFERRED: 9 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*