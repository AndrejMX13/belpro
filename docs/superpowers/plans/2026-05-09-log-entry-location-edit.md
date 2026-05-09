# Log Entry Location Edit + Auto-Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow the manager to add or fix the location field on a pending log entry, and re-render the full detail view after any save.

**Architecture:** Two-layer change — extend the Pydantic update schema and router to accept `location`, then add a location input to the frontend edit form and replace the fragile inline DOM update pattern with a full re-render call.

**Tech Stack:** FastAPI + Pydantic (API), vanilla JS (frontend)

---

## Files

- Modify: `api/schemas/log_entry.py` — add `location` to `LogEntryUpdate`
- Modify: `api/routers/log_entries.py` — apply location update in handler
- Modify: `frontend/js/volunteers.js` — add location input, update save handler

---

## Task 1: Extend the API update schema

**Files:**
- Modify: `api/schemas/log_entry.py:62-66`

- [ ] **Step 1: Add `location` to `LogEntryUpdate`**

In `api/schemas/log_entry.py`, add `location` as the last field of `LogEntryUpdate`:

```python
class LogEntryUpdate(BaseModel):
    """Editable fields — blocked once the entry is approved."""

    activity_description: Annotated[str, Field(min_length=1)] | None = None
    hours: Annotated[Decimal, Field(ge=Decimal("0.5"), le=Decimal("24.0"))] | None = None
    location: str | None = None
```

`None` means "not provided" for `activity_description` and `hours`. For `location` we need to distinguish "not provided" from "explicitly cleared to null" — the router handles this via `model_fields_set` (see Task 2).

- [ ] **Step 2: Commit**

```bash
git add api/schemas/log_entry.py
git commit -m "feat: add location to LogEntryUpdate schema"
```

---

## Task 2: Apply location update in the router

**Files:**
- Modify: `api/routers/log_entries.py:252-269`

- [ ] **Step 1: Update the handler**

In `api/routers/log_entries.py`, update `update_log_entry` to apply the location field and update the docstring:

```python
async def update_log_entry(
    entry_id: uuid.UUID,
    payload: LogEntryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> LogEntryResponse:
    """Update activity_description, hours, and/or location. Blocked once the entry is approved."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    if entry.status == EntryStatus.APPROVED:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Odobrenega vnosa ni mogoče urejati.",
        )
    if payload.activity_description is not None:
        entry.activity_description = payload.activity_description
    if payload.hours is not None:
        entry.hours = payload.hours
    if 'location' in payload.model_fields_set:
        entry.location = payload.location
    await db.commit()
    await db.refresh(entry)
    return LogEntryResponse.model_validate(entry)
```

The `model_fields_set` check means: if `location` was present in the request body (even as `null`), apply it. If the field was absent entirely, leave the existing value unchanged.

- [ ] **Step 2: Rebuild the API container and verify**

```bash
docker compose up -d --build api
```

Open `http://localhost:8100/docs`, find `PATCH /api/log-entries/{entry_id}`, and confirm the request body schema now shows `location`.

- [ ] **Step 3: Commit**

```bash
git add api/routers/log_entries.py
git commit -m "feat: apply location field in log entry update handler"
```

---

## Task 3: Add location field to the frontend edit form

**Files:**
- Modify: `frontend/js/volunteers.js` (edit form template inside `renderLogEntryDetail`)

- [ ] **Step 1: Add the location input**

In `frontend/js/volunteers.js`, inside `renderLogEntryDetail`, find the edit form template. Locate the hours field block and add the location field immediately after it, before the error div:

Replace:
```javascript
        <div class=\"field\" style=\"max-width:160px\">
          <label>Ure</label>
          <input type=\"number\" id=\"d-hours\" value=\"${entry.hours}\" min=\"0.5\" max=\"24\" step=\"0.5\" />
        </div>
        <div id=\"d-edit-error\" class=\"form-error\" hidden></div>
```

With:
```javascript
        <div class=\"field\" style=\"max-width:160px\">
          <label>Ure</label>
          <input type=\"number\" id=\"d-hours\" value=\"${entry.hours}\" min=\"0.5\" max=\"24\" step=\"0.5\" />
        </div>
        <div class=\"field\">
          <label>Lokacija</label>
          <input type=\"text\" id=\"d-location\" value=\"${esc(entry.location || '')}\" placeholder=\"Npr. Dom starejših Trnovo\" />
        </div>
        <div id=\"d-edit-error\" class=\"form-error\" hidden></div>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: add location input to log entry edit form"
```

---

## Task 4: Update the save handler

**Files:**
- Modify: `frontend/js/volunteers.js` (save handler inside `renderLogEntryDetail`)

- [ ] **Step 1: Replace the save handler body**

Find the `d-save-btn` click handler. Replace the entire `try` block (from `const updated = await ...` to the end of the try/catch, plus the two lines after it) with the new version that includes `location` in the payload and calls `renderLogEntryDetail` on success:

Replace:
```javascript
      try {
        const updated = await API.logEntries.update(entry.id, { activity_description: desc, hours });
        entry = updated;
        $('d-desc-display').textContent = updated.activity_description;
        $('d-hours-display').textContent = fmtHours(updated.hours);
        toast('Vnos posodobljen.');
      } catch (err) {
        errEl.textContent = err.message;
        errEl.hidden = false;
      }
      $('d-save-btn').disabled = false;
      $('d-save-btn').textContent = 'Shrani spremembe';
```

With:
```javascript
      const location = $('d-location').value.trim() || null;
      try {
        await API.logEntries.update(entry.id, { activity_description: desc, hours, location });
        toast('Vnos posodobljen.');
        await renderLogEntryDetail(id, { backHash, backLabel, backNav, goBack });
      } catch (err) {
        errEl.textContent = err.message;
        errEl.hidden = false;
        $('d-save-btn').disabled = false;
        $('d-save-btn').textContent = 'Shrani spremembe';
      }
```

Note: `$('d-save-btn').disabled = false` is only needed in the error branch — on success the whole page re-renders, so the old button element is gone.

- [ ] **Step 2: Manual verification**

1. Open `http://localhost:80` and navigate to a pending entry.
2. Edit the description, hours, and location fields, then click "Shrani spremembe".
3. Confirm the toast "Vnos posodobljen." appears and the detail view re-renders showing the updated values.
4. Clear the location field and save again — confirm location shows "—" in the info grid.
5. Edit only description (leave location unchanged) — confirm location is not cleared.

- [ ] **Step 3: Commit**

```bash
git add frontend/js/volunteers.js
git commit -m "feat: include location in save payload and re-render detail after save"
```
