# Community 398

> 9 nodes

## Key Concepts

- **Task 2: Error log API endpoints + schemas + tests** (9 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:python (# api/tests/test_errors.py)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (docker compose exec api pytest tests/test_errors.py -v)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:python (# api/schemas/error_log.py)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:python (# api/routers/errors.py)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:python (from routers.errors import router as errors_router)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:python (app.include_router(errors_router, prefix="/api"))** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (docker compose exec api pytest tests/test_errors.py -v)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (git add api/schemas/error_log.py api/routers/errors.py api/t)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`

## Relationships

- [[Community 433]] (1 shared connections)

## Source Files

- `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`

## Audit Trail

- EXTRACTED: 17 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*