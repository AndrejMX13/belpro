# Work Date Rename + Dashboard Entry Creation Design

## Goal

Rename `entry_date` → `work_date` throughout the stack to clearly separate "when work was performed" from "when the entry was submitted" (`created_at`). Expose `work_date` as an editable field in the entry detail form. Add the ability to create new log entries from the manager dashboard (from the volunteer detail page).

## Architecture

Three concerns addressed together because the rename is a prerequisite for the other two:
1. **Rename** — Alembic migration + all code and workflow references.
2. **Edit `work_date`** — Add to `LogEntryUpdate` schema and the entry detail edit form.
3. **Create entries from dashboard** — "Dodaj vnos" button on volunteer detail page, pre-fills `volunteer_id`.

## Tech Stack

FastAPI (Python), SQLAlchemy 2.x + Alembic, PostgreSQL, vanilla JS frontend, n8n workflows (updated via n8n-mcp tools).

---

## Data Layer

### Migration

New Alembic migration (`002_rename_entry_date_to_work_date.py`):

```sql
ALTER TABLE log_entries RENAME COLUMN entry_date TO work_date;
ALTER INDEX idx_entries_date RENAME TO idx_entries_work_date;
```

PostgreSQL's `RENAME COLUMN` automatically updates column references inside all index definitions, so `idx_entries_vol_date` needs only a name update for clarity:

```sql
ALTER INDEX idx_entries_vol_date RENAME TO idx_entries_vol_work_date;
```

### ORM model (`api/models/log_entry.py`)

Rename field `entry_date` → `work_date`. No type or nullability change.

### Schemas (`api/schemas/log_entry.py`)

- `LogEntryCreate`: rename field `entry_date` → `work_date`.
- `LogEntryResponse`: rename field `entry_date` → `work_date`.
- `LogEntryUpdate`: add `work_date: date | None = None`. `None` means "not provided" (safe — `work_date` is NOT NULL in the DB, so `None` unambiguously means omitted).

---

## API Layer

### Router: `api/routers/log_entries.py`

- `sort_by` Literal: `"entry_date"` → `"work_date"`.
- `date_from` / `date_to` filter clauses: `LogEntry.entry_date` → `LogEntry.work_date`. Filtering by work date range is the correct semantic (used for monthly report compliance periods).
- `update_log_entry`: add handling for `work_date` — same guard as other fields (blocked if `entry.status == EntryStatus.APPROVED`):
  ```python
  if payload.work_date is not None:
      entry.work_date = payload.work_date
  ```
- `create_log_entry`: rename `entry_date=payload.entry_date` → `work_date=payload.work_date`.
- Manager approval notification message: rename field reference.

### Other routers

- `api/routers/reports.py` — rename field references.
- `api/routers/analytics.py` — rename field references.
- `api/routers/volunteers.py` — rename field references.
- `api/services/report_pdf.py` — rename field references.

---

## Frontend (`frontend/js/volunteers.js`)

### Global renames

All occurrences of `entry_date` → `work_date` in:
- `approvalsState.filter.sort_by` default value
- `volunteerLogState.filter.sort_by` default value (and reset in `renderDetail`)
- All `e.entry_date` / `entry.entry_date` display references

### List views — two date columns

Both the approvals list and the volunteer log list gain a second date column.

**Approvals thead** (8 columns total):
```
Dan opravljenega dela | Prostovoljec | Opis dela | Ure | Lokacija | Dan vnosa | Status | Dejanja
```

**Volunteer log thead** (6 columns total):
```
Dan opravljenega dela | Opis dela | Ure | Lokacija | Dan vnosa | Status
```

Both "Dan opravljenega dela" (`work_date`) and "Dan vnosa" (`created_at`) are sortable via the existing `approvalsSortTh` / `volLogSortTh` helpers.

`created_at` is a full ISO timestamp in API responses; display the date part only: `e.created_at.slice(0, 10)`.

The `colspan` values on empty-row `<td>` elements must be updated to match the new column counts (approvals: 8, volunteer log: 6).

### Entry detail edit form (`renderLogEntryDetail`)

Add a date input for `work_date` in the edit form, between the existing header info and the activity description field:

```html
<div class="field">
  <label>Dan opravljenega dela</label>
  <input type="date" id="d-work-date" value="${entry.work_date}" />
</div>
```

In the save handler, read the value and include it in the update payload:
```javascript
const workDate = $('d-work-date').value || null;
await API.logEntries.update(entry.id, { activity_description: desc, hours, location, work_date: workDate });
```

The edit form is already hidden for `approved` entries — no additional guard needed in the frontend.

### "Dodaj vnos" button (volunteer detail page)

Add a "Dodaj vnos" button next to the existing volunteer edit button in the volunteer detail page header.

Clicking it opens the standard modal with this form:

| Field | Input type | Default | Required |
|-------|-----------|---------|----------|
| Dan opravljenega dela | `<input type="date">` | today (`new Date().toISOString().slice(0,10)`) | yes |
| Ure | `<input type="number" step="0.5" min="0.5" max="24">` | — | yes |
| Opis dela | `<textarea>` | — | yes |
| Lokacija | `<input type="text">` | — | no |

`volunteer_id` comes from the current page context — no selector.

On submit: `POST /log-entries` with `status: "pending_manager"` (default in `LogEntryCreate`).

On success: close modal, navigate to the new entry's detail page (`#volunteers/{volunteerId}/log/{newEntryId}`).

On error: display error message inside the form, keep modal open.

---

## n8n Workflows

Both `n8n/workflows/volunteer_entry.json` and `n8n/workflows/manager_approval.json` reference `entry_date` in Set nodes and message templates. All references must be updated to `work_date` using n8n-mcp tools (`n8n_get_workflow` → `n8n_update_full_workflow`). Never edit workflow JSON by hand.

---

## Scripts and Docs

- `scripts/list_pending_entries.py`: rename `entry_date` → `work_date` in output formatting.
- `SPEC.md`: update field name references.
- `db/init.sql`: update the comment on the column (schema itself is managed by migrations after first run).

---

## Business Rules (unchanged)

- `work_date` is editable only while entry is `pending_volunteer` or `pending_manager`. Blocked once `approved`.
- New entries created from the dashboard start as `pending_manager`.
- `date_from` / `date_to` API filters apply to `work_date` (not `created_at`).
- `created_at` and `updated_at` are always system-managed; never user-editable.
