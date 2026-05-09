# Work Date Rename + Dashboard Entry Creation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename `entry_date` → `work_date` throughout the stack, expose it as an editable field in the entry detail form, and add a "Dodaj vnos" button on the volunteer detail page to create entries from the dashboard.

**Architecture:** An Alembic migration renames the DB column; all Python and JS references are updated to match. `work_date` is added to `LogEntryUpdate` so the existing PATCH endpoint can update it. A new modal form on the volunteer detail page POSTs to the existing `POST /log-entries` endpoint, which already accepts all required fields.

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy 2.x + Alembic, PostgreSQL, vanilla JS (no framework), n8n-mcp tools for workflow updates.

---

## File Map

| File | Change |
|------|--------|
| `api/db/migrations/versions/002_rename_entry_date_to_work_date.py` | Create — renames column and indexes |
| `api/models/log_entry.py` | Modify — rename field, update index name |
| `api/schemas/log_entry.py` | Modify — rename in all three schemas, add `work_date` to `LogEntryUpdate` |
| `api/routers/log_entries.py` | Modify — sort_by, date filters, create, update, email notify |
| `api/routers/reports.py` | Modify — 6 `LogEntry.entry_date` references |
| `api/routers/analytics.py` | Modify — 8 `LogEntry.entry_date` references |
| `api/routers/volunteers.py` | Modify — 3 `entry_date` references |
| `api/services/report_pdf.py` | Modify — 1 `e.entry_date` reference |
| `frontend/js/volunteers.js` | Modify — sort defaults, list columns, edit form, new entry form |
| `db/init.sql` | Modify — column name in schema (for fresh deployments) |
| `scripts/list_pending_entries.py` | Modify — 1 `entry_date` reference |

n8n workflows are updated in Tasks 8 using n8n-mcp — no direct file editing.

---

## Task 1: Alembic Migration

**Files:**
- Create: `api/db/migrations/versions/002_rename_entry_date_to_work_date.py`

- [ ] **Step 1: Create the migration file**

```python
# api/db/migrations/versions/002_rename_entry_date_to_work_date.py
"""Rename entry_date to work_date in log_entries.

Revision ID: 002
Revises: 001
Create Date: 2026-05-09
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename entry_date → work_date and update index names."""
    op.alter_column("log_entries", "entry_date", new_column_name="work_date")
    op.execute("ALTER INDEX idx_entries_date RENAME TO idx_entries_work_date")
    op.execute("ALTER INDEX idx_entries_vol_date RENAME TO idx_entries_vol_work_date")


def downgrade() -> None:
    op.execute("ALTER INDEX idx_entries_vol_work_date RENAME TO idx_entries_vol_date")
    op.execute("ALTER INDEX idx_entries_work_date RENAME TO idx_entries_date")
    op.alter_column("log_entries", "work_date", new_column_name="entry_date")
```

- [ ] **Step 2: Run the migration**

```bash
docker compose exec api alembic upgrade head
```

Expected output ends with: `Running upgrade 001 -> 002, Rename entry_date to work_date in log_entries`

- [ ] **Step 3: Verify the column was renamed**

```bash
docker compose exec postgres psql -U belpro -d belpro \
  -c "\d log_entries" | grep -E "work_date|entry_date"
```

Expected: `work_date | date | not null` — no `entry_date` row.

- [ ] **Step 4: Commit**

```bash
git add api/db/migrations/versions/002_rename_entry_date_to_work_date.py
git commit -m "feat: migration 002 — rename entry_date to work_date"
```

---

## Task 2: ORM Model + Schemas

**Files:**
- Modify: `api/models/log_entry.py`
- Modify: `api/schemas/log_entry.py`

- [ ] **Step 1: Update the ORM model**

In `api/models/log_entry.py`, make these two changes:

Change the index name on line ~49:
```python
        Index("idx_entries_vol_work_date", "volunteer_id", "work_date"),
```
(was `idx_entries_vol_date`)

Change the field name on line ~60:
```python
    work_date: Mapped[date] = mapped_column(Date)
```
(was `entry_date`)

