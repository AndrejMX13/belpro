# Design: httpOnly Cookie Auth (ISS-005)

**Date:** 2026-05-19  
**Issue:** ISS-005  
**Status:** Approved

---

## Problem

The manager dashboard currently stores the session credential in `sessionStorage` as a base64-encoded Basic Auth string. `sessionStorage` is readable by any JavaScript running on the page — an XSS payload on the local network could steal it trivially. The fix is to move the credential out of JavaScript's reach entirely by using an httpOnly cookie.

---

## Scope

- Manager dashboard auth only.
- n8n, shell scripts (`test_backup_restore.sh`, `switch_manager_phone.sh`), and Docker Compose health checks all use Basic Auth or unauthenticated endpoints — none require changes.
- No TLS in scope for v1; `Secure` cookie flag is configurable, defaulting to `False`.

---

## Architecture

### Dual auth in `require_manager`

The existing `HTTPBasic` security scheme is replaced with two optional extractors:

- A `Cookie` extractor for `belpro_session`
- An optional `HTTPBasic` extractor (`auto_error=False`)

`require_manager` tries the cookie first. If the signature is valid and not expired, the request passes. If no cookie is present, it falls back to Basic Auth using the existing verification logic (DB hash first, env var fallback). If neither succeeds, it raises HTTP 401.

Removing `HTTPBasic` as the primary scheme means FastAPI no longer sends `WWW-Authenticate: Basic` on 401 responses, so browsers won't pop up the native Basic Auth dialog. This is desirable — the dashboard has its own login screen.

### Session token

Signed with **itsdangerous** `URLSafeTimedSerializer` using the existing `API_SECRET_KEY`. No server-side session storage — the signature is self-contained and includes expiry. Token payload: `{"sub": "manager"}`. On password change the old cookies remain valid until they expire (acceptable for a single-manager deployment).

### New settings

| Variable | Default | Purpose |
|----------|---------|---------|
| `SESSION_DURATION_HOURS` | `24` | Cookie max-age and token expiry |
| `COOKIE_SECURE` | `False` | Set `True` when TLS is added |

### New endpoints

**`POST /api/auth/login`**  
Body: `{"password": "..."}`. Verifies password using the same logic as `require_manager`. On success: sets `belpro_session` cookie (`HttpOnly`, `SameSite=Strict`, `Max-Age` from `SESSION_DURATION_HOURS`). Returns `{"ok": true}`. On failure: HTTP 401.

**`POST /api/auth/logout`**  
No body. Clears `belpro_session` cookie (max-age=0). Returns `{"ok": true}`. No auth required.

---

## File Map

| File | Change |
|------|--------|
| `api/core/auth.py` | Replace `HTTPBasic` with dual cookie + optional Basic extractor; update `require_manager` |
| `api/core/settings.py` | Add `session_duration_hours: int = 24`, `cookie_secure: bool = False` |
| `api/routers/auth.py` | New file — `POST /api/auth/login`, `POST /api/auth/logout` |
| `api/schemas/auth.py` | New file — `LoginRequest`, `LoginResponse` |
| `api/main.py` | Register the new auth router |
| `.env.example` | Add `SESSION_DURATION_HOURS`, `COOKIE_SECURE` |
| `.env.example.sl` | Same, Slovenian comments |
| `frontend/js/api.js` | Remove `_creds`, `setPassword`, `loadFromSession`, `clear`, `sessionStorage` usage, `Authorization` header injection; add `auth.login()`, `auth.logout()` |
| `frontend/js/volunteers.js` | Update login form handler to call `API.auth.login()`; update logout to call `API.auth.logout()` |

---

## What does NOT change

- All `require_manager` decorators on existing routes — zero route-level changes
- n8n workflows and their `BelPro API (Basic Auth)` credential
- `test_backup_restore.sh` and `switch_manager_phone.sh` — both use `-u manager:$PASSWORD` curl, which hits the Basic Auth fallback unchanged
- Docker Compose health checks — hit the public `/health` endpoint, no auth involved
- `scripts/n8n_workflows.py` — calls n8n's own API, not BelPro

---

## Behaviour changes visible to the manager

| Before | After |
|--------|-------|
| Credential in `sessionStorage` (JS-readable) | Credential in httpOnly cookie (JS-invisible) |
| Survives page refresh (sessionStorage persists within tab) | Survives page refresh, tab close, and browser restart (for session duration) |
| Lost on tab close | Persists for 24 hours (configurable) |
| Local network access unaffected | Local network access unaffected |

---

## Not in scope

- Token invalidation on password change (acceptable for single-manager deployment)
- `Secure` cookie flag (requires TLS, deferred post-v1)
- CSRF tokens (mitigated by `SameSite=Strict` in single-origin setup)
