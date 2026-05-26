# GET /api/errors (list_errors)

> 12 nodes

## Key Concepts

- **Task 4: Migrate call sites to get_app_settings** (12 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (# Remove:)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (# Before:)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (# Remove:)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (settings: Annotated[Settings, Depends(get_settings)],)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (settings: Annotated[AppSettings, Depends(get_app_settings)],)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (settings: Annotated[Settings, Depends(get_settings)],)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (settings: Annotated[AppSettings, Depends(get_app_settings)],)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (# Remove:)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:python (# Before:)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:block33 (docker compose exec api pytest tests/ -v)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`
- **code:bash (git add api/routers/log_entries.py api/routers/auth.py api/r)** (1 connections) — `docs/superpowers/plans/2026-05-20-settings-table.md`

## Relationships

- [[Community 539]] (1 shared connections)

## Source Files

- `docs/superpowers/plans/2026-05-20-settings-table.md`

## Audit Trail

- EXTRACTED: 23 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*