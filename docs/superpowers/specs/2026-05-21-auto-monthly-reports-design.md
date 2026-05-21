# Auto Monthly Report Delivery — Design

## Goal

Add automatic monthly report delivery triggered by a cron job in the ops service, with the delivery day and reporting period configurable from the Sistemske nastavitve dashboard page.

## Architecture

Two new runtime-tunable settings (`report_auto_day`, `report_auto_period`) are stored in the existing `AppSetting` table and exposed via the existing admin settings API and UI. When the manager saves these settings, the API notifies the ops service via an internal HTTP call. Ops regenerates its crontab and reloads crond. On the configured day each month, the cron entry calls a new ops script that calls the existing `POST /api/reports/send-monthly` endpoint.

## Tech Stack

Python stdlib `http.server.ThreadingHTTPServer` for the ops notification server; existing FastAPI admin endpoints for settings; existing `POST /api/reports/send-monthly` for the actual send; BusyBox crond on Alpine for scheduling.

---

## Section 1 — Settings Storage

Two new keys added to the `settings` table (`AppSetting` model, `api/models/app_setting.py`):

| name | type | default | constraint |
|------|------|---------|------------|
| `report_auto_day` | int | 28 | 1–28 |
| `report_auto_period` | str | `current` | `current` or `previous` |

**`report_auto_day`** — day of month crond fires. Capped at 28 to guarantee firing every month including February.

**`report_auto_period`** — which calendar month's entries to include:
- `current`: report covers `today.year / today.month` (entries approved so far in the current month)
- `previous`: report covers the previous calendar month — `(today.replace(day=1) - timedelta(days=1)).year / .month`. Handles the January→December year boundary correctly.

No migration needed — rows are created by the first PATCH save, identical to existing settings (`max_photos_per_entry`, etc.).

New `AppSettings` properties (`api/services/app_settings.py`):

```python
@property
def report_auto_day(self) -> int:
    return self._int("report_auto_day", 28)

@property
def report_auto_period(self) -> str:
    return self._str("report_auto_period", "current")
```

New schema fields (`api/schemas/admin.py`):

```python
# AdminSettingsResponse
report_auto_day: int
report_auto_period: str

# AdminSettingsUpdate
report_auto_day: int | None = Field(None, ge=1, le=28)
report_auto_period: str | None = Field(None, pattern="^(current|previous)$")
```

---

## Section 2 — Ops HTTP Server

### Process model

`ops/entrypoint.sh` changes from running crond as the sole foreground process to:

```bash
#!/bin/bash
crond -l 2          # start crond in background (daemonises)
exec python3 /app/scripts/ops_server.py   # HTTP server becomes foreground / PID 1
```

### ops_server.py

`ops/scripts/ops_server.py` — `ThreadingHTTPServer` on `0.0.0.0:9000` (internal Docker network only, not exposed to host).

**On startup (before accepting requests):**
1. Fetch current settings from `GET http://api:8000/api/admin/settings` (API is guaranteed healthy via `depends_on`).
2. Regenerate `/etc/crontabs/ops` from settings.
3. Send SIGHUP to crond to reload.

**Endpoint: `POST /reconfigure`**
- Validates `X-Internal-Key` header against `API_SECRET_KEY` env var. Returns `403` on mismatch.
- Returns `202 Accepted` immediately (the request thread is the worker thread — `ThreadingHTTPServer` already handles each request in its own thread, so the main loop never blocks).
- Worker: parses JSON payload → regenerates `/etc/crontabs/ops` → sends SIGHUP to crond → logs failure via `POST /api/errors` if anything goes wrong.

**Endpoint: `GET /health`**
- Returns `200 OK` with `{"status": "ok"}`. Used by Docker healthcheck.

### Crontab template

The generated `/etc/crontabs/ops` always contains the fixed entries plus the monthly report line:

```
# m h dom mon dow command
0 2 * * * /app/scripts/backup.sh >> /proc/1/fd/1 2>&1
0 3 * * * /app/scripts/photo_cleanup.py >> /proc/1/fd/1 2>&1
0 7 <report_auto_day> * * /app/scripts/monthly_report_send.py --period <report_auto_period> >> /proc/1/fd/1 2>&1
```

The static `ops/crontab` file (baked into the image) serves as the initial default (day=28, period=current) and as the template reference. The ops server writes the dynamically generated version to `/etc/crontabs/ops` at runtime, overwriting the baked-in file.

---

## Section 3 — API Notification Call

After a successful `PATCH /admin/settings` save, `api/routers/admin.py` calls:

```
POST http://ops:9000/reconfigure
X-Internal-Key: <API_SECRET_KEY>
Content-Type: application/json

{"report_auto_day": 28, "report_auto_period": "current", ...}
```

Fire-and-forget with a 3-second timeout using `httpx.AsyncClient`. If ops is unreachable or returns an error, the failure is written to `ErrorLog` but the settings save response is **not** affected — the manager's PATCH still returns the updated settings normally.

`docker-compose.yml` adds one env var to the api service:

```yaml
OPS_URL: http://ops:9000
```

No port is exposed to the host. Docker's internal network handles `http://ops:9000` from the api container.

---

## Section 4 — Monthly Report Send Script

`ops/scripts/monthly_report_send.py` — invoked by crond.

```
usage: monthly_report_send.py --period {current,previous}
```

**Month resolution:**

```python
today = datetime.now(timezone.utc)
if args.period == "previous":
    ref = today.replace(day=1) - timedelta(days=1)
    year, month = ref.year, ref.month
else:
    year, month = today.year, today.month
```

Calls `POST http://api:8000/api/reports/send-monthly?year={year}&month={month}` with `X-Internal-Key` auth. On HTTP error or connection failure, reports via `POST /api/errors` using the established ops error reporting pattern (same as `photo_cleanup.py`). Logs a success summary to stdout (captured by crond to Docker logs).

---

## Section 5 — Docker Compose Changes

**api service** — add env var:
```yaml
OPS_URL: http://ops:9000
```

**ops service** — add healthcheck:
```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -qO /dev/null http://localhost:9000/health || exit 1"]
  interval: 15s
  timeout: 5s
  retries: 3
  start_period: 30s
```

No new volumes, no new port mappings.

---

## Error Handling Summary

| Failure point | Behaviour |
|---------------|-----------|
| API can't reach ops on settings save | Logged to ErrorLog; settings save succeeds |
| ops can't reach API on startup (settings fetch) | 3 attempts, 2 s apart; fall back to baked-in default crontab if all fail, log to stdout |
| Crontab write or crond SIGHUP fails | Logged to ErrorLog via `POST /api/errors` |
| monthly_report_send.py HTTP error | Logged to ErrorLog via `POST /api/errors` |
| Report delivery failures (email/WhatsApp) | Handled by existing API logic; logged to ErrorLog with error badge |

---

## Files Changed

| File | Change |
|------|--------|
| `api/services/app_settings.py` | Add `report_auto_day` and `report_auto_period` properties |
| `api/schemas/admin.py` | Add two new fields to response and update schemas |
| `api/routers/admin.py` | Notify ops after successful PATCH |
| `frontend/js/admin.js` | Add day and period inputs to Sistemske nastavitve card |
| `ops/entrypoint.sh` | Start crond in background, run ops_server.py in foreground |
| `ops/scripts/ops_server.py` | New: threaded HTTP server with `/reconfigure` and `/health` |
| `ops/scripts/monthly_report_send.py` | New: calls send-monthly API endpoint |
| `ops/crontab` | Add default monthly report line (day=28, period=current) |
| `docker-compose.yml` | Add `OPS_URL` to api env; add ops healthcheck |
