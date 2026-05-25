# api/main.py

> 14 nodes · cohesion 0.15

## Key Concepts

- **api/main.py** (22 connections) — `api/main.py`
- **seed_whatsapp_phone_from_env()** (6 connections) — `api/main.py`
- **lifespan()** (4 connections) — `api/main.py`
- **health_detailed()** (4 connections) — `api/main.py`
- **test_seed_whatsapp_phone_populates_null_db_field()** (3 connections) — `api/tests/test_managers.py`
- **test_seed_whatsapp_phone_does_not_overwrite_existing_value()** (3 connections) — `api/tests/test_managers.py`
- **health()** (2 connections) — `api/main.py`
- **Belpro FastAPI application entry point.** (1 connections) — `api/main.py`
- **Seed ngo_whatsapp_phone from .env into DB on first boot, if DB value is null.** (1 connections) — `api/main.py`
- **Fail fast if DB unreachable; seed WhatsApp phone from .env if DB null.** (1 connections) — `api/main.py`
- **Health check — returns ok when the service is up.** (1 connections) — `api/main.py`
- **Per-service health status for the manager dashboard widget.** (1 connections) — `api/main.py`
- **seed_whatsapp_phone_from_env writes normalized phone to DB when DB value is null** (1 connections) — `api/tests/test_managers.py`
- **seed_whatsapp_phone_from_env leaves existing DB value untouched.** (1 connections) — `api/tests/test_managers.py`

## Relationships

- [[AppSettings]] (2 shared connections)
- [[test_managers.py]] (2 shared connections)
- [[scripts/gen_diagrams.py]] (1 shared connections)
- [[scripts/gen_diagrams_sl.py]] (1 shared connections)
- [[scripts/setup.sh]] (1 shared connections)
- [[normalize_phone()]] (1 shared connections)
- [[str]] (1 shared connections)

## Source Files

- `api/main.py`
- `api/tests/test_managers.py`

## Audit Trail

- EXTRACTED: 43 (84%)
- INFERRED: 8 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*