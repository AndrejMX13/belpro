# Report Delivery Error Visibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make email and WhatsApp report delivery failures visible in Docker logs (Python logger) and the Dnevnik napak dashboard (ErrorLog DB rows), prevent SmtpNotConfiguredError from aborting the whole batch, log invalid phone numbers, and fix stale field names in the n8n summary Code node.

**Architecture:** All API-side changes are confined to `api/routers/reports.py`. We add a module-level logger, import the `ErrorLog` model, collapse `SmtpNotConfiguredError` into the general exception handler so a misconfigured SMTP server no longer kills the entire run, write `ErrorLog` rows directly via the open DB session for every delivery failure, and add an explicit error for invalid phone numbers rather than silently skipping. The n8n workflow JSON is patched to reference correct API response field names and reimported via the import script.

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy async, pytest-asyncio, `unittest.mock.AsyncMock`

---

## File Map

| File | Change |
|---|---|
| `api/routers/reports.py` | Add logger; collapse `SmtpNotConfiguredError`; add `logger.error` + `ErrorLog` write for all 4 failure points; add invalid-phone error |
| `api/tests/test_reports.py` | Add 4 new tests covering the above behaviours |
| `n8n/workflows/monthly_reports.json` | Fix `jsCode` field names in `Zabeleži Rezultat` Code node |

---

## Background the implementer needs

**What `send_monthly_reports` does today (lines 172–352 of `api/routers/reports.py`):**
- Iterates active volunteers; for each with approved entries it generates a PDF and attempts email + WhatsApp delivery
- Does the same for the consolidated manager PDF
- Catches delivery exceptions and collects them in an `errors: list[str]` that is returned in the JSON response
- **Gap 1:** No `import logging` / no `logger` — nothing reaches Docker logs
- **Gap 2:** No `ErrorLog` rows written — nothing reaches Dnevnik napak
- **Gap 3:** `SmtpNotConfiguredError` has its own `except` block that does `raise HTTPException(status_code=503, ...)`, aborting the entire batch (all remaining volunteers stop, WhatsApp sends never happen)
- **Gap 4:** `normalize_phone` returning `None` causes silent skip — volunteer gets nothing, no error anywhere

**ErrorLog model** (`api/models/error_log.py`):
```python
class ErrorLog(Base):
    service: Mapped[str]      # e.g. "api"
    operation: Mapped[str]    # e.g. "send_monthly_reports"
    message: Mapped[str]      # short human-readable label
    detail: Mapped[str | None] # full error string
    acknowledged: Mapped[bool] # default False
    created_at: Mapped[datetime]
```

**n8n Code node bug** — `Zabeleži Rezultat` node currently references:
- `result.sent_to_volunteers` → actual field: `result.sent_via_email` + `result.sent_via_whatsapp`
- `result.manager_sent` → actual: `result.manager_email_sent` / `result.manager_whatsapp_sent`
- `result.skipped_no_email` → actual: `result.skipped_no_channel`

**Test conventions:**
- Tests run inside the container: `docker compose exec api pytest tests/test_reports.py -v`
- `volunteer_factory(**overrides)` supports any `Volunteer` field as a keyword arg
- Mock `send_email` at import site: `"routers.reports.send_email"` (not `"services.email.send_email"`)
- Mock `EvolutionClient.send_document` at the class: `"services.evolution.EvolutionClient.send_document"`
- `send_email` is `async def` — use `new_callable=AsyncMock`
- `db_session` fixture gives access to the test DB session for assertions

---

## Task 1 — Add logger to reports.py and write failing tests for delivery error logging

**Files:**
- Modify: `api/tests/test_reports.py` (add tests — they will FAIL until Task 2)
- Modify: `api/routers/reports.py` (add `import logging` + `logger`)

### Step 1a — Add the failing tests

- [ ] Open `api/tests/test_reports.py` and append these four tests:

