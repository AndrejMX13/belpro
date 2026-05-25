# test_auth.py

> 34 nodes · cohesion 0.08

## Key Concepts

- **test_auth.py** (11 connections) — `api/tests/test_auth.py`
- **_verify_session_token()** (8 connections) — `api/core/auth.py`
- **auth.py** (7 connections) — `api/routers/auth.py`
- **login()** (7 connections) — `api/routers/auth.py`
- **auth.py** (6 connections) — `api/core/auth.py`
- **_make_session_token()** (6 connections) — `api/core/auth.py`
- **LoginResponse** (5 connections) — `api/schemas/auth.py`
- **_verify_password()** (4 connections) — `api/core/auth.py`
- **require_manager()** (4 connections) — `api/core/auth.py`
- **logout()** (4 connections) — `api/routers/auth.py`
- **auth.py** (4 connections) — `api/schemas/auth.py`
- **LoginRequest** (3 connections) — `api/schemas/auth.py`
- **test_make_and_verify_session_token()** (3 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_wrong_secret()** (3 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_expired()** (3 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_garbage()** (2 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_empty()** (2 connections) — `api/tests/test_auth.py`
- **Manager authentication — httpOnly session cookie with Basic Auth fallback.  Auth** (1 connections) — `api/core/auth.py`
- **Create a signed, self-expiring session token.** (1 connections) — `api/core/auth.py`
- **Return True if the token signature is valid and not expired.** (1 connections) — `api/core/auth.py`
- **Verify password against DB hash or env var fallback.** (1 connections) — `api/core/auth.py`
- **Reject requests without a valid session cookie or Basic Auth credentials.** (1 connections) — `api/core/auth.py`
- **Auth endpoints — login sets an httpOnly session cookie, logout clears it.** (1 connections) — `api/routers/auth.py`
- **Verify manager password and set an httpOnly session cookie.** (1 connections) — `api/routers/auth.py`
- **Clear the session cookie.** (1 connections) — `api/routers/auth.py`
- *... and 9 more nodes in this community*

## Relationships

- [[Settings Table ISS-026 Design]] (5 shared connections)
- [[BaseModel]] (2 shared connections)

## Source Files

- `api/core/auth.py`
- `api/routers/auth.py`
- `api/schemas/auth.py`
- `api/tests/test_auth.py`

## Audit Trail

- EXTRACTED: 70 (71%)
- INFERRED: 29 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*