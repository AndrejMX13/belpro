# Community 401

> 9 nodes

## Key Concepts

- **Task 4: Automated backup job** (9 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (#!/bin/bash)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (docker compose up -d --build ops)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (docker compose exec ops /app/scripts/backup.sh)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:block27 ([backup] Starting backup: 20260520_020000)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (docker compose exec ops ls /backups/)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (docker compose exec -e POSTGRES_PASSWORD=wrong ops /app/scri)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (curl -s http://localhost:8100/api/errors \)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`
- **code:bash (git add ops/scripts/backup.sh)** (1 connections) — `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`

## Relationships

- [[Community 432]] (1 shared connections)

## Source Files

- `docs/superpowers/plans/2026-05-20-ops-sidecar-and-error-log.md`

## Audit Trail

- EXTRACTED: 17 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*