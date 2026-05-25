# renderSettings() — settings page

> 15 nodes · cohesion 0.17

## Key Concepts

- **renderSettings() — settings page** (6 connections) — `frontend/js/volunteers.js`
- **API.managers.me()** (4 connections) — `frontend/js/api.js`
- **renderDocuments() — documents page** (4 connections) — `frontend/js/documents.js`
- **GET /managers/me** (4 connections) — `api/routers/managers.py`
- **API.managers.update()** (3 connections) — `frontend/js/api.js`
- **PATCH /managers/me** (3 connections) — `api/routers/managers.py`
- **GET /managers/me/config-info** (3 connections) — `api/routers/managers.py`
- **ManagerResponse shape (first_name, last_name, email, phone, ngo_name, ngo_street, ngo_postal_code, ngo_city, ngo_davcna, ngo_whatsapp_phone, report_email, report_whatsapp, default_report_email, default_report_whatsapp, gdpr_additional_clauses)** (3 connections) — `api/routers/managers.py`
- **API.managers.changePassword()** (2 connections) — `frontend/js/api.js`
- **API.managers.configInfo()** (2 connections) — `frontend/js/api.js`
- **API.documents.consentPdf()** (2 connections) — `frontend/js/api.js`
- **POST /managers/me/change-password** (2 connections) — `api/routers/managers.py`
- **GET /documents/consent-pdf** (2 connections) — `api/routers/documents.py`
- **ConfigInfoResponse shape (smtp_host, smtp_port, smtp_user, smtp_configured, evolution_api_admin_url, wa_phone, wa_state, wa_synced)** (2 connections) — `api/routers/managers.py`
- **checkManagerSetup()** (1 connections) — `frontend/js/volunteers.js`

## Relationships

- [[volunteers.js]] (7 shared connections)

## Source Files

- `api/routers/documents.py`
- `api/routers/managers.py`
- `frontend/js/api.js`
- `frontend/js/documents.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 43 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*