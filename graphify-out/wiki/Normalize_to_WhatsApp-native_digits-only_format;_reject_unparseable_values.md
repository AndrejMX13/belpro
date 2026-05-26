# Normalize to WhatsApp-native digits-only format; reject unparseable values.

> 14 nodes

## Key Concepts

- **VolunteerUpdate** (14 connections) — `api/schemas/volunteer.py`
- **test_volunteer_update_schema.py** (11 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_accepts_first_name()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_accepts_last_name()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_rejects_empty_first_name()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_rejects_empty_last_name()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_accepts_email_string()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_coerces_empty_email_to_none()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_accepts_none_email()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_normalises_phone()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_all_none_produces_empty_dump()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **test_first_name_included_in_dump()** (2 connections) — `api/tests/test_volunteer_update_schema.py`
- **Fields that can be updated on an existing volunteer.** (1 connections) — `api/schemas/volunteer.py`
- **Unit tests for VolunteerUpdate schema — no DB required.** (1 connections) — `api/tests/test_volunteer_update_schema.py`

## Relationships

- [[test_app_settings.py]] (3 shared connections)

## Source Files

- `api/schemas/volunteer.py`
- `api/tests/test_volunteer_update_schema.py`

## Audit Trail

- EXTRACTED: 26 (55%)
- INFERRED: 21 (45%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*