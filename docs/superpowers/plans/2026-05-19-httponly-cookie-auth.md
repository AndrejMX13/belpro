# httpOnly Cookie Auth (ISS-005) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `sessionStorage`-based credential storage with an httpOnly session cookie so the manager's password is invisible to JavaScript and cannot be stolen by XSS.

**Architecture:** Dual auth in `require_manager` — cookie path for the browser dashboard, Basic Auth fallback for n8n and scripts. New `POST /api/auth/login` and `POST /api/auth/logout` endpoints. Session token signed with `itsdangerous` using the existing `API_SECRET_KEY`. Frontend drops `sessionStorage` and all `Authorization` header injection; calls login/logout endpoints instead.

**Tech Stack:** FastAPI, itsdangerous (already a transitive Starlette dependency), httpx AsyncClient (tests), vanilla JS

---

## File Map

| File | Change |
|------|--------|
| `api/core/settings.py` | Add `session_duration_hours: int = 24`, `cookie_secure: bool = False` |
| `api/schemas/auth.py` | New — `LoginRequest`, `LoginResponse` |
| `api/core/auth.py` | Extract `_verify_password`; add `_make_session_token`, `_verify_session_token`; replace `HTTPBasic` with dual cookie + optional Basic extractor |
| `api/routers/auth.py` | New — `POST /api/auth/login`, `POST /api/auth/logout` |
| `api/main.py` | Register auth router |
| `api/tests/test_auth.py` | New — all auth tests |
| `.env.example` | Add `SESSION_DURATION_HOURS`, `COOKIE_SECURE` |
| `.env.example.sl` | Same, Slovenian comments |
| `frontend/js/api.js` | Remove `_creds`, `setPassword`, `loadFromSession`, `clear`, `sessionStorage`, `Authorization` injection; add `auth.login()`, `auth.logout()` |
| `frontend/js/volunteers.js` | Update login form handler and logout to use `API.auth` |

---

## Task 1: Settings fields, schemas, and env examples

**Files:**
- Modify: `api/core/settings.py`
- Create: `api/schemas/auth.py`
- Modify: `.env.example`
- Modify: `.env.example.sl`

No TDD needed — these are pure data definitions with no logic to test.

- [ ] **Step 1: Add session settings to `api/core/settings.py`**

Add two fields at the end of the `Settings` class, after `max_photos_per_entry`:

```python
    # ── Session ───────────────────────────────────────────────────────────────
    session_duration_hours: int = 24
    cookie_secure: bool = False
```

- [ ] **Step 2: Create `api/schemas/auth.py`**

```python
"""Schemas for the auth endpoints."""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Body for POST /api/auth/login."""

    password: str


class LoginResponse(BaseModel):
    """Response for login and logout endpoints."""

    ok: bool
```

- [ ] **Step 3: Add new vars to `.env.example`**

Find the existing `API_SECRET_KEY` block (around line 40) and add two lines after `MANAGER_PASSWORD=...`:

```
# SESSION_DURATION_HOURS: how long a dashboard login session lasts (hours).
SESSION_DURATION_HOURS=24

# COOKIE_SECURE: set True when serving over HTTPS (not needed for LAN-only HTTP).
COOKIE_SECURE=False
```

- [ ] **Step 4: Add new vars to `.env.example.sl`**

Same addition in `.env.example.sl`, Slovenian comments:

```
# SESSION_DURATION_HOURS: kako dolgo traja seja upravljalca (v urah).
SESSION_DURATION_HOURS=24

# COOKIE_SECURE: nastavi na True, ko strežnik deluje prek HTTPS.
COOKIE_SECURE=False
```

- [ ] **Step 5: Commit**

```bash
git add api/core/settings.py api/schemas/auth.py .env.example .env.example.sl
git commit -m "feat(auth): add session settings and auth schemas"
```

---

## Task 2: Session token helpers

**Files:**
- Modify: `api/core/auth.py`
- Create: `api/tests/test_auth.py`

- [ ] **Step 1: Write failing tests for token helpers**

Create `api/tests/test_auth.py`:

```python
"""Tests for auth helpers and endpoints."""
import pytest

from core.auth import _make_session_token, _verify_session_token

_SECRET = "test-secret-key-32-bytes-padding!"


def test_make_and_verify_session_token() -> None:
    token = _make_session_token(_SECRET)
    assert isinstance(token, str)
    assert len(token) > 10
    assert _verify_session_token(token, _SECRET, duration_hours=24) is True


def test_verify_session_token_wrong_secret() -> None:
    token = _make_session_token(_SECRET)
    assert _verify_session_token(token, "wrong-secret", duration_hours=24) is False


def test_verify_session_token_garbage() -> None:
    assert _verify_session_token("notavalidtoken", _SECRET, duration_hours=24) is False


def test_verify_session_token_empty() -> None:
    assert _verify_session_token("", _SECRET, duration_hours=24) is False
```

- [ ] **Step 2: Run tests to confirm they fail**

```
docker compose exec api pytest tests/test_auth.py -v
```

Expected: `ImportError` — `_make_session_token` does not exist yet.

- [ ] **Step 3: Replace `api/core/auth.py` with the new version**

```python
"""Manager authentication — httpOnly session cookie with Basic Auth fallback.

Auth priority on every protected request:
  1. belpro_session httpOnly cookie (signed with API_SECRET_KEY)
  2. HTTP Basic Auth (Authorization header) — used by n8n and scripts

Password verification priority:
  1. manager.password_hash in DB (set via the settings UI)
  2. MANAGER_PASSWORD env var (initial / fallback)
"""
from __future__ import annotations

import secrets
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, get_settings
from db.session import get_db
from services.password import verify_password

_security = HTTPBasic(auto_error=False)


def _make_session_token(secret_key: str) -> str:
    """Create a signed, self-expiring session token."""
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps({"sub": "manager"})


def _verify_session_token(token: str, secret_key: str, duration_hours: int) -> bool:
    """Return True if the token signature is valid and not expired."""
    if not token:
        return False
    s = URLSafeTimedSerializer(secret_key)
    try:
        s.loads(token, max_age=duration_hours * 3600)
        return True
    except (BadSignature, SignatureExpired):
        return False


async def _verify_password(
    password: str,
    settings: Settings,
    db: AsyncSession,
) -> bool:
    """Verify password against DB hash or env var fallback."""
    from models.manager import Manager  # local import avoids circular dependency

    manager = (await db.execute(select(Manager).limit(1))).scalar_one_or_none()

    if manager and manager.password_hash:
        return verify_password(password, manager.password_hash)
    return secrets.compare_digest(
        password.encode("utf-8"),
        settings.manager_password.encode("utf-8"),
    )


async def require_manager(
    request: Request,
    credentials: Annotated[Optional[HTTPBasicCredentials], Depends(_security)],
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Reject requests without a valid session cookie or Basic Auth credentials."""
    # 1. Cookie path (browser dashboard)
    session_cookie = request.cookies.get("belpro_session")
    if session_cookie and _verify_session_token(
        session_cookie, settings.api_secret_key, settings.session_duration_hours
    ):
        return

    # 2. Basic Auth fallback (n8n, scripts)
    if credentials and await _verify_password(credentials.password, settings, db):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nepravilni podatki za prijavo.",
    )
```

- [ ] **Step 4: Run token helper tests**

```
docker compose exec api pytest tests/test_auth.py::test_make_and_verify_session_token tests/test_auth.py::test_verify_session_token_wrong_secret tests/test_auth.py::test_verify_session_token_garbage tests/test_auth.py::test_verify_session_token_empty -v
```

Expected: all 4 PASS.

- [ ] **Step 5: Run full test suite to catch regressions**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS. The `auth` fixture still passes `Authorization: Basic ...` headers which hit the Basic Auth fallback branch — no regressions.

- [ ] **Step 6: Commit**

```bash
git add api/core/auth.py api/tests/test_auth.py
git commit -m "feat(auth): add session token helpers and dual-auth require_manager"
```

---

## Task 3: Login and logout endpoints

**Files:**
- Create: `api/routers/auth.py`
- Modify: `api/main.py`
- Modify: `api/tests/test_auth.py`

- [ ] **Step 1: Write failing tests for login/logout**

Append to `api/tests/test_auth.py`:

