# Community 503

> 7 nodes

## Key Concepts

- **Task 1: Alembic migration — seed `evolution_instance_name`** (7 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`
- **code:python (async def test_settings_table_seeded_evolution_instance_name)** (1 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`
- **code:bash (docker compose exec api pytest tests/test_app_settings.py::t)** (1 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`
- **code:python (# api/db/migrations/versions/015_seed_evolution_instance_nam)** (1 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`
- **code:bash (docker compose exec api alembic upgrade head)** (1 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`
- **code:bash (docker compose exec api pytest tests/test_app_settings.py::t)** (1 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`
- **code:bash (git add api/db/migrations/versions/015_seed_evolution_instan)** (1 connections) — `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`

## Relationships

- [[Community 401]] (1 shared connections)

## Source Files

- `docs/superpowers/plans/2026-05-25-evolution-instance-appsetting.md`

## Audit Trail

- EXTRACTED: 13 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*