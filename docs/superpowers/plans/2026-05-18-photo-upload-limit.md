# Photo Upload Limit (ISS-002) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent volunteers from attaching more than `MAX_PHOTOS_PER_ENTRY` photos to a single log entry via WhatsApp; the manager dashboard is not subject to this limit.

**Architecture:** `MAX_PHOTOS_PER_ENTRY=5` lives in `.env`. FastAPI reads it via `Settings` and exposes it at `GET /api/log-entries/photo-limit`. The n8n volunteer_entry workflow fetches this limit before each photo upload; if the entry is already at the limit the photo is rejected (not uploaded) and the volunteer receives a Slovenian message explaining the situation. No API-level enforcement — the check is entirely in n8n, so the manager dashboard is unaffected.

**Tech Stack:** Python 3.11 / FastAPI / pydantic-settings, n8n workflow JSON via n8n-mcp, Docker Compose

---

## File Map

| File | Change |
|------|--------|
| `.env.example` | Add `MAX_PHOTOS_PER_ENTRY=5` with English comment |
| `.env.example.sl` | Add `MAX_PHOTOS_PER_ENTRY=5` with Slovenian comment |
| `api/core/settings.py` | Add `max_photos_per_entry: int = 5` field |
| `api/routers/log_entries.py` | Add `GET /api/log-entries/photo-limit` endpoint |
| `api/tests/test_log_entries.py` | Add test for the new endpoint |
| `n8n/workflows/volunteer_entry.json` | Add limit-check nodes in photo sub-flow (via n8n-mcp + export) |

---

## Task 1: Add MAX_PHOTOS_PER_ENTRY to both env example files

**Files:**
- Modify: `.env.example`
- Modify: `.env.example.sl`

- [ ] **Step 1: Edit .env.example**

Find the `# Faster-Whisper` section (around line 83). Insert a new section immediately above it:

```
# -----------------------------------------------------------------------------
# Uploads
# MAX_PHOTOS_PER_ENTRY: maximum photos a volunteer may attach to one log entry.
# The bot rejects any photo that would push the count above this limit.
# The manager dashboard is not subject to this limit.
# -----------------------------------------------------------------------------
MAX_PHOTOS_PER_ENTRY=5
```

- [ ] **Step 2: Edit .env.example.sl**

Find the equivalent Whisper section in `.env.example.sl`. Insert immediately above it:

```
# -----------------------------------------------------------------------------
# Nalaganje datotek
# MAX_PHOTOS_PER_ENTRY: največ slik, ki jih prostovoljec lahko priloži enemu vnosu.
# Bot zavrne vsako sliko, ki bi presegla to mejo.
# Upravljalska nadzorna plošča te omejitve ne upošteva.
# -----------------------------------------------------------------------------
MAX_PHOTOS_PER_ENTRY=5
```

- [ ] **Step 3: Commit**

```bash
git add .env.example .env.example.sl
git commit -m "config: add MAX_PHOTOS_PER_ENTRY env variable (default 5)"
```

---

## Task 2: Settings field + photo-limit API endpoint

**Files:**
- Modify: `api/core/settings.py`
- Modify: `api/routers/log_entries.py` (add before the `/{entry_id}` route to avoid shadowing)
- Modify: `api/tests/test_log_entries.py`

- [ ] **Step 1: Write the failing test**

Add to the end of `api/tests/test_log_entries.py`:

```python
async def test_photo_limit_returns_default(client: AsyncClient) -> None:
    r = await client.get("/api/log-entries/photo-limit")
    assert r.status_code == 200
    assert r.json() == {"max_photos": 5}
```

Note: no `auth` header — this endpoint is open (used by internal n8n calls).

- [ ] **Step 2: Run the test to verify it fails**

```bash
docker compose exec -T api pytest tests/test_log_entries.py::test_photo_limit_returns_default -v
```