```python
# ── report delivery error logging ─────────────────────────────────────────────
from unittest.mock import AsyncMock, patch

from models.error_log import ErrorLog
from services.email import SmtpNotConfiguredError


async def test_send_monthly_email_failure_logged(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """Email delivery failure writes an ErrorLog row and appears in response errors."""
    v = await volunteer_factory(report_email=True, email="vol@test.si")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 1), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    with patch("routers.reports.send_email", new_callable=AsyncMock,
               side_effect=Exception("SMTP connection refused")):
        r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("e-pošta" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
    assert any("e-pošta" in (row.detail or "") for row in rows)


async def test_send_monthly_whatsapp_failure_logged(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """WhatsApp delivery failure writes an ErrorLog row and appears in response errors."""
    v = await volunteer_factory(report_whatsapp=True, phone="+38641111222")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 2), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    with patch(
        "services.evolution.EvolutionClient.send_document",
        new_callable=AsyncMock,
        side_effect=Exception("Evolution 500"),
    ):
        r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("WhatsApp" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
    assert any("WhatsApp" in (row.detail or "") for row in rows)


async def test_send_monthly_smtp_not_configured_does_not_abort_batch(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """SmtpNotConfiguredError must NOT abort the batch — response is 200 with error in list."""
    v = await volunteer_factory(report_email=True, email="vol@test.si")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 3), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    with patch("routers.reports.send_email", new_callable=AsyncMock,
               side_effect=SmtpNotConfiguredError("SMTP ni konfiguriran")):
        r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("e-pošta" in e for e in data["errors"])


async def test_send_monthly_invalid_phone_logged(
    client: AsyncClient, auth: dict, db_session, volunteer_factory, log_entry_factory
) -> None:
    """Volunteer with WhatsApp enabled but invalid phone gets an error log entry."""
    v = await volunteer_factory(report_whatsapp=True, phone="not-a-phone")
    await log_entry_factory(
        v.id, work_date=date(2026, 3, 4), hours=Decimal("2.0"), status=EntryStatus.APPROVED
    )

    r = await client.post("/api/reports/send-monthly?year=2026&month=3", headers=auth)

    assert r.status_code == 200
    data = r.json()
    assert any("WhatsApp" in e for e in data["errors"])
    rows = (
        await db_session.execute(
            select(ErrorLog).where(ErrorLog.operation == "send_monthly_reports")
        )
    ).scalars().all()
    assert len(rows) >= 1
```

- [ ] **Run the tests to verify they FAIL**

```
docker compose exec api pytest tests/test_reports.py::test_send_monthly_email_failure_logged tests/test_reports.py::test_send_monthly_whatsapp_failure_logged tests/test_reports.py::test_send_monthly_smtp_not_configured_does_not_abort_batch tests/test_reports.py::test_send_monthly_invalid_phone_logged -v
```

Expected: FAIL — some with `AssertionError` (no ErrorLog rows), `test_send_monthly_smtp_not_configured_does_not_abort_batch` with `assert r.status_code == 200` (currently returns 503).

### Step 1b — Add the logger (no logic change yet)

- [ ] In `api/routers/reports.py`, add `import logging` to the stdlib imports block (after `from __future__ import annotations`):

```python
import logging
import io
import uuid
# ... rest of stdlib imports
```

- [ ] Add the module-level logger after the last import line:

```python
logger = logging.getLogger(__name__)
```

- [ ] Add `ErrorLog` to the model imports (alongside `LogEntry`, `Manager`, etc.):

```python
from models.error_log import ErrorLog
```

- [ ] Run existing test suite to confirm nothing broke:

```
docker compose exec api pytest tests/test_reports.py -v
```

Expected: only the 4 new tests fail; all pre-existing tests pass.

---

## Task 2 — Implement delivery error logging for email failures (volunteer + manager)

**Files:**
- Modify: `api/routers/reports.py` (volunteer email block + manager email block)

### Step 2a — Fix volunteer email exception handling

- [ ] Locate the volunteer email delivery block in `send_monthly_reports`. It currently looks like:

