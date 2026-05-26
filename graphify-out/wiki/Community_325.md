# Community 325

> 10 nodes

## Key Concepts

- **httpOnly Cookie Auth Design ISS-005** (9 connections) — `docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md`
- **Dashboard Login Screen** (2 connections) — `frontend/index.html`
- **POST /api/auth/login (login)** (2 connections) — `api/routers/auth.py`
- **API.auth.login()** (2 connections) — `frontend/js/api.js`
- **API.auth.logout()** (2 connections) — `frontend/js/api.js`
- **POST /auth/login** (2 connections) — `api/routers/auth.py`
- **POST /auth/logout** (2 connections) — `api/routers/auth.py`
- **POST /api/auth/logout (logout)** (1 connections) — `api/routers/auth.py`
- **login form submit handler** (1 connections) — `frontend/js/volunteers.js`
- **logout button handler** (1 connections) — `frontend/js/volunteers.js`

## Relationships

- [[POST /api/log-entries/{id}/photos (upload_photo)]] (3 shared connections)
- [[n8n MCP Workflow Management Guide]] (1 shared connections)
- [[PATCH /api/log-entries/{id} (update_log_entry)]] (1 shared connections)
- [[Volunteer (ORM)]] (1 shared connections)

## Source Files

- `api/routers/auth.py`
- `docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md`
- `frontend/index.html`
- `frontend/js/api.js`
- `frontend/js/volunteers.js`

## Audit Trail

- EXTRACTED: 23 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*