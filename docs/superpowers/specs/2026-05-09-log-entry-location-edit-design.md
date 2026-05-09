# Design: Log Entry Location Edit + Auto-Refresh

**Date:** 2026-05-09  
**Status:** Approved

---

## Problem

The "Uredi vnos" (edit entry) section on the log entry detail page allows editing `activity_description` and `hours`, but not `location`. Whisper transcription and the n8n location extraction are imperfect — location frequently comes in null or incorrect. The manager has no way to fix it without direct database access.

Additionally, the current save handler manually patches individual DOM elements after save, which is fragile and must be extended for every new editable field.

---

## Solution

### 1. Add location field to the edit form

Add a free-text `<input>` for `location` to the "Uredi vnos" section, between the hours field and the save button. The field is optional — it may be left blank.

### 2. Include location in the save payload

Pass `location` (trimmed string, or `null` if blank) alongside `activity_description` and `hours` in the `API.logEntries.update()` call.

### 3. Replace inline DOM updates with full re-render

On successful save, call `renderLogEntryDetail(id, { backHash, backLabel, backNav, goBack })` instead of manually patching `d-desc-display` and `d-hours-display`. This re-fetches the entry from the API and re-renders the full detail view with fresh server data. The toast fires before the re-render so it remains visible.

### 4. API schema check

Verify that `PATCH /api/log-entries/{id}` accepts `location` as an updatable field. If not, add it to the Pydantic update schema.

---

## Scope

- `frontend/js/volunteers.js` — edit form HTML + save handler
- `api/schemas/log_entry.py` — update schema (if location not already included)

No migration needed. No new endpoints. No changes to n8n workflows.

---

## Out of Scope

- Adding `entry_date` as an editable field
- Editing approved entries
- Validation of location format
