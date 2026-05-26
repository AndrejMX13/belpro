# Community 514

> 6 nodes

## Key Concepts

- **auth.py** (6 connections) — `api/core/auth.py`
- **_verify_password()** (4 connections) — `api/core/auth.py`
- **require_manager()** (4 connections) — `api/core/auth.py`
- **Manager authentication — httpOnly session cookie with Basic Auth fallback.  Auth** (1 connections) — `api/core/auth.py`
- **Verify password against DB hash or env var fallback.** (1 connections) — `api/core/auth.py`
- **Reject requests without a valid session cookie or Basic Auth credentials.** (1 connections) — `api/core/auth.py`

## Relationships

- [[Code: Preveri Slike Stanje]] (3 shared connections)
- [[POST /api/log-entries/{id}/photos (upload_photo)]] (2 shared connections)

## Source Files

- `api/core/auth.py`

## Audit Trail

- EXTRACTED: 15 (88%)
- INFERRED: 2 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*