```python
        if will_email:
            body = (...)
            try:
                await send_email(...)
                sent_via_email.append(f"{vol.first_name} {vol.last_name} <{vol.email}>")
            except SmtpNotConfiguredError as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{vol.first_name} {vol.last_name} (e-pošta): {exc}")
```

Replace the two `except` blocks with a single one:

```python
        if will_email:
            body = (...)
            try:
                await send_email(...)
                sent_via_email.append(f"{vol.first_name} {vol.last_name} <{vol.email}>")
            except Exception as exc:  # noqa: BLE001
                detail = f"{vol.first_name} {vol.last_name} (e-pošta): {exc}"
                logger.error("Report email delivery failed: %s", detail)
                db.add(ErrorLog(
                    service="api",
                    operation="send_monthly_reports",
                    message="Dostava e-poštnega poročila ni uspela",
                    detail=detail,
                ))
                errors.append(detail)
```

### Step 2b — Fix manager email exception handling

- [ ] Locate the manager email delivery block. It currently has the same two-`except` pattern:

```python
        if manager_will_email:
            ...
            try:
                await send_email(...)
                manager_email_sent = True
            except SmtpNotConfiguredError as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc
            except Exception as exc:  # noqa: BLE001
                errors.append(f"Upravljalec (e-pošta): {exc}")
```

Replace with:

```python
        if manager_will_email:
            ...
            try:
                await send_email(...)
                manager_email_sent = True
            except Exception as exc:  # noqa: BLE001
                detail = f"Upravljalec (e-pošta): {exc}"
                logger.error("Report email delivery to manager failed: %s", detail)
                db.add(ErrorLog(
                    service="api",
                    operation="send_monthly_reports",
                    message="Dostava e-poštnega poročila upravljalcu ni uspela",
                    detail=detail,
                ))
                errors.append(detail)
```

- [ ] **Run the email tests — expect them to pass now:**

```
docker compose exec api pytest tests/test_reports.py::test_send_monthly_email_failure_logged tests/test_reports.py::test_send_monthly_smtp_not_configured_does_not_abort_batch -v
```

Expected: PASS

---

## Task 3 — Implement delivery error logging for WhatsApp failures (volunteer + manager)

**Files:**
- Modify: `api/routers/reports.py` (volunteer WhatsApp block + manager WhatsApp block)

### Step 3a — Fix volunteer WhatsApp exception handling

- [ ] Locate the volunteer WhatsApp delivery block. It currently looks like:

```python
        if will_whatsapp:
            normalized = normalize_phone(vol.phone)
            if normalized:
                try:
                    await wa_client.send_document(normalized, pdf_bytes, filename, caption)
                    sent_via_whatsapp.append(f"{vol.first_name} {vol.last_name}")
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{vol.first_name} {vol.last_name} (WhatsApp): {exc}")
```

Replace with:

```python
        if will_whatsapp:
            normalized = normalize_phone(vol.phone)
            if not normalized:
                detail = (
                    f"{vol.first_name} {vol.last_name} (WhatsApp): "
                    f"neveljavna telefonska številka '{vol.phone}'"
                )
                logger.warning("Invalid phone for WhatsApp report delivery: %s", detail)
                db.add(ErrorLog(
                    service="api",
                    operation="send_monthly_reports",
                    message="Neveljavna telefonska številka za WhatsApp poročilo",
                    detail=detail,
                ))
                errors.append(detail)
            else:
                try:
                    await wa_client.send_document(normalized, pdf_bytes, filename, caption)
                    sent_via_whatsapp.append(f"{vol.first_name} {vol.last_name}")
                except Exception as exc:  # noqa: BLE001
                    detail = f"{vol.first_name} {vol.last_name} (WhatsApp): {exc}"
                    logger.error("Report WhatsApp delivery failed: %s", detail)
                    db.add(ErrorLog(
                        service="api",
                        operation="send_monthly_reports",
                        message="Dostava WhatsApp poročila ni uspela",
                        detail=detail,
                    ))
                    errors.append(detail)
```