```python
import base64

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success_sets_cookie(client: AsyncClient) -> None:
    r = await client.post("/api/auth/login", json={"password": "testpass123"})
    assert r.status_code == 200
    assert r.json() == {"ok": True}
    assert "belpro_session" in r.cookies


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(client: AsyncClient) -> None:
    r = await client.post("/api/auth/login", json={"password": "wrongpassword"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_logout_clears_cookie(client: AsyncClient) -> None:
    await client.post("/api/auth/login", json={"password": "testpass123"})
    r = await client.post("/api/auth/logout")
    assert r.status_code == 200
    assert r.json() == {"ok": True}


@pytest.mark.asyncio
async def test_cookie_auth_grants_access_to_protected_route(client: AsyncClient) -> None:
    await client.post("/api/auth/login", json={"password": "testpass123"})
    # httpx stores the cookie and sends it automatically on the next request
    r = await client.get("/api/managers/me")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_no_auth_returns_401(client: AsyncClient) -> None:
    r = await client.get("/api/managers/me")
    assert r.status_code == 401
    # Must NOT trigger the browser's native Basic Auth dialog
    assert "WWW-Authenticate" not in r.headers
```

- [ ] **Step 2: Run tests to confirm they fail**

```
docker compose exec api pytest tests/test_auth.py::test_login_success_sets_cookie tests/test_auth.py::test_login_wrong_password_returns_401 tests/test_auth.py::test_logout_clears_cookie tests/test_auth.py::test_cookie_auth_grants_access_to_protected_route tests/test_auth.py::test_no_auth_returns_401 -v
```

Expected: all FAIL — `/api/auth/login` does not exist yet.

- [ ] **Step 3: Create `api/routers/auth.py`**

```python
"""Auth endpoints — login sets an httpOnly session cookie, logout clears it."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import _make_session_token, _verify_password
from core.settings import Settings, get_settings
from db.session import get_db
from schemas.auth import LoginRequest, LoginResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    response: Response,
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Verify manager password and set an httpOnly session cookie."""
    if not await _verify_password(body.password, settings, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Napačno geslo.",
        )
    token = _make_session_token(settings.api_secret_key)
    response.set_cookie(
        key="belpro_session",
        value=token,
        httponly=True,
        samesite="strict",
        secure=settings.cookie_secure,
        max_age=settings.session_duration_hours * 3600,
    )
    return LoginResponse(ok=True)


@router.post("/auth/logout", response_model=LoginResponse)
async def logout(response: Response) -> LoginResponse:
    """Clear the session cookie."""
    response.delete_cookie(key="belpro_session", samesite="strict")
    return LoginResponse(ok=True)
```

- [ ] **Step 4: Register the auth router in `api/main.py`**

Add the import alongside the existing router imports:

```python
from routers.auth import router as auth_router
```

Add the `include_router` call alongside the existing ones:

```python
app.include_router(auth_router, prefix="/api")
```

- [ ] **Step 5: Run the new tests**

```
docker compose exec api pytest tests/test_auth.py::test_login_success_sets_cookie tests/test_auth.py::test_login_wrong_password_returns_401 tests/test_auth.py::test_logout_clears_cookie tests/test_auth.py::test_cookie_auth_grants_access_to_protected_route tests/test_auth.py::test_no_auth_returns_401 -v
```

Expected: all 5 PASS.

- [ ] **Step 6: Run full test suite**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 7: Commit**

```bash
git add api/routers/auth.py api/main.py api/tests/test_auth.py
git commit -m "feat(auth): add login and logout endpoints with httpOnly cookie"
```

---

## Task 4: Frontend — `api.js`

**Files:**
- Modify: `frontend/js/api.js`

No automated tests — verify manually in Task 6.

- [ ] **Step 1: Read the current top of `api.js` to understand the full scope of changes**

The first ~35 lines contain `_creds`, `setPassword`, `loadFromSession`, `clear`, and `_authHeaders`. All of these are replaced. The `Authorization` header is also injected in two places inside the photo upload methods (around lines 132 and 156).

- [ ] **Step 2: Replace the credential management block**

The current block (lines 1–34, everything before `_handleUnauthorized`) is:

```js
'use strict';

const API = (() => {
  const BASE = '/api';
  let _creds = null;

  function setPassword(password) {
    _creds = btoa('manager:' + password);
    sessionStorage.setItem('bpCreds', _creds);
  }

  function loadFromSession() {
    _creds = sessionStorage.getItem('bpCreds');
    return _creds !== null;
  }

  function clear() {
    _creds = null;
    sessionStorage.removeItem('bpCreds');
  }

  function _authHeaders(extra = {}) {
    const headers = { ...extra };
    if (_creds) headers['Authorization'] = 'Basic ' + _creds;
    return headers;
  }
```

Replace with:

```js
'use strict';

const API = (() => {
  const BASE = '/api';

  function _authHeaders(extra = {}) {
    return { ...extra };
  }
```

- [ ] **Step 3: Remove `Authorization` header injection from photo upload methods**

Search for the two lines that manually set `headers['Authorization']` inside the photo upload and `uploadPhoto` methods (currently around lines 132 and 156 after the edit above). Delete those lines — the cookie is sent automatically by the browser.

- [ ] **Step 4: Add `auth` object to the returned API surface**

Find the `return {` block at the bottom of the IIFE and add `auth` as the first entry:

```js
  return {
    auth: {
      login:  (password) => request('/auth/login',  { method: 'POST', body: JSON.stringify({ password }) }),
      logout: ()         => request('/auth/logout', { method: 'POST' }),
    },
    // ... existing entries unchanged ...
```

- [ ] **Step 5: Remove `setPassword`, `loadFromSession`, and `clear` from the returned surface** (if they were previously exported). Search the `return {` block for these three names and delete their entries.

- [ ] **Step 6: Commit**

```bash
git add frontend/js/api.js
git commit -m "feat(auth): replace sessionStorage credential with httpOnly cookie in api.js"
```

---

## Task 5: Frontend — `volunteers.js`

**Files:**
- Modify: `frontend/js/volunteers.js`

- [ ] **Step 1: Update the login form submit handler**

Find the `$('login-form').addEventListener('submit', ...)` block (currently around line 50). The current handler:

```js
$('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  API.setPassword($('login-password').value);
  // makes a test request to verify credentials, shows error on 401
  ...
```

Replace with:

```js
$('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  $('login-error').hidden = true;
  try {
    await API.auth.login($('login-password').value);
    hideLogin();
    initApp();
  } catch {
    $('login-error').hidden = false;
  }
});
```

Note: `API.auth.login()` calls the login endpoint directly — the endpoint IS the verification. A 401 throws, a 200 means the cookie is set and the session is live.

- [ ] **Step 2: Update the startup / session restore logic**

Find the app initialisation code that calls `loadFromSession()` (near the bottom of the file or in a `DOMContentLoaded` handler). The current pattern is:

```js
if (API.loadFromSession()) {
  initApp();
} else {
  showLogin();
}
```

Replace with:

```js
initApp();
```

Rationale: with a persistent httpOnly cookie the browser sends it automatically on the first request. `initApp()` will call a protected endpoint; if the cookie is absent or expired the API returns 401, the `belpro:unauthorized` event fires, and `showLogin()` is called — the same error path that already exists.

- [ ] **Step 3: Update the logout handler**

Find any logout button click handler. The current handler calls `API.clear()` or similar. Replace with:

```js
await API.auth.logout();
showLogin();
```

- [ ] **Step 4: Remove any remaining references to `API.setPassword`, `API.loadFromSession`, or `API.clear`**

Search `volunteers.js` for these three names and delete any remaining calls.

- [ ] **Step 5: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat(auth): update dashboard login/logout to use httpOnly cookie session"
```

---

## Task 6: Manual browser test

No code changes — verify the full flow works end to end.

- [ ] **Step 1: Rebuild the API container**

```
docker compose up -d --build api
```

- [ ] **Step 2: Open the dashboard at `http://localhost` and verify the login screen appears**

- [ ] **Step 3: Log in with the manager password**

Confirm: login screen disappears, dashboard loads normally. Open DevTools → Application → Cookies — confirm `belpro_session` cookie is present with `HttpOnly` flag, no value visible. Confirm `sessionStorage` has no `bpCreds` entry.

- [ ] **Step 4: Refresh the page**

Confirm: dashboard loads immediately, no login screen. The cookie is sent automatically.

- [ ] **Step 5: Open a new tab to `http://localhost`**

Confirm: dashboard loads without login (cookie is shared across tabs).

- [ ] **Step 6: Log out**

Confirm: login screen reappears. Cookie is cleared. Refresh — login screen persists (no valid cookie).

- [ ] **Step 7: Log in again, then wait for session expiry (or manually delete the cookie in DevTools)**

Delete the `belpro_session` cookie in DevTools. Refresh or make any API call — confirm the login screen reappears.

- [ ] **Step 8: Verify n8n workflows are unaffected**

Trigger a test entry via WhatsApp or run the n8n workflow manually. Confirm it still completes without auth errors.