The full `__table_args__` tuple after the change:
```python
    __table_args__ = (
        Index("idx_entries_volunteer", "volunteer_id"),
        Index("idx_entries_status", "status"),
        Index("idx_entries_work_date", "work_date"),
        Index("idx_entries_location", "location"),
        Index("idx_entries_created", "created_at"),
        Index("idx_entries_vol_work_date", "volunteer_id", "work_date"),
    )
```

- [ ] **Step 2: Update all schemas**

Replace the full content of `api/schemas/log_entry.py` with:

```python
"""Pydantic schemas for the LogEntry entity."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from models.log_entry import EntryStatus


class LogEntryCreate(BaseModel):
    """Fields required to create a new log entry."""

    volunteer_id: uuid.UUID
    work_date: date
    activity_description: Annotated[str, Field(min_length=1)]
    hours: Annotated[Decimal, Field(ge=Decimal("0.5"), le=Decimal("24.0"))]
    location: str | None = None
    raw_transcript: str | None = None
    # Defaults to pending_manager for dashboard / n8n-created entries.
    # n8n may override to pending_volunteer when the WhatsApp confirmation flow is active.
    status: EntryStatus = EntryStatus.PENDING_MANAGER


class LogEntryResponse(BaseModel):
    """Full log entry returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    volunteer_id: uuid.UUID
    work_date: date
    activity_description: str
    raw_transcript: str | None
    hours: Decimal
    location: str | None
    status: EntryStatus
    photos: list[PhotoResponse] = []
    volunteer_confirmed_at: datetime | None
    manager_approved_at: datetime | None
    manager_notified_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PhotoResponse(BaseModel):
    """A single photo attached to a log entry."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    log_entry_id: uuid.UUID
    photo_path: str
    photo_exif_timestamp: datetime | None
    photo_exif_lat: Decimal | None
    photo_exif_lon: Decimal | None
    uploaded_at: datetime


class LogEntryUpdate(BaseModel):
    """Editable fields — blocked once the entry is approved."""

    activity_description: Annotated[str, Field(min_length=1)] | None = None
    hours: Annotated[Decimal, Field(ge=Decimal("0.5"), le=Decimal("24.0"))] | None = None
    location: str | None = None
    work_date: date | None = None


class LogEntryListResponse(BaseModel):
    """Paginated log entry list."""

    items: list[LogEntryResponse]
    total: int
```

- [ ] **Step 3: Verify the API container still starts**

```bash
docker compose up -d --build api
docker compose logs api --tail=20
```

Expected: no import errors, `Application startup complete.`

- [ ] **Step 4: Commit**

```bash
git add api/models/log_entry.py api/schemas/log_entry.py
git commit -m "feat: rename entry_date to work_date in ORM model and schemas"
```

---

## Task 3: log_entries Router

**Files:**
- Modify: `api/routers/log_entries.py`

- [ ] **Step 1: Fix email notification (line ~62)**

Change:
```python
            f"<strong>{entry.entry_date}</strong> je bila <strong>{action}</strong> s strani upravljalca.</p>"
```
To:
```python
            f"<strong>{entry.work_date}</strong> je bila <strong>{action}</strong> s strani upravljalca.</p>"
```

- [ ] **Step 2: Fix sort_by Literal and date filters (lines ~148–169)**

Change the `sort_by` parameter:
```python
    sort_by: Literal["work_date", "hours", "created_at", "status", "activity_description", "location"] = Query(default="work_date"),
```

Change the two date filter clauses:
```python
    if date_from is not None:
        stmt = stmt.where(LogEntry.work_date >= date_from)
        count_stmt = count_stmt.where(LogEntry.work_date >= date_from)
    if date_to is not None:
        stmt = stmt.where(LogEntry.work_date <= date_to)
        count_stmt = count_stmt.where(LogEntry.work_date <= date_to)
```

- [ ] **Step 3: Fix create_log_entry (line ~229)**

Change:
```python
    entry = LogEntry(
        volunteer_id=payload.volunteer_id,
        entry_date=payload.entry_date,
        activity_description=payload.activity_description,
        hours=payload.hours,
        location=payload.location,
        raw_transcript=payload.raw_transcript,
        status=payload.status,
    )
```
To:
```python
    entry = LogEntry(
        volunteer_id=payload.volunteer_id,
        work_date=payload.work_date,
        activity_description=payload.activity_description,
        hours=payload.hours,
        location=payload.location,
        raw_transcript=payload.raw_transcript,
        status=payload.status,
    )
```

