# Community 53

> 12 nodes · cohesion 0.20

## Key Concepts

- **render_consent_pdf()** (11 connections) — `api/services/consent_pdf.py`
- **consent_pdf.py** (4 connections) — `api/services/consent_pdf.py`
- **download_consent_pdf()** (3 connections) — `api/routers/documents.py`
- **test_render_consent_pdf_with_additional_clauses()** (3 connections) — `api/tests/test_documents.py`
- **documents.py** (2 connections) — `api/routers/documents.py`
- **_esc()** (2 connections) — `api/services/consent_pdf.py`
- **_now_str()** (2 connections) — `api/services/consent_pdf.py`
- **Documents router — downloadable compliance documents.** (1 connections) — `api/routers/documents.py`
- **Generate and stream the GDPR Article 13 consent notice PDF.** (1 connections) — `api/routers/documents.py`
- **GDPR Article 13 consent notice PDF generation.** (1 connections) — `api/services/consent_pdf.py`
- **Render the GDPR Article 13 consent notice PDF and return raw bytes.      `manage** (1 connections) — `api/services/consent_pdf.py`
- **render_consent_pdf produces bytes when additional clauses are set.** (1 connections) — `api/tests/test_documents.py`

## Relationships

- [[Community 47]] (3 shared connections)
- [[Community 86]] (1 shared connections)
- [[Community 69]] (1 shared connections)
- [[Community 54]] (1 shared connections)

## Source Files

- `api/routers/documents.py`
- `api/services/consent_pdf.py`
- `api/tests/test_documents.py`

## Audit Trail

- EXTRACTED: 23 (72%)
- INFERRED: 9 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*