Expected: FAIL — 404 Not Found (endpoint doesn't exist yet).

- [ ] **Step 3: Add the setting to Settings**

In `api/core/settings.py`, add after the `ngo_whatsapp_phone` field:

```python
    # ── Uploads ───────────────────────────────────────────────────────────────
    max_photos_per_entry: int = 5
```

- [ ] **Step 4: Add the endpoint to the router**

In `api/routers/log_entries.py`, find the `list_log_entries` endpoint (the one at `@router.get("")`). Add the new endpoint immediately after it and before the `@router.get("/{entry_id}")` route — static paths must come before parameterised ones or FastAPI will route `/photo-limit` as an entry ID:

```python
@router.get("/photo-limit")
async def get_photo_limit() -> dict:
    """Return the configured maximum photos per log entry. Used by n8n workflows."""
    from core.settings import get_settings
    return {"max_photos": get_settings().max_photos_per_entry}
```

- [ ] **Step 5: Rebuild and run the test**

```bash
docker compose up -d --build api
docker compose exec -T api pytest tests/test_log_entries.py::test_photo_limit_returns_default -v
```

Expected: PASS.

- [ ] **Step 6: Run the full test suite**

```bash
docker compose exec -T api pytest tests/ -v --tb=short
```

Expected: all tests pass (130+ total, now 131).

- [ ] **Step 7: Commit**

```bash
git add api/core/settings.py api/routers/log_entries.py api/tests/test_log_entries.py
git commit -m "feat: expose photo limit at GET /api/log-entries/photo-limit"
```

---

## Task 3: n8n workflow — insert photo limit check

**Files:**
- Modify: `n8n/workflows/volunteer_entry.json` (via n8n-mcp, then exported with `scripts/n8n_workflows.py`)

### Context — existing photo sub-flow

When a volunteer sends an image while in `awaiting_photos` mode, the flow is:

```
[image arrives]
  → Code: Check Photo State       (outputs {phone, remoteJid, entry_id, messageKey, messageData, has_active_photo_state})
  → IF: Photo State               (id: if_photo_state) — branches on has_active_photo_state
    [true branch]
      → HTTP: GET Entry (Photo Count)  (id: http_get_entry_for_photos)
          GET http://api:8000/api/log-entries/{entry_id}/photos/base64
          Response has a `photos` array
      → HTTP: Fetch Image          ← CURRENT direct connection to remove
      → Code: Build Image Media Body
      → Code: Pripravi Upload Slike
      → HTTP: Upload Photo
      → Code: Slika Prejeta        (sends confirmation only if photo_count === 1)
      → HTTP: WA Slika Prejeta
```

### New flow after HTTP: GET Entry (Photo Count)

```
HTTP: GET Entry (Photo Count)
  → HTTP: GET Photo Limit          (new)
  → Code: Check Photo Limit        (new)
  → IF: Photo Limit Reached        (new)
      [true]  → Code: Limit Reject Message  (new)
               → HTTP: WA Photo Limit       (new, same pattern as HTTP: WA Slika Prejeta)
               → END
      [false] → HTTP: Fetch Image   (existing — restores the severed connection)
```

### Node specifications

**HTTP: GET Photo Limit**
- id: `http_get_photo_limit`
- type: `n8n-nodes-base.httpRequest`, typeVersion 4.2
- Method: GET
- URL: `http://api:8000/api/log-entries/photo-limit`
- No authentication, no headers

**Code: Check Photo Limit**
- id: `code_check_photo_limit`
- type: `n8n-nodes-base.code`, typeVersion 2
- Mode: `runOnceForAllItems`

```javascript
// Find the actual name of the node that checks photo state (it outputs
// {phone, remoteJid, has_active_photo_state, entry_id}) by reading the
// workflow JSON — look for the Code node just before IF: Photo State.
// Replace 'Code: Check Photo State' below with the real name if different.
const entryData = $('HTTP: GET Entry (Photo Count)').first().json;
const limitData = $('HTTP: GET Photo Limit').first().json;
const stateData = $('Code: Check Photo State').first().json;

const currentCount = (entryData.photos && entryData.photos.length)
  ? entryData.photos.length
  : 0;
const maxPhotos = limitData.max_photos || 5;

return [{
  json: {
    phone: stateData.phone,
    remoteJid: stateData.remoteJid,
    entry_id: stateData.entry_id,
    messageKey: stateData.messageKey,
    messageData: stateData.messageData,
    current_count: currentCount,
    max_photos: maxPhotos,
    at_limit: currentCount >= maxPhotos
  }
}];
```

**IF: Photo Limit Reached**
- id: `if_photo_limit`
- type: `n8n-nodes-base.if`, typeVersion 2
- Condition: `{{ $json.at_limit }}` equals `true` (boolean)
- Output 0 (true): limit hit — reject
- Output 1 (false): under limit — continue to upload

**Code: Limit Reject Message**
- id: `code_limit_reject_msg`
- type: `n8n-nodes-base.code`, typeVersion 2

```javascript
const d = $input.first().json;
const msg = `Vnos že vsebuje ${d.current_count} od ${d.max_photos} dovoljenih slik. `
  + `Nova slika ni bila dodana.\n\n1 - Potrdi vnos\n4 - Prekliči`;
return [{json: {phone: d.remoteJid, text: msg}}];
```

**HTTP: WA Photo Limit**
- id: `http_wa_photo_limit`
- Copy the full parameters block from `HTTP: WA Slika Prejeta` (same Evolution API send-text call) — it sends to `{{ $json.phone }}` with body `{{ $json.text }}`. Change only the node name and id.

### Steps

- [ ] **Step 1: Get the volunteer_entry workflow**

Use `mcp__n8n-mcp__n8n_list_workflows` to find the volunteer_entry workflow ID.
Use `mcp__n8n-mcp__n8n_get_workflow` with that ID to fetch the full JSON.

From the JSON, note:
- The exact name of the Code node that outputs `has_active_photo_state` (used in `Code: Check Photo Limit` above as `'Code: Check Photo State'`)
- The exact parameters of `HTTP: WA Slika Prejeta` (to copy for `HTTP: WA Photo Limit`)
- The x/y positions of nodes around `HTTP: GET Entry (Photo Count)` and `HTTP: Fetch Image` (to place new nodes sensibly)

- [ ] **Step 2: Add nodes and rewire using n8n-mcp**

Use `mcp__n8n-mcp__n8n_update_full_workflow` with the modified workflow JSON that:
1. Adds the four new nodes listed above to the `nodes` array
2. In `connections`, removes the existing link from `HTTP: GET Entry (Photo Count)` → `HTTP: Fetch Image`
3. Adds new links:
   - `HTTP: GET Entry (Photo Count)` → `HTTP: GET Photo Limit`
   - `HTTP: GET Photo Limit` → `Code: Check Photo Limit`
   - `Code: Check Photo Limit` → `IF: Photo Limit Reached`
   - `IF: Photo Limit Reached` output 0 (true) → `Code: Limit Reject Message`
   - `IF: Photo Limit Reached` output 1 (false) → `HTTP: Fetch Image`
   - `Code: Limit Reject Message` → `HTTP: WA Photo Limit`

- [ ] **Step 3: Verify in n8n UI**

Open http://localhost:5678, find volunteer_entry, confirm the new nodes are visible and wired correctly. The workflow should remain active (not deactivated by the update).

- [ ] **Step 4: Export the workflow**

```bash
python ./scripts/n8n_workflows.py export
```

Check that `n8n/workflows/volunteer_entry.json` has been updated (git diff should show the new nodes).

- [ ] **Step 5: Commit**

```bash
git add n8n/workflows/volunteer_entry.json
git commit -m "feat(n8n): reject volunteer photo uploads that exceed MAX_PHOTOS_PER_ENTRY"
```

---

## Self-review

**Spec coverage:**
- `MAX_PHOTOS_PER_ENTRY` in `.env` → Task 1 ✓
- Both `.env.example` files → Task 1 ✓
- API reads the env var → Task 2 (settings.py) ✓
- `GET /api/log-entries/photo-limit` endpoint → Task 2 ✓
- n8n enforces only on volunteer side → Task 3 ✓
- Manager bypass (no API enforcement) → by design — only n8n checks ✓
- Reject incoming photo, keep already-accepted photos → Task 3 (check before upload) ✓
- Volunteer informed of limit with current count → Task 3 (Slovenian message) ✓

**No placeholders:** All code is complete. The only open variable is the exact node name for `Code: Check Photo State` — the subagent resolves this by reading the live workflow in Step 1.
