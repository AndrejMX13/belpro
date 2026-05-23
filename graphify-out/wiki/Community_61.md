# Community 61

> 9 nodes · cohesion 0.22

## Key Concepts

- **conftest.py** (6 connections) — `api/tests/conftest.py`
- **engine()** (6 connections) — `api/tests/conftest.py`
- **auth()** (2 connections) — `api/tests/conftest.py`
- **client()** (2 connections) — `api/tests/conftest.py`
- **db_session()** (2 connections) — `api/tests/conftest.py`
- **AsyncClient with get_db dependency wired to the test session.** (1 connections) — `api/tests/conftest.py`
- **HTTP Basic Auth header for the seeded manager.** (1 connections) — `api/tests/conftest.py`
- **Run Alembic migrations against belpro_test, seed one Manager row.     Drops all** (1 connections) — `api/tests/conftest.py`
- **Per-test session inside a SAVEPOINT.  The app's commit() releases the     savepo** (1 connections) — `api/tests/conftest.py`

## Relationships

- [[Community 25]] (1 shared connections)
- [[Community 22]] (1 shared connections)
- [[Community 36]] (1 shared connections)
- [[Community 11]] (1 shared connections)
- [[Community 8]] (1 shared connections)
- [[Community 46]] (1 shared connections)

## Source Files

- `api/tests/conftest.py`

## Audit Trail

- EXTRACTED: 18 (82%)
- INFERRED: 4 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*