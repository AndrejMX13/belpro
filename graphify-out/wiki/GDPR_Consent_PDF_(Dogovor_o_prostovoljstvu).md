# GDPR Consent PDF (Dogovor o prostovoljstvu)

> 22 nodes

## Key Concepts

- **render_consent_pdf()** (11 connections) — `api/services/consent_pdf.py`
- **test_documents.py** (8 connections) — `api/tests/test_documents.py`
- **consent_pdf.py** (7 connections) — `api/services/consent_pdf.py`
- **test_render_consent_pdf_returns_bytes()** (3 connections) — `api/tests/test_documents.py`
- **test_render_consent_pdf_with_additional_clauses()** (3 connections) — `api/tests/test_documents.py`
- **test_render_consent_pdf_empty_clauses_treated_as_none()** (3 connections) — `api/tests/test_documents.py`
- **_esc()** (2 connections) — `api/services/consent_pdf.py`
- **_now_str()** (2 connections) — `api/services/consent_pdf.py`
- **test_consent_pdf_returns_pdf()** (2 connections) — `api/tests/test_documents.py`
- **test_consent_pdf_requires_auth()** (2 connections) — `api/tests/test_documents.py`
- **test_patch_manager_saves_gdpr_clauses()** (2 connections) — `api/tests/test_documents.py`
- **test_patch_manager_clears_gdpr_clauses()** (2 connections) — `api/tests/test_documents.py`
- **GDPR Article 13 consent notice PDF generation.** (1 connections) — `api/services/consent_pdf.py`
- **Render the GDPR Article 13 consent notice PDF and return raw bytes.      `manage** (1 connections) — `api/services/consent_pdf.py`
- **Tests for the /documents router and consent_pdf service.** (1 connections) — `api/tests/test_documents.py`
- **render_consent_pdf returns non-empty bytes for a minimal manager.** (1 connections) — `api/tests/test_documents.py`
- **render_consent_pdf produces bytes when additional clauses are set.** (1 connections) — `api/tests/test_documents.py`
- **render_consent_pdf handles empty string clauses without error.** (1 connections) — `api/tests/test_documents.py`
- **Authenticated request returns a PDF response.** (1 connections) — `api/tests/test_documents.py`
- **Unauthenticated request is rejected.** (1 connections) — `api/tests/test_documents.py`
- **PATCH /managers/me accepts and persists gdpr_additional_clauses.** (1 connections) — `api/tests/test_documents.py`
- **PATCH /managers/me with empty string clears gdpr_additional_clauses.      Note:** (1 connections) — `api/tests/test_documents.py`

## Relationships

- [[Code: Build Image Media Body]] (3 shared connections)
- [[n8n MCP Workflow Management Guide]] (2 shared connections)
- [[009_rename_entry_date_to_work_date.py]] (2 shared connections)

## Source Files

- `api/services/consent_pdf.py`
- `api/tests/test_documents.py`

## Audit Trail

- EXTRACTED: 47 (82%)
- INFERRED: 10 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*