# Community 3

> 48 nodes · cohesion 0.05

## Key Concepts

- **normalize_phone()** (16 connections) — `api/utils/phone.py`
- **test_managers.py** (13 connections) — `api/tests/test_managers.py`
- **test_phone_utils.py** (10 connections) — `api/tests/test_phone_utils.py`
- **EvolutionClient** (7 connections) — `api/services/evolution.py`
- **seed_whatsapp_phone_from_env()** (6 connections) — `api/main.py`
- **main.py** (5 connections) — `api/main.py`
- **health_detailed()** (4 connections) — `api/main.py`
- **lifespan()** (4 connections) — `api/main.py`
- **.get_connected_phone()** (3 connections) — `api/services/evolution.py`
- **test_seed_whatsapp_phone_does_not_overwrite_existing_value()** (3 connections) — `api/tests/test_managers.py`
- **test_seed_whatsapp_phone_populates_null_db_field()** (3 connections) — `api/tests/test_managers.py`
- **health()** (2 connections) — `api/main.py`
- **.send_document()** (2 connections) — `api/services/evolution.py`
- **test_already_normalized()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_empty_string_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_jid_phone_part()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_none_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_dashes()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_parentheses()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_plus_prefix()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_strips_spaces()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_too_short_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **test_whitespace_only_returns_none()** (2 connections) — `api/tests/test_phone_utils.py`
- **Belpro FastAPI application entry point.** (1 connections) — `api/main.py`
- **Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.** (1 connections) — `api/main.py`
- *... and 23 more nodes in this community*

## Relationships

- [[Community 36]] (2 shared connections)
- [[Community 41]] (2 shared connections)
- [[Community 69]] (2 shared connections)
- [[Community 11]] (1 shared connections)

## Source Files

- `api/main.py`
- `api/services/evolution.py`
- `api/tests/test_managers.py`
- `api/tests/test_phone_utils.py`
- `api/utils/phone.py`

## Audit Trail

- EXTRACTED: 88 (72%)
- INFERRED: 35 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*