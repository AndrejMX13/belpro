# load_key()

> 68 nodes · cohesion 0.05

## Key Concepts

- **load_key()** (16 connections) — `api/services/encryption.py`
- **test_encryption.py** (14 connections) — `api/tests/test_encryption.py`
- **_to_response()** (12 connections) — `api/routers/volunteers.py`
- **create_volunteer()** (12 connections) — `api/routers/volunteers.py`
- **volunteers.py** (11 connections) — `api/routers/volunteers.py`
- **list_volunteers()** (10 connections) — `api/routers/volunteers.py`
- **_to_detail_response()** (9 connections) — `api/routers/volunteers.py`
- **cmd_rotate()** (9 connections) — `api/scripts/rotate_emso_key.py`
- **check_emso()** (8 connections) — `api/routers/volunteers.py`
- **update_volunteer()** (8 connections) — `api/routers/volunteers.py`
- **encrypt_emso()** (8 connections) — `api/services/encryption.py`
- **hash_emso()** (8 connections) — `api/services/encryption.py`
- **mask_emso()** (8 connections) — `api/services/encryption.py`
- **get_volunteer()** (7 connections) — `api/routers/volunteers.py`
- **decrypt_emso()** (7 connections) — `api/services/encryption.py`
- **emso_checksum_valid()** (7 connections) — `api/utils/emso.py`
- **activate_volunteer()** (6 connections) — `api/routers/volunteers.py`
- **deactivate_volunteer()** (6 connections) — `api/routers/volunteers.py`
- **cmd_backup()** (6 connections) — `api/scripts/rotate_emso_key.py`
- **main()** (6 connections) — `api/scripts/rotate_emso_key.py`
- **encryption.py** (6 connections) — `api/services/encryption.py`
- **rotate_emso_key.py** (5 connections) — `api/scripts/rotate_emso_key.py`
- **cmd_restore()** (5 connections) — `api/scripts/rotate_emso_key.py`
- **_db_url()** (4 connections) — `api/scripts/rotate_emso_key.py`
- **test_emso.py** (4 connections) — `api/tests/test_emso.py`
- *... and 43 more nodes in this community*

## Relationships

- [[Volunteer (ORM)]] (26 shared connections)
- [[str]] (4 shared connections)
- [[volunteer.py]] (3 shared connections)
- [[BaseModel]] (2 shared connections)
- [[GET /api/volunteers/{id} (get_volunteer)]] (2 shared connections)
- [[EmsoCheckResponse (Schema)]] (1 shared connections)
- [[Base]] (1 shared connections)
- [[path]] (1 shared connections)
- [[volunteer_factory()]] (1 shared connections)
- [[n8n/workflows/volunteer_entry.json]] (1 shared connections)
- [[BelPro - Vnos Prostovoljcev (Volunteer Entry Workflow)]] (1 shared connections)

## Source Files

- `api/routers/volunteers.py`
- `api/scripts/rotate_emso_key.py`
- `api/services/encryption.py`
- `api/tests/test_emso.py`
- `api/tests/test_encryption.py`
- `api/utils/emso.py`

## Audit Trail

- EXTRACTED: 176 (65%)
- INFERRED: 95 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*