### Step 3b — Fix manager WhatsApp exception handling

- [ ] Locate the manager WhatsApp delivery block:

```python
        if manager_will_whatsapp:
            normalized_mgr = normalize_phone(manager.phone)
            if normalized_mgr:
                try:
                    await wa_client.send_document(
                        normalized_mgr, consolidated_bytes, consolidated_filename, mgr_caption
                    )
                    manager_whatsapp_sent = True
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"Upravljalec (WhatsApp): {exc}")
```

Replace with:

```python
        if manager_will_whatsapp:
            normalized_mgr = normalize_phone(manager.phone)
            if not normalized_mgr:
                detail = f"Upravljalec (WhatsApp): neveljavna telefonska številka '{manager.phone}'"
                logger.warning("Invalid manager phone for WhatsApp report delivery: %s", detail)
                db.add(ErrorLog(
                    service="api",
                    operation="send_monthly_reports",
                    message="Neveljavna telefonska številka upravljalca za WhatsApp poročilo",
                    detail=detail,
                ))
                errors.append(detail)
            else:
                try:
                    await wa_client.send_document(
                        normalized_mgr, consolidated_bytes, consolidated_filename, mgr_caption
                    )
                    manager_whatsapp_sent = True
                except Exception as exc:  # noqa: BLE001
                    detail = f"Upravljalec (WhatsApp): {exc}"
                    logger.error("Report WhatsApp delivery to manager failed: %s", detail)
                    db.add(ErrorLog(
                        service="api",
                        operation="send_monthly_reports",
                        message="Dostava WhatsApp poročila upravljalcu ni uspela",
                        detail=detail,
                    ))
                    errors.append(detail)
```

- [ ] **Run all four new tests:**

```
docker compose exec api pytest tests/test_reports.py::test_send_monthly_email_failure_logged tests/test_reports.py::test_send_monthly_whatsapp_failure_logged tests/test_reports.py::test_send_monthly_smtp_not_configured_does_not_abort_batch tests/test_reports.py::test_send_monthly_invalid_phone_logged -v
```

Expected: all 4 PASS

- [ ] **Run the full test suite to confirm no regressions:**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Commit the API changes:**

```bash
git add api/routers/reports.py api/tests/test_reports.py
git commit -m "$(cat <<'EOF'
feat: log report delivery failures to Docker logs and Dnevnik napak

Email and WhatsApp delivery errors in send_monthly_reports now emit
logger.error (Docker logs) and write an ErrorLog row (Dnevnik napak)
for each failure. SmtpNotConfiguredError no longer aborts the batch.
Invalid phone numbers produce an explicit error instead of silent skip.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4 — Fix stale field names in the n8n monthly reports Code node

**Files:**
- Modify: `n8n/workflows/monthly_reports.json` (the `jsCode` value in the `code-log` node)

### Step 4a — Update the Code node JavaScript

- [ ] In `n8n/workflows/monthly_reports.json`, find the `code-log` node. Its `parameters.jsCode` currently reads:

```javascript
const result = $input.first().json;
const sent = result.sent_to_volunteers || [];
const errors = result.errors || [];

const lines = [
  `BelPro mesečna poročila — ${result.month}/${result.year}`,
  `Poslano prostovoljcem: ${sent.length}`,
  `Upravljalec obveščen: ${result.manager_sent ? 'Da' : 'Ne'}`,
  `Preskočeni (brez vnosov): ${(result.skipped_no_entries || []).length}`,
  `Preskočeni (brez e-pošte): ${(result.skipped_no_email || []).length}`,
];

if (errors.length > 0) {
  lines.push(`NAPAKE (${errors.length}):`);
  errors.forEach(e => lines.push('  ' + e));
}

console.log(lines.join('\n'));
return [{ json: result }];
```

Replace the `jsCode` value (escape newlines as `\n` in the JSON string) with:

```javascript
const result = $input.first().json;
const sentEmail = result.sent_via_email || [];
const sentWa = result.sent_via_whatsapp || [];
const errors = result.errors || [];

const lines = [
  `BelPro mesečna poročila — ${result.month}/${result.year}`,
  `Poslano e-pošta: ${sentEmail.length}, WhatsApp: ${sentWa.length}`,
  `Upravljalec — e-pošta: ${result.manager_email_sent ? 'Da' : 'Ne'}, WhatsApp: ${result.manager_whatsapp_sent ? 'Da' : 'Ne'}`,
  `Preskočeni (brez vnosov): ${(result.skipped_no_entries || []).length}`,
  `Preskočeni (brez kanala): ${(result.skipped_no_channel || []).length}`,
];

if (errors.length > 0) {
  lines.push(`NAPAKE (${errors.length}):`);
  errors.forEach(e => lines.push('  ' + e));
}

console.log(lines.join('\n'));
return [{ json: result }];
```

**Important:** The JSON file stores the JS as a single string with `\n` line breaks. Edit the `jsCode` field value only — do not change node IDs, positions, credentials, or any other field.

The `jsCode` value in the JSON must be (all on one line with literal `\n`):
```
"const result = $input.first().json;\nconst sentEmail = result.sent_via_email || [];\nconst sentWa = result.sent_via_whatsapp || [];\nconst errors = result.errors || [];\n\nconst lines = [\n  `BelPro mesečna poročila — ${result.month}/${result.year}`,\n  `Poslano e-pošta: ${sentEmail.length}, WhatsApp: ${sentWa.length}`,\n  `Upravljalec — e-pošta: ${result.manager_email_sent ? 'Da' : 'Ne'}, WhatsApp: ${result.manager_whatsapp_sent ? 'Da' : 'Ne'}`,\n  `Preskočeni (brez vnosov): ${(result.skipped_no_entries || []).length}`,\n  `Preskočeni (brez kanala): ${(result.skipped_no_channel || []).length}`,\n];\n\nif (errors.length > 0) {\n  lines.push(`NAPAKE (${errors.length}):`);\n  errors.forEach(e => lines.push('  ' + e));\n}\n\nconsole.log(lines.join('\\n'));\nreturn [{ json: result }];\n"
```

This same string must appear in **both** places the node appears in the JSON: under `nodes[].parameters.jsCode` and under `activeVersion.nodes[].parameters.jsCode`.

### Step 4b — Reimport the workflow into n8n

- [ ] Run the import script (from the project root, using PowerShell):

```powershell
python scripts/n8n_workflows.py import
```

Expected output: confirmation that `BelPro — Mesečna Poročila` was updated successfully. No errors.

### Step 4c — Commit

- [ ] Commit the n8n change:

```bash
git add n8n/workflows/monthly_reports.json
git commit -m "$(cat <<'EOF'
fix: correct field names in monthly reports n8n summary Code node

sent_to_volunteers → sent_via_email/sent_via_whatsapp,
manager_sent → manager_email_sent/manager_whatsapp_sent,
skipped_no_email → skipped_no_channel.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Self-Review

**Spec coverage:**
- Docker logging for email failures ✓ Task 2
- Docker logging for WhatsApp failures ✓ Task 3
- Dnevnik napak (ErrorLog rows) for email failures ✓ Task 2
- Dnevnik napak (ErrorLog rows) for WhatsApp failures ✓ Task 3
- SmtpNotConfiguredError no longer aborts batch ✓ Task 2 (collapsed into `except Exception`)
- Invalid phone number logged as error ✓ Task 3
- n8n Code node field names fixed ✓ Task 4
- Tests for all 4 behaviours ✓ Task 1

**Placeholder scan:** None found. All code blocks are complete.

**Type consistency:**
- `ErrorLog` constructor arguments (`service`, `operation`, `message`, `detail`) match the model definition throughout.
- `logger` is used consistently as `logger.error(...)` and `logger.warning(...)`.
- `detail` variable is consistently a `str` built before being passed to both `logger` and `ErrorLog`.
