# Community 504

> 6 nodes

## Key Concepts

- **test_migrations.py** (3 connections) — `api/tests/test_migrations.py`
- **migrations_engine()** (2 connections) — `api/tests/test_migrations.py`
- **test_migration_roundtrip()** (2 connections) — `api/tests/test_migrations.py`
- **Migration roundtrip test — runs against belpro_test_migrations (isolated DB).** (1 connections) — `api/tests/test_migrations.py`
- **Session-scoped engine targeting belpro_test_migrations.** (1 connections) — `api/tests/test_migrations.py`
- **stamp base → upgrade head → downgrade -1 → upgrade head all exit 0.** (1 connections) — `api/tests/test_migrations.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `api/tests/test_migrations.py`

## Audit Trail

- EXTRACTED: 10 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*