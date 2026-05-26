# Community 311

> 11 nodes

## Key Concepts

- **Task 3: Admin router + integration tests** (11 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (# ── Integration tests for GET/PATCH /api/admin/settings ───)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:block15 (docker compose exec api pytest tests/test_app_settings.py -k)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python ("""Pydantic schemas for the admin settings endpoints.""")** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python ("""Admin router — runtime-tunable settings management.""")** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (from routers.admin import router as admin_router)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (app.include_router(admin_router, prefix="/api"))** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (from routers.admin import router as admin_router)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (app.include_router(admin_router, prefix="/api"))** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:block22 (docker compose exec api pytest tests/test_app_settings.py -v)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:bash (git add api/schemas/admin.py api/routers/admin.py api/main.p)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`

## Relationships

- [[Community 539]] (1 shared connections)

## Source Files

- `docs/superpowers/plans/2026-05-20-settings-table.md`

## Audit Trail

- EXTRACTED: 21 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*