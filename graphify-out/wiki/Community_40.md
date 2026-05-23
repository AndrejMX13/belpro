# Community 40

> 17 nodes · cohesion 0.15

## Key Concepts

- **load_key()** (16 connections) — `api/services/encryption.py`
- **_to_response()** (10 connections) — `api/routers/volunteers.py`
- **create_volunteer()** (7 connections) — `api/routers/volunteers.py`
- **list_volunteers()** (5 connections) — `api/routers/volunteers.py`
- **activate_volunteer()** (4 connections) — `api/routers/volunteers.py`
- **deactivate_volunteer()** (4 connections) — `api/routers/volunteers.py`
- **update_volunteer()** (4 connections) — `api/routers/volunteers.py`
- **test_load_key_accepts_key_without_padding()** (2 connections) — `api/tests/test_encryption.py`
- **test_load_key_accepts_valid_32_byte_key()** (2 connections) — `api/tests/test_encryption.py`
- **test_load_key_rejects_short_key()** (2 connections) — `api/tests/test_encryption.py`
- **List volunteers with optional filters, sorting, and pagination.** (1 connections) — `api/routers/volunteers.py`
- **Register a new volunteer.  Encrypts EMŠO before storing.** (1 connections) — `api/routers/volunteers.py`
- **Re-activate a previously deactivated volunteer.** (1 connections) — `api/routers/volunteers.py`
- **Soft-delete a volunteer by setting active=False.** (1 connections) — `api/routers/volunteers.py`
- **Update mutable fields on a volunteer (report channel preferences).** (1 connections) — `api/routers/volunteers.py`
- **Decrypt EMŠO, mask it, and build a VolunteerResponse from an ORM object.** (1 connections) — `api/routers/volunteers.py`
- **Decode and validate a base64-encoded 32-byte AES-256 key.      Raises ValueError** (1 connections) — `api/services/encryption.py`

## Relationships

- [[Community 30]] (9 shared connections)
- [[Community 33]] (8 shared connections)
- [[Community 29]] (2 shared connections)
- [[Community 7]] (2 shared connections)
- [[Community 11]] (1 shared connections)
- [[Community 25]] (1 shared connections)

## Source Files

- `api/routers/volunteers.py`
- `api/services/encryption.py`
- `api/tests/test_encryption.py`

## Audit Trail

- EXTRACTED: 33 (52%)
- INFERRED: 30 (48%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*