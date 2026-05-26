# scripts/upgrade.sh

> 22 nodes

## Key Concepts

- **Design Details** (7 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Report Auto-Hour Implementation Design** (5 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Ops server (`ops/scripts/ops_server.py`)** (4 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Schemas (`api/schemas/admin.py`)** (3 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Test Plan** (3 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **AppSettings (`api/services/app_settings.py`)** (2 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Admin router (`api/routers/admin.py`)** (2 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **DB seed migration** (2 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **2026-05-22-report-auto-hour-design.md** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Scope** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Files Touched** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python (@property)** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python (report_auto_hour: int)** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python (report_auto_hour: int | None = Field(None, ge=0, le=23))** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python ("report_auto_hour": app_settings.report_auto_hour,)** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python ("0 {report_hour} {day} * * /app/scripts/monthly_report_send.)** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python (report_hour = max(0, min(int(payload.get("report_auto_hour",)** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:python (report_hour = max(0, min(int(rows.get("report_auto_hour", 7))** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **code:sql (INSERT INTO settings (name, value, value_type))** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **Frontend (`frontend/js/admin.js`)** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **New tests — `test_admin.py`** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`
- **New tests — `test_app_settings.py`** (1 connections) — `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`

## Relationships

- No strong cross-community connections detected

## Source Files

- `docs/superpowers/specs/2026-05-22-report-auto-hour-design.md`

## Audit Trail

- EXTRACTED: 42 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*