- [ ] **Step 4: Add work_date to update_log_entry**

In `update_log_entry`, update the docstring and add the `work_date` handler after the `location` block:

```python
async def update_log_entry(
    entry_id: uuid.UUID,
    payload: LogEntryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Update activity_description, hours, location, and/or work_date. Blocked once approved."""
    ...
    if payload.activity_description is not None:
        entry.activity_description = payload.activity_description
    if payload.hours is not None:
        entry.hours = payload.hours
    # location is nullable, so model_fields_set distinguishes "not sent" from "explicitly cleared to null"
    if 'location' in payload.model_fields_set:
        entry.location = payload.location
    if payload.work_date is not None:
        entry.work_date = payload.work_date
    await db.commit()
    ...
```

- [ ] **Step 5: Verify with curl**

```bash
# List entries — should return work_date field, not entry_date
curl -s -u admin:$MANAGER_PASSWORD http://localhost:8100/log-entries?limit=1 | python -m json.tool | grep work_date
```

Expected: `"work_date": "YYYY-MM-DD"` appears in output.

- [ ] **Step 6: Commit**

```bash
git add api/routers/log_entries.py
git commit -m "feat: update log_entries router for work_date rename and editable work_date"
```

---

## Task 4: Remaining Backend Files

**Files:**
- Modify: `api/routers/reports.py`
- Modify: `api/routers/analytics.py`
- Modify: `api/routers/volunteers.py`
- Modify: `api/services/report_pdf.py`

All changes in this task are pure renames — `entry_date` → `work_date`. No logic changes.

- [ ] **Step 1: Update api/routers/reports.py**

There are 6 occurrences of `LogEntry.entry_date`. Replace all:
```
LogEntry.entry_date  →  LogEntry.work_date
```
Also one `.order_by(LogEntry.entry_date)`:
```python
.order_by(LogEntry.work_date)
```

- [ ] **Step 2: Update api/routers/analytics.py**

There are 8 occurrences of `LogEntry.entry_date`. Replace all:
```
LogEntry.entry_date  →  LogEntry.work_date
```
Also two direct date comparisons at the bottom:
```python
LogEntry.work_date >= date(first_y, first_m, 1),
LogEntry.work_date <= date(y, m, last_day),
```

- [ ] **Step 3: Update api/routers/volunteers.py**

Three occurrences. The sort key lambda and two filter comparisons:
```python
volunteer.log_entries.sort(key=lambda e: e.work_date, reverse=True)
...
and e.work_date.year == today.year
and e.work_date.month == today.month
...
LogEntry.work_date >= first_day,
LogEntry.work_date <= last_day,
```

- [ ] **Step 4: Update api/services/report_pdf.py**

One occurrence in the table row builder:
```python
f"<td class='num'>{_fmt_date(e.work_date)}</td>"
```

- [ ] **Step 5: Rebuild and verify**

```bash
docker compose up -d --build api
docker compose logs api --tail=20
```

Expected: clean startup, no `AttributeError: 'LogEntry' object has no attribute 'entry_date'`.

- [ ] **Step 6: Commit**

```bash
git add api/routers/reports.py api/routers/analytics.py api/routers/volunteers.py api/services/report_pdf.py
git commit -m "feat: rename entry_date to work_date in reports, analytics, volunteers, pdf service"
```

---

## Task 5: Frontend — Renames + Two-Column Date Lists

**Files:**
- Modify: `frontend/js/volunteers.js`

This task updates all `entry_date` references in the JS and adds the second date column to both list views.

- [ ] **Step 1: Update sort_by defaults (3 places)**

Line ~236 in `approvalsState`:
```javascript
filter: { status: 'pending_manager', search_q: '', date_from: null, date_to: null, sort_by: 'work_date', sort_dir: 'desc', offset: 0, limit: 20 },
```

Line ~244 in `volunteerLogState`:
```javascript
filter: { status: '', search_q: '', date_from: null, date_to: null, sort_by: 'work_date', sort_dir: 'desc', offset: 0, limit: 20 },
```

Line ~691 inside `renderDetail` (filter reset):
```javascript
volunteerLogState.filter = { status: '', search_q: '', date_from: null, date_to: null, sort_by: 'work_date', sort_dir: 'desc', offset: 0, limit: 20 };
```

- [ ] **Step 2: Update approvals thead — two date columns**

Replace `renderApprovalsThead()`:
```javascript
function renderApprovalsThead() {
  return `
    ${approvalsSortTh('Dan opravljenega dela', 'work_date')}
    <th>Prostovoljec</th>
    ${approvalsSortTh('Opis dela', 'activity_description')}
    ${approvalsSortTh('Ure', 'hours')}
    ${approvalsSortTh('Lokacija', 'location')}
    ${approvalsSortTh('Dan vnosa', 'created_at')}
    <th>Status</th>
    <th>Dejanja</th>
  `;
}
```

- [ ] **Step 3: Update approvals table row — add created_at cell, fix colspan**

In `renderApprovalsTable`, change the row template:
```javascript
    return `
      <tr data-id="${e.id}" style="cursor:pointer">
        <td>${esc(e.work_date)}</td>
        <td data-stop><a href="#approvals/volunteer/${e.volunteer_id}" style="color:var(--accent);text-decoration:none">${esc(name)}</a></td>
        <td>${desc}</td>
        <td style="text-align:right">${fmtHours(e.hours)}</td>
        <td>${e.location ? esc(e.location) : '—'}</td>
        <td>${e.created_at.slice(0, 10)}</td>
        <td>${statusBadge(e.status)}</td>
        <td class="td-actions" data-stop>${actions}</td>
      </tr>`;
```

Fix the empty-row colspan:
```javascript
    setHtml(tbody, `<tr class="empty-row"><td colspan="8">${msg}</td></tr>`);
```

Also fix the loading row colspan in the HTML template in `renderDetail` — search for:
```javascript
<tbody id="vlog-body"><tr class="loading-row"><td colspan="5">Nalaganje…</td></tr></tbody>
```
(this belongs to the volunteer log table, not approvals — handle in Step 5 below)

- [ ] **Step 4: Update approvals loading row colspan in approvals HTML**

Search for the approvals table loading row in the approvals page HTML template and update `colspan="7"` to `colspan="8"`. (If no loading row exists in the approvals HTML template, skip this step.)

- [ ] **Step 5: Update volunteer log thead — two date columns**

Replace `renderVolunteerLogThead()`:
```javascript
function renderVolunteerLogThead() {
  return `
    ${volLogSortTh('Dan opravljenega dela', 'work_date')}
    ${volLogSortTh('Opis dela', 'activity_description')}
    ${volLogSortTh('Ure', 'hours')}
    ${volLogSortTh('Lokacija', 'location')}
    ${volLogSortTh('Dan vnosa', 'created_at')}
    <th>Status</th>
  `;
}
```

- [ ] **Step 6: Update volunteer log table row — add created_at cell, fix colspan**

In `renderVolunteerLogTable`, change the row template:
```javascript
    return `
      <tr data-id="${e.id}" style="cursor:pointer">
        <td>${esc(e.work_date)}</td>
        <td>${desc}</td>
        <td style="text-align:right">${fmtHours(e.hours)}</td>
        <td>${e.location ? esc(e.location) : '—'}</td>
        <td>${e.created_at.slice(0, 10)}</td>
        <td>${statusBadge(e.status)}</td>
      </tr>`;
```

Fix the empty-row colspan:
```javascript
    setHtml(tbody, `<tr class="empty-row"><td colspan="6">Ni vnosov, ki ustrezajo filtru.</td></tr>`);
```

Fix the loading row colspan in `renderDetail` (around line ~790):
```javascript
<tbody id="vlog-body"><tr class="loading-row"><td colspan="6">Nalaganje…</td></tr></tbody>
```

- [ ] **Step 7: Update entry detail header display (line ~1611)**

Change:
```javascript
        <div class="detail-name">${esc(entry.entry_date)}</div>
```
To:
```javascript
        <div class="detail-name">${esc(entry.work_date)}</div>
```

