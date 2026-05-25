# persist_report()

> 42 nodes

## Key Concepts

- **Report Delivery Error Visibility Implementation Plan** (8 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 3b — Fix manager WhatsApp exception handling** (6 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 1b — Add the logger (no logic change yet)** (5 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 2b — Fix manager email exception handling** (4 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Task 4 — Fix stale field names in the n8n monthly reports Code node** (4 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 4a — Update the Code node JavaScript** (4 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Task 1 — Add logger to reports.py and write failing tests for delivery error logging** (3 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 1a — Add the failing tests** (3 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Task 2 — Implement delivery error logging for email failures (volunteer + manager)** (3 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 2a — Fix volunteer email exception handling** (3 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Task 3 — Implement delivery error logging for WhatsApp failures (volunteer + manager)** (3 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 3a — Fix volunteer WhatsApp exception handling** (3 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Background the implementer needs** (2 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 4b — Reimport the workflow into n8n** (2 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **Step 4c — Commit** (2 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **2026-05-21-report-delivery-error-visibility.md** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **File Map** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:python (class ErrorLog(Base):)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:python (# ── report delivery error logging ─────────────────────────)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:block3 (docker compose exec api pytest tests/test_reports.py::test_s)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:python (import logging)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:python (logger = logging.getLogger(__name__))** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:python (from models.error_log import ErrorLog)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:block7 (docker compose exec api pytest tests/test_reports.py -v)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- **code:python (if will_email:)** (1 connections) — `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`
- *... and 17 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `docs/superpowers/plans/2026-05-21-report-delivery-error-visibility.md`

## Audit Trail

- EXTRACTED: 82 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*