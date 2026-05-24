# Coverage Baseline

**Last updated:** 2026-05-24 · **Total: 84%** (240 tests, 3471 statements)

Regenerate: `docker compose exec api pytest tests/ --cov=. --cov-report=term-missing -q`

---

## Gaps by file

| File | Cover | Key uncovered areas |
|------|-------|---------------------|
| [routers/log_entries.py](../api/routers/log_entries.py) | 30% | photo serve/delete, confirm entry, update entry, most upload logic (L48–605) |
| [routers/reports.py](../api/routers/reports.py) | 36% | PDF generation, auto-send, report listing/download (L131–403) |
| [routers/managers.py](../api/routers/managers.py) | 42% | manager creation, GDPR consent, config-info sync (L31–165) |
| [services/email.py](../api/services/email.py) | 39% | email send path (L24–88) — intentionally untested (external service) |
| [routers/volunteers.py](../api/routers/volunteers.py) | 50% | update, deactivate, delete, check-emso (L126–368) |
| [main.py](../api/main.py) | 50% | health endpoints, lifespan startup hooks (L40–173) |
| [routers/auth.py](../api/routers/auth.py) | 80% | cookie/session edge cases (L26–39) |
| [routers/admin.py](../api/routers/admin.py) | 80% | error branches (L64, 101–113) |
| [routers/analytics.py](../api/routers/analytics.py) | 82% | pagination/edge paths (L48, 64, 108, 131–160) |

## Well-covered (≥89%)

All models, schemas, services (encryption, password, PDF, report storage) — 100% or near.  
`conftest.py`, `services/app_settings.py`, `services/logo.py`, `core/settings.py` — 97–100%.