- [ ] **Step 8: Verify in browser**

Open `http://localhost:80`, log in, navigate to Approvals. Confirm:
- Two date columns appear: "Dan opravljenega dela" and "Dan vnosa", both sortable.
- Clicking each header sorts the table.
- Navigate to a volunteer's log — same two columns appear there.

- [ ] **Step 9: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: rename entry_date to work_date in frontend, add two-column date display to lists"
```

---

## Task 6: Frontend — work_date in Entry Edit Form

**Files:**
- Modify: `frontend/js/volunteers.js`

- [ ] **Step 1: Add work_date input to the edit form**

In `renderLogEntryDetail`, inside the `${editable ? \`...\` : ''}` block, add a date field after the hours field and before the location field:

```javascript
      ${editable ? `
      <p class="section-title">Uredi vnos</p>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem">
        <div class="field">
          <label>Opis dela</label>
          <textarea id="d-desc" rows="4" style="width:100%;resize:vertical">${esc(entry.activity_description)}</textarea>
        </div>
        <div class="field" style="max-width:160px">
          <label>Ure</label>
          <input type="number" id="d-hours" value="${entry.hours}" min="0.5" max="24" step="0.5" />
        </div>
        <div class="field" style="max-width:200px">
          <label>Dan opravljenega dela</label>
          <input type="date" id="d-work-date" value="${entry.work_date}" />
        </div>
        <div class="field">
          <label>Lokacija</label>
          <input type="text" id="d-location" value="${esc(entry.location || '')}" placeholder="Npr. Dom starejših Trnovo" />
        </div>
        <div id="d-edit-error" class="form-error" hidden></div>
        <div class="form-actions">
          <button class="btn btn-primary btn-sm" id="d-save-btn">Shrani spremembe</button>
        </div>
      </div>
    ` : ''}
```

- [ ] **Step 2: Read and include work_date in the save handler**

In the `$('d-save-btn').addEventListener` block, add work_date reading and validation, and include it in the update call:

```javascript
  if (editable) {
    $('d-save-btn').addEventListener('click', async () => {
      const desc     = $('d-desc').value.trim();
      const hours    = parseFloat($('d-hours').value);
      const workDate = $('d-work-date').value;
      const errEl    = $('d-edit-error');
      if (!desc) {
        errEl.textContent = 'Opis dela ne sme biti prazen.';
        errEl.hidden = false;
        return;
      }
      if (isNaN(hours) || hours < 0.5 || hours > 24) {
        errEl.textContent = 'Ure morajo biti med 0.5 in 24.';
        errEl.hidden = false;
        return;
      }
      if (!workDate) {
        errEl.textContent = 'Dan opravljenega dela je obvezen.';
        errEl.hidden = false;
        return;
      }
      errEl.hidden = true;
      $('d-save-btn').disabled = true;
      $('d-save-btn').textContent = 'Shranjevanje…';
      const location = $('d-location').value.trim() || null;
      try {
        await API.logEntries.update(entry.id, { activity_description: desc, hours, location, work_date: workDate });
        toast('Vnos posodobljen.');
        await renderLogEntryDetail(id, { backHash, backLabel, backNav, goBack });
      } catch (err) {
        errEl.textContent = err.message;
        errEl.hidden = false;
        $('d-save-btn').disabled = false;
        $('d-save-btn').textContent = 'Shrani spremembe';
      }
    });
  }
```

- [ ] **Step 3: Verify in browser**

Open a pending entry detail page. Confirm:
- "Dan opravljenega dela" date input appears in the edit form, pre-filled with the entry's work_date.
- Change the date, click "Shrani spremembe" — page re-renders with the new date in the header and in the edit form.
- The detail-header at the top shows the updated work_date.

- [ ] **Step 4: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: add work_date field to entry detail edit form"
```

---

## Task 7: Frontend — "Dodaj vnos" on Volunteer Detail Page

**Files:**
- Modify: `frontend/js/volunteers.js`

- [ ] **Step 1: Add "Dodaj vnos" button to the volunteer detail page**

In `renderDetail`, find the `<p class="section-title">Dnevnik dela</p>` line (around line ~767) and add a button row right after it:

```javascript
      <p class="section-title">Dnevnik dela</p>
      <div style="margin-bottom:1rem">
        <button class="btn btn-primary btn-sm" id="add-entry-btn">+ Dodaj vnos</button>
      </div>
```

- [ ] **Step 2: Wire up the button to open a modal form**

After the back-btn event listener (around line ~803), add:

```javascript
    $('add-entry-btn').addEventListener('click', () => {
      const today = new Date().toISOString().slice(0, 10);
      openModal('Nov vnos', `
        <form id="add-entry-form" novalidate>
          <div class="field" style="max-width:200px">
            <label>Dan opravljenega dela *</label>
            <input type="date" id="ae-work-date" value="${today}" required />
          </div>
          <div class="field" style="max-width:160px">
            <label>Ure *</label>
            <input type="number" id="ae-hours" min="0.5" max="24" step="0.5" placeholder="npr. 4" required />
          </div>
          <div class="field">
            <label>Opis dela *</label>
            <textarea id="ae-desc" rows="4" style="width:100%;resize:vertical" required></textarea>
          </div>
          <div class="field">
            <label>Lokacija</label>
            <input type="text" id="ae-location" placeholder="Npr. Dom starejših Trnovo" />
          </div>
          <div id="ae-error" class="form-error" hidden></div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" id="ae-submit">Shrani vnos</button>
          </div>
        </form>
      `);

      $('add-entry-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const workDate = $('ae-work-date').value;
        const hours    = parseFloat($('ae-hours').value);
        const desc     = $('ae-desc').value.trim();
        const location = $('ae-location').value.trim() || null;
        const errEl    = $('ae-error');

        if (!workDate) {
          errEl.textContent = 'Dan opravljenega dela je obvezen.';
          errEl.hidden = false;
          return;
        }
        if (isNaN(hours) || hours < 0.5 || hours > 24) {
          errEl.textContent = 'Ure morajo biti med 0.5 in 24.';
          errEl.hidden = false;
          return;
        }
        if (!desc) {
          errEl.textContent = 'Opis dela ne sme biti prazen.';
          errEl.hidden = false;
          return;
        }

        errEl.hidden = true;
        $('ae-submit').disabled = true;
        $('ae-submit').textContent = 'Shranjevanje…';

        try {
          const entry = await API.logEntries.create({
            volunteer_id: id,
            work_date:    workDate,
            hours,
            activity_description: desc,
            location,
          });
          closeModal();
          toast('Vnos ustvarjen.');
          history.pushState(null, '', `#volunteers/${id}/log/${entry.id}`);
          renderLogEntryDetail(entry.id, {
            backHash:  `#volunteers/${id}`,
            backLabel: '← Nazaj na prostovoljca',
            backNav:   'volunteers',
            goBack:    () => renderDetail(id),
          });
        } catch (err) {
          errEl.textContent = err.message;
          errEl.hidden = false;
          $('ae-submit').disabled = false;
          $('ae-submit').textContent = 'Shrani vnos';
        }
      });
    });
```

- [ ] **Step 3: Add API.logEntries.create to the API client**

Find `API.logEntries` in `volunteers.js` (the object with `.list`, `.get`, `.update`, etc.) and add a `create` method:

```javascript
    create: (payload) => apiFetch('/log-entries', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
```

- [ ] **Step 4: Verify in browser**

Open a volunteer detail page. Confirm:
- "+ Dodaj vnos" button appears below the "Dnevnik dela" heading.
- Click it — modal opens with the form fields; date defaults to today.
- Fill in all required fields, submit — modal closes, page navigates to the new entry detail.
- The new entry appears in the volunteer's log list with status "Čaka odobritev".
- Submitting with missing required fields shows the appropriate error message.

- [ ] **Step 5: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: add 'Dodaj vnos' button and form to volunteer detail page"
```

---

## Task 8: n8n Workflows

Both `volunteer_entry` and `manager_approval` workflows reference `entry_date` in Set nodes and WhatsApp message templates.

- [ ] **Step 1: List active workflows and get their IDs**

Use n8n-mcp:
```
n8n_list_workflows
```

Note the IDs for `volunteer_entry` and `manager_approval`.

- [ ] **Step 2: Fetch and update volunteer_entry workflow**

```
n8n_get_workflow(id="<volunteer_entry_id>")
```

Search the returned JSON for all occurrences of `entry_date`. Replace each with `work_date`. Common locations:
- Set node field mappings like `{{ $json.entry_date }}` → `{{ $json.work_date }}`
- WhatsApp message text like `entry_date` literal → `work_date`
- HTTP Request node body fields named `entry_date` → `work_date`

Then update:
```
n8n_update_full_workflow(id="<volunteer_entry_id>", workflow=<updated_json>)
```

- [ ] **Step 3: Fetch and update manager_approval workflow**

```
n8n_get_workflow(id="<manager_approval_id>")
```

Same process — find all `entry_date` references, replace with `work_date`, then:
```
n8n_update_full_workflow(id="<manager_approval_id>", workflow=<updated_json>)
```

- [ ] **Step 4: Validate both workflows**

```
n8n_validate_workflow(id="<volunteer_entry_id>")
n8n_validate_workflow(id="<manager_approval_id>")
```

Both should return no errors.

- [ ] **Step 5: Export updated workflow JSONs**

```
n8n_get_workflow(id="<volunteer_entry_id>")  → save to n8n/workflows/volunteer_entry.json
n8n_get_workflow(id="<manager_approval_id>") → save to n8n/workflows/manager_approval.json
```

- [ ] **Step 6: Commit**

```bash
git add n8n/workflows/volunteer_entry.json n8n/workflows/manager_approval.json
git commit -m "feat: update n8n workflows for work_date rename"
```

---

## Task 9: Scripts and Docs

**Files:**
- Modify: `scripts/list_pending_entries.py`
- Modify: `db/init.sql`

- [ ] **Step 1: Update list_pending_entries.py**

Find the `entry_date` reference in the file and rename it to `work_date`. The file prints entry fields; it likely has something like `entry['entry_date']` or `e.entry_date` — replace with `work_date`.

Run the script to verify it still works:
```powershell
. .\scripts\load_env.ps1
python scripts\list_pending_entries.py
```

Expected: output shows `work_date` in the field names, no `KeyError` or `AttributeError`.

- [ ] **Step 2: Update db/init.sql**

In `db/init.sql`, rename the column definition from `entry_date` to `work_date` so that fresh deployments use the correct name from the start:

```sql
    entry_date              DATE            NOT NULL,   -- Date of the work, not submission date
```
→
```sql
    work_date               DATE            NOT NULL,   -- Date the work was performed, not submission date
```

Update the column comment below the table:
```sql
COMMENT ON COLUMN log_entries.entry_date IS 'The date work was performed, not when it was submitted.';
```
→
```sql
COMMENT ON COLUMN log_entries.work_date IS 'The date work was performed, not when it was submitted.';
```

Also update the index names in `init.sql`:
```sql
CREATE INDEX idx_entries_date     ON log_entries(entry_date);
CREATE INDEX idx_entries_vol_date ON log_entries(volunteer_id, entry_date);
```
→
```sql
CREATE INDEX idx_entries_work_date     ON log_entries(work_date);
CREATE INDEX idx_entries_vol_work_date ON log_entries(volunteer_id, work_date);
```

- [ ] **Step 3: Update SPEC.md**

Search SPEC.md for `entry_date` and replace all occurrences with `work_date`. Also update any human-readable descriptions that say "entry date" to say "work date" or "dan opravljenega dela".

```bash
grep -n "entry_date" SPEC.md
```

Make the replacements, then verify:

```bash
grep "entry_date" SPEC.md
```

Expected: no output (all replaced).

- [ ] **Step 4: Commit**

```bash
git add scripts/list_pending_entries.py db/init.sql SPEC.md
git commit -m "feat: rename entry_date to work_date in scripts, init.sql, and SPEC"
```

---

## Task 10: Run graphify update

After all code changes are committed, update the knowledge graph.

- [ ] **Step 1: Run graphify**

```bash
graphify update .
```

- [ ] **Step 2: Commit the updated graph**

```bash
git add graphify-out/
git commit -m "chore: update graphify knowledge graph after work_date rename"
```
