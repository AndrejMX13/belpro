# Code: Preveri Slike Stanje

> 16 nodes

## Key Concepts

- **test_auth.py** (11 connections) — `api/tests/test_auth.py`
- **_verify_session_token()** (8 connections) — `api/core/auth.py`
- **_make_session_token()** (6 connections) — `api/core/auth.py`
- **test_make_and_verify_session_token()** (3 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_wrong_secret()** (3 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_expired()** (3 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_garbage()** (2 connections) — `api/tests/test_auth.py`
- **test_verify_session_token_empty()** (2 connections) — `api/tests/test_auth.py`
- **Create a signed, self-expiring session token.** (1 connections) — `api/core/auth.py`
- **Return True if the token signature is valid and not expired.** (1 connections) — `api/core/auth.py`
- **test_login_success_sets_cookie()** (1 connections) — `api/tests/test_auth.py`
- **test_login_wrong_password_returns_401()** (1 connections) — `api/tests/test_auth.py`
- **test_logout_clears_cookie()** (1 connections) — `api/tests/test_auth.py`
- **test_cookie_auth_grants_access_to_protected_route()** (1 connections) — `api/tests/test_auth.py`
- **test_no_auth_returns_401_without_www_authenticate()** (1 connections) — `api/tests/test_auth.py`
- **Tests for auth helpers and endpoints.** (1 connections) — `api/tests/test_auth.py`

## Relationships

- [[Community 511]] (3 shared connections)
- [[GET /api/log-entries/{id}/photos/{photo_id}/file (get_photo_file)]] (1 shared connections)

## Source Files

- `api/core/auth.py`
- `api/tests/test_auth.py`

## Audit Trail

- EXTRACTED: 29 (63%)
- INFERRED: 17 (37%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*