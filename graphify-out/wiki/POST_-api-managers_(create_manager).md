# POST /api/managers (create_manager)

> 12 nodes

## Key Concepts

- **env.py** (6 connections) — `api/db/migrations/env.py`
- **_get_url()** (5 connections) — `api/db/migrations/env.py`
- **_run_async_migrations()** (4 connections) — `api/db/migrations/env.py`
- **run_migrations_offline()** (3 connections) — `api/db/migrations/env.py`
- **run_migrations_online()** (3 connections) — `api/db/migrations/env.py`
- **_do_run_migrations()** (2 connections) — `api/db/migrations/env.py`
- **Alembic environment — async SQLAlchemy / asyncpg configuration.** (1 connections) — `api/db/migrations/env.py`
- **Read DATABASE_URL from settings (env / .env file).** (1 connections) — `api/db/migrations/env.py`
- **Run migrations without a live DB connection (generates SQL script).** (1 connections) — `api/db/migrations/env.py`
- **Inner helper called inside the async connection context.** (1 connections) — `api/db/migrations/env.py`
- **Create an async engine and run migrations inside it.** (1 connections) — `api/db/migrations/env.py`
- **Run migrations against a live database.** (1 connections) — `api/db/migrations/env.py`

## Relationships

- [[volunteers.js]] (1 shared connections)

## Source Files

- `api/db/migrations/env.py`

## Audit Trail

- EXTRACTED: 28 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*