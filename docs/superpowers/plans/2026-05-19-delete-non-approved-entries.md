# Delete Non-Approved Entries Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow the manager to delete log entries that are in `pending_volunteer` or `pending_manager` status, with cascading photo file cleanup and a frontend delete button with confirmation. `approved` and `rejected` entries are protected — they cannot be deleted.

**Architecture:** The existing `DELETE /api/log-entries/{id}` endpoint currently only allows `pending_volunteer` deletion — extend it to also allow `pending_manager`, and keep `approved` and `rejected` blocked (HTTP 409). Add disk photo cleanup before the DB delete (the ORM cascade handles DB records). Add `deleteEntry` to the frontend API client and a delete button to the entry detail view in `volunteers.js`.

**Tech Stack:** FastAPI, SQLAlchemy async, pytest-asyncio, vanilla JS

---

## File Map

| File | Change |
|------|--------|
| `api/routers/log_entries.py` | Extend `delete_log_entry` to allow `pending_manager` (keep `rejected` and `approved` blocked); add photo disk cleanup |
| `api/tests/test_log_entries.py` | Add tests for the newly allowed statuses and photo cleanup |
| `frontend/js/api.js` | Add `deleteEntry(id)` to `logEntries` object |
| `frontend/js/volunteers.js` | Add delete button to entry detail view, wired to `API.logEntries.deleteEntry` |

---

## Task 1: Extend the DELETE endpoint and clean up photo files

**Files:**
- Modify: `api/routers/log_entries.py:565-587`
- Test: `api/tests/test_log_entries.py`

### Context

The existing endpoint (line 565) rejects any status that is not `pending_volunteer`. The new rule: allow `pending_volunteer` and `pending_manager`; reject `approved` and `rejected` with HTTP 409. Additionally, photo files on disk are currently **not** deleted — only the DB records are removed via ORM cascade. This must be fixed.

The `LogEntry.photos` relationship uses `cascade="all, delete-orphan"` (see `api/models/log_entry.py:86`), so photo *DB rows* are automatically removed when the entry is deleted. Photo *files on disk* must be removed manually, following the same pattern as `delete_photo` (line 443: `(_PHOTOS_ROOT / photo.photo_path).unlink(missing_ok=True)`).

- [ ] **Step 1: Write the failing tests**

In `api/tests/test_log_entries.py`, add these three tests after the existing `test_delete_entry_wrong_status_returns_409`:

```python
@pytest.mark.asyncio
async def test_delete_pending_manager_entry_succeeds(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.PENDING_MANAGER)
    r = await client.delete(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 204
    r2 = await client.get(f"/api/log-entries/{e.id}", headers=auth)
    assert r2.status_code == 404


@pytest.mark.asyncio
async def test_delete_rejected_entry_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.REJECTED)
    r = await client.delete(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 409


@pytest.mark.asyncio
async def test_delete_approved_entry_returns_409(
    client: AsyncClient, auth: dict, volunteer_factory, log_entry_factory
) -> None:
    v = await volunteer_factory()
    e = await log_entry_factory(v.id, status=EntryStatus.APPROVED)
    r = await client.delete(f"/api/log-entries/{e.id}", headers=auth)
    assert r.status_code == 409
```

Note: `test_delete_entry_not_found` already exists — do not add it again. The existing `test_delete_entry_wrong_status_returns_409` tests `approved` → 409 and will still pass unchanged.

- [ ] **Step 2: Run tests to confirm the right ones fail**

```
docker compose exec api pytest tests/test_log_entries.py::test_delete_pending_manager_entry_succeeds tests/test_log_entries.py::test_delete_rejected_entry_returns_409 tests/test_log_entries.py::test_delete_approved_entry_returns_409 -v
```

Expected: `test_delete_pending_manager_entry_succeeds` FAIL (`assert 409 == 204`); the two `_returns_409` tests PASS (current code already blocks them).

- [ ] **Step 3: Update the endpoint**

In `api/routers/log_entries.py`, replace the `delete_log_entry` function (lines 565–587) entirely:

```python
@router.delete(
    "/{entry_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(require_manager)],
)
async def delete_log_entry(
    entry_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)] = ...,
) -> None:
    """Delete a pending_volunteer or pending_manager log entry and its associated photo files."""
    entry = (
        await db.execute(select(LogEntry).where(LogEntry.id == entry_id))
    ).scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Ne najdem dnevniškega zapisa")
    if entry.status not in (EntryStatus.PENDING_VOLUNTEER, EntryStatus.PENDING_MANAGER):
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=f"Vnosa v statusu '{entry.status.value}' ni mogoče izbrisati.",
        )

    photos = (
        await db.execute(select(LogEntryPhoto).where(LogEntryPhoto.log_entry_id == entry_id))
    ).scalars().all()
    for photo in photos:
        try:
            (_PHOTOS_ROOT / photo.photo_path).unlink(missing_ok=True)
        except Exception:
            pass
    try:
        (_PHOTOS_ROOT / str(entry_id)).rmdir()
    except Exception:
        pass

    await db.delete(entry)
    await db.commit()
```

- [ ] **Step 4: Run all new tests**

```
docker compose exec api pytest tests/test_log_entries.py::test_delete_pending_manager_entry_succeeds tests/test_log_entries.py::test_delete_rejected_entry_returns_409 tests/test_log_entries.py::test_delete_approved_entry_returns_409 -v
```

Expected: all three PASS.

- [ ] **Step 5: Run the full test suite to check for regressions**

```
docker compose exec api pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add api/routers/log_entries.py api/tests/test_log_entries.py
git commit -m "feat: allow deletion of pending_manager entries; keep rejected and approved protected"
```

---

## Task 2: Frontend — API client method and delete button

**Files:**
- Modify: `frontend/js/api.js:125-176`
- Modify: `frontend/js/volunteers.js` (around lines 1876–1912 and 2060–2094)

### Context

`api.js` has `approve` and `reject` in `logEntries` but no `deleteEntry`. The entry detail view in `volunteers.js` renders in `renderLogEntryDetail` (line 1858). The header already has conditional approve/reject buttons at lines 1907–1911. The delete button must appear only for `pending_volunteer` and `pending_manager`. `editable` (line 1876: `entry.status !== 'approved'`) is too broad — it also includes `rejected`. Introduce a new `canDelete` variable alongside the existing ones.

The `doAction` handler for approve/reject (lines 2060–2094) can be extended to handle `delete`. Alternatively add a separate event listener — a separate listener is cleaner since delete navigates away rather than re-rendering.

The `closeModal`/modal pattern from volunteer delete (line 1038–1051 in volunteers.js) is the reference for the confirmation flow — use `confirm()` for the prompt.

- [ ] **Step 1: Add `deleteEntry` to `api.js`**

In `frontend/js/api.js`, in the `logEntries` object (currently ending at line 175 with `reject`), add the new method:

```js
// Before the closing `},` of the logEntries object, add:
deleteEntry: (id) => request('/log-entries/' + id, { method: 'DELETE' }),
```

The full `logEntries` block after the change (lines 125–176 with addition):

```js
logEntries: {
  get:    (id)       => request('/log-entries/' + id),
  create: (payload)  => request('/log-entries', { method: 'POST', body: JSON.stringify(payload) }),
  update: (id, data) => request('/log-entries/' + id, { method: 'PATCH', body: JSON.stringify(data) }),

  uploadPhoto: (entryId, formData) => {
    /* ... unchanged ... */
  },

  photoUrl: async (entryId, photoId) => {
    /* ... unchanged ... */
  },

  deletePhoto: (entryId, photoId) =>
    request('/log-entries/' + entryId + '/photos/' + photoId, { method: 'DELETE' }),
  list: (params = {}) => {
    /* ... unchanged ... */
  },
  approve: (id) => request('/log-entries/' + id + '/approve', { method: 'PATCH' }),
  reject:  (id) => request('/log-entries/' + id + '/reject',  { method: 'PATCH' }),
  deleteEntry: (id) => request('/log-entries/' + id, { method: 'DELETE' }),
},
```

Only the last line is new — do not touch anything else in the block.

- [ ] **Step 2: Add `canDelete` and the delete button to the entry detail header in `volunteers.js`**

First, add `canDelete` alongside the existing `canApprove` declaration (line 1877). Current code:

```js
  const editable   = entry.status !== 'approved';
  const canApprove = entry.status === 'pending_manager';
```

Change to:

```js
  const editable   = entry.status !== 'approved';
  const canApprove = entry.status === 'pending_manager';
  const canDelete  = entry.status === 'pending_volunteer' || entry.status === 'pending_manager';
```

Then, in the `detail-header` HTML block (line 1907), replace the `${canApprove ? ...}` block with this expanded version:

```js
      ${canApprove ? `
        <div style="display:flex;gap:0.5rem;align-items:center">
          <button class="btn btn-primary btn-sm" id="approve-btn">Odobri</button>
          <button class="btn btn-danger btn-sm"  id="reject-btn">Zavrni</button>
          <button class="btn btn-danger btn-sm"  id="delete-entry-btn" style="margin-left:0.25rem">Izbriši</button>
        </div>` : canDelete ? `
        <div style="display:flex;gap:0.5rem;align-items:center">
          <button class="btn btn-danger btn-sm" id="delete-entry-btn">Izbriši</button>
        </div>` : ''}
```

When `canApprove` is true (`pending_manager`), the delete button appears alongside Odobri/Zavrni. When `canDelete` is true but `canApprove` is false (`pending_volunteer`), only the delete button appears. For `rejected` and `approved`, neither block renders.

- [ ] **Step 3: Wire the delete button event listener in `volunteers.js`**

The event listeners for approve/reject are registered near the end of `renderLogEntryDetail`, after `setHtml`. Locate the block around line 2093:

```js
    $('approve-btn').addEventListener('click', () => doAction('approve'));
    $('reject-btn').addEventListener('click',  () => doAction('reject'));
```

After those two lines (still inside the same `if` block, or right after it), add:

```js
    const delEntryBtn = $('delete-entry-btn');
    if (delEntryBtn) {
      delEntryBtn.addEventListener('click', async () => {
        if (!confirm('Trajno izbriši ta vnos?\n\nTega dejanja ni mogoče razveljaviti.')) return;
        delEntryBtn.disabled = true;
        delEntryBtn.textContent = 'Brisanje…';
        try {
          await API.logEntries.deleteEntry(entry.id);
          goBack ? goBack() : (window.location.hash = backHash);
        } catch (err) {
          alert('Napaka pri brisanju: ' + err.message);
          delEntryBtn.disabled = false;
          delEntryBtn.textContent = 'Izbriši';
        }
      });
    }
```

`goBack` and `backHash` are already in scope (they come from the function's options parameter).

- [ ] **Step 4: Manually test in the browser**

1. Open the dashboard at `http://localhost`.
2. Find a `pending_manager` entry in the Approvals list and open its detail page.
3. Confirm the "Izbriši" button appears next to Odobri/Zavrni.
4. Click "Izbriši", dismiss the confirmation with Cancel — verify nothing happens.
5. Click "Izbriši" again, confirm — verify the entry disappears and you are navigated back to the approvals list.
6. Find a `pending_volunteer` entry (filter: Vsi). Open it. Confirm the "Izbriši" button appears without Odobri/Zavrni.
7. Delete it — verify it disappears.
8. Find a `rejected` entry (filter: Vsi). Open it. Verify no "Izbriši" button appears.
9. Find an `approved` entry. Verify no "Izbriši" button appears.

- [ ] **Step 5: Commit**

```bash
git add frontend/js/api.js frontend/js/volunteers.js
git commit -m "feat: add delete button for non-approved log entries in entry detail view"
```
