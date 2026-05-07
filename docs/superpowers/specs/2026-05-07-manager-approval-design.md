# Manager WhatsApp Approval Workflow — Design Spec

**Date:** 2026-05-07
**Status:** Approved

## Problem

The volunteer entry flow works end-to-end: voice message → transcribe → extract → confirm → status = `pending_manager`. But there is no WhatsApp-based manager approval. The manager must use the web dashboard to approve/reject entries. We need the manager to receive a WhatsApp notification with entry details and be able to approve or reject by replying with a number.

Additionally, testing manager approval is blocked by only having 2 phone numbers (volunteer test + BelPro bot). We need a way to test without a third phone.

## Solution

Create a separate `manager_approval` workflow, called from the volunteer workflow via n8n Execute Workflow node. Add manager detection to the volunteer workflow's routing. Provide a Manual Trigger for testing without a phone.

## Architecture

### Routing Change (volunteer_entry.json)

```
Webhook: WhatsApp
       ↓
[NEW] HTTP: Lookup Manager   ← GET /api/managers/me (every call, no cache)
       ↓
Filter & Route               ← NEW: if sender == manager.phone → route = "manager"
       ↓
Razpotje (Switch)            ← NEW branch: "Upravljalec"
       ↓
[NEW] Code: Parse Manager Action
       ↓
[NEW] Execute Workflow       → calls manager_approval workflow
```

The manager phone is fetched fresh on every webhook call. No cache, no restart needed if the manager changes their number via the dashboard.

### Manager Workflow (manager_approval.json)

```
┌─ Manual Trigger ──────────────────────┐
│  Input: {entry_id, manager_phone,     │
│  manager_remoteJid, volunteer_name,   │
│  volunteer_remoteJid, entry_date,     │
│  hours, activity_description,         │
│  location, action}                    │
│                                       ↓
└─ Execute Workflow Trigger ──→ Code: Parse Action
                                      ↓
                              Switch: Action
                              ╱            ╲
                      "odobri"              "zavrni"
                         ↓                      ↓
              HTTP: PATCH /approve    HTTP: PATCH /reject
                         ↓                      ↓
                         └──────┬───────────────┘
                                ↓
                    Code: Build Volunteer Msg
                                ↓
                    HTTP: WA Notify Volunteer
                                ↓
                    Code: Build Manager Confirm
                                ↓
                    HTTP: WA Confirm to Manager
```

**~8 nodes.** Both triggers feed the same processing nodes.

### Manager → "Not Registered" Fix

Because the manager phone is checked BEFORE the volunteer lookup path in `Filter & Route`, manager messages are routed to the manager branch. They never reach `Prostovoljec Najden?` → `HTTP: WA Ni Registriran`. This naturally fixes the bug.

### Testing Without a Third Phone

The Manual Trigger accepts a JSON payload identical to what Execute Workflow would receive. To test:

1. Ensure a log entry with status `pending_manager` exists in the database
2. Open the manager workflow in n8n
3. Paste the test JSON into the Manual Trigger
4. Execute

No phone needed for this path.

## Data Flow

### Execute Workflow Input (from volunteer flow)

```json
{
  "entry_id": "uuid",
  "manager_phone": "38530369632",
  "manager_remoteJid": "38530369632@s.whatsapp.net",
  "volunteer_name": "Slavko Pridni",
  "volunteer_remoteJid": "38630369632@s.whatsapp.net",
  "entry_date": "07.05.2026",
  "hours": 3,
  "activity_description": "Okopavanje solate",
  "location": "Radece"
}
```

The manager replies to the notification with: `1` or `odobri` → approve, `2` or `zavrni` → reject.

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/managers/me` | GET | Lookup manager phone |
| `/api/log-entries/{id}/approve` | PATCH | Approve entry |
| `/api/log-entries/{id}/reject` | PATCH | Reject entry |

All require HTTP Basic Auth (manager password). Credential already exists in n8n as "BelPro API (Basic Auth)".

### WhatsApp Messages

**To volunteer (on approval):**
```
Vaš vnos z dne 07.05.2026 je bil odobren. ✅
📝 Okopavanje solate, 3 ur
```

**To volunteer (on rejection):**
```
Vaš vnos z dne 07.05.2026 je bil zavrnjen. ❌
Upravljalec vas bo kontaktiral za podrobnosti.
```

**To manager (confirmation):**
```
Vnos za Slavko Pridni je bil odobren/zavrnjen.
```

## Interaction Format

Both volunteer and manager use text replies with numbers (buttons attempted, blocked by Evolution API compatibility — see below).

- Volunteer: `1` = Potrdi, `2` = Popravi, `3` = Preklici
- Manager: `1` or `odobri` = Approve, `2` or `zavrni` = Reject

## Known Limitation: Buttons

WhatsApp interactive buttons were tested on 2026-05-07. The Evolution API `sendButtons` endpoint accepts requests but produces empty `quick_reply` buttons with no visible text. Root cause: n8n body serialization incompatibility with Evolution API v2.x button format. When a compatible approach is found, buttons should replace numbered text everywhere (volunteer confirmation + manager approval).

## Files Changed

| File | Change |
|------|--------|
| `n8n/workflows/volunteer_entry.json` | +4-5 nodes: Lookup Manager, manager branch in Filter & Route, new switch output, Parse Manager Action, Execute Workflow |
| `n8n/workflows/manager_approval.json` | New file: ~8 nodes |
