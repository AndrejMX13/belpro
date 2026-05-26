# 014_seed_report_auto_hour.py

> 19 nodes

## Key Concepts

- **Task 1: Test Infrastructure** (10 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.1 — Create `belpro_test` database** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.2 — Create `api/.env.test`** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.3 — Create `api/requirements-test.txt`** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.4 — Create `api/pyproject.toml`** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.5 — Create `api/tests/__init__.py`** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.6 — Create `api/tests/conftest.py`** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.7 — Install test dependencies** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.8 — Verify infrastructure with a dry run** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **Step 1.9 — Commit** (2 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:bash (docker compose exec postgres psql -U belpro -c "CREATE DATAB)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:dotenv (# Test database — separate from production belpro DB)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:block3 (pytest>=8.0)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:toml ([tool.pytest.ini_options])** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:python** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:python (# Load test env BEFORE any app imports — must be the very fi)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:bash (cd api)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:bash (cd api)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`
- **code:bash (git add api/.env.test api/requirements-test.txt api/pyprojec)** (1 connections) — `docs/superpowers/plans/2026-05-09-test-suite.md`

## Relationships

- [[Community 393]] (1 shared connections)

## Source Files

- `docs/superpowers/plans/2026-05-09-test-suite.md`

## Audit Trail

- EXTRACTED: 37 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*