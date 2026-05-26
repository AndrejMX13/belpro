# POST /api/log-entries/{id}/photos (upload_photo)

> 12 nodes

## Key Concepts

- **auth.py** (7 connections) — `api/routers/auth.py`
- **login()** (7 connections) — `api/routers/auth.py`
- **LoginResponse** (5 connections) — `api/schemas/auth.py`
- **logout()** (4 connections) — `api/routers/auth.py`
- **auth.py** (4 connections) — `api/schemas/auth.py`
- **api/routers/auth.py Login and Logout Endpoints** (4 connections) — `docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md`
- **belpro_session httpOnly Cookie** (2 connections) — `docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md`
- **Auth endpoints — login sets an httpOnly session cookie, logout clears it.** (1 connections) — `api/routers/auth.py`
- **Verify manager password and set an httpOnly session cookie.** (1 connections) — `api/routers/auth.py`
- **Clear the session cookie.** (1 connections) — `api/routers/auth.py`
- **Schemas for the auth endpoints.** (1 connections) — `api/schemas/auth.py`
- **Response for login and logout endpoints.** (1 connections) — `api/schemas/auth.py`

## Relationships

- [[Community 325]] (3 shared connections)
- [[Community 514]] (2 shared connections)
- [[test_app_settings.py]] (2 shared connections)
- [[Code: Preveri Slike Stanje]] (1 shared connections)

## Source Files

- `api/routers/auth.py`
- `api/schemas/auth.py`
- `docs/superpowers/specs/2026-05-19-httponly-cookie-auth-design.md`

## Audit Trail

- EXTRACTED: 27 (71%)
- INFERRED: 11 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*