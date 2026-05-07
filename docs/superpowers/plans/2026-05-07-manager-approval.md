# Manager WhatsApp Approval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add manager detection and routing to the volunteer_entry workflow, and create a new manager_approval workflow so managers can approve/reject entries via WhatsApp text replies.

**Architecture:** A new "HTTP: Pridobi Upravljalca" node is inserted between Webhook and Filter & Route to fetch the manager phone on every webhook call. Filter & Route detects manager messages and routes them to a new "Upravljalec" switch branch, which parses the reply and calls manager_approval via Execute Workflow. The manager_approval workflow handles both Execute Workflow Trigger (production) and Manual Trigger (testing), processes approve/reject actions, notifies the volunteer, and confirms to the manager.

**Tech Stack:** n8n workflows (n8n-mcp tools), Evolution API (WhatsApp), FastAPI backend (existing approve/reject endpoints)

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `n8n/workflows/volunteer_entry.json` | Modify (6 nodes + rewire) | Main WhatsApp webhook — add manager detection, routing, and state management |
| `n8n/workflows/manager_approval.json` | Create (~9 nodes) | New workflow — process approve/reject actions, notify volunteer + manager |
| (none) | No Python changes needed | All API endpoints already exist |

---

### Task 1: Fix existing HTTP: Lookup Manager URL (bugfix)

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

The existing `HTTP: Lookup Manager` node (id: `http_lookup_mgr`) calls `GET http://api:8000/api/managers` — missing the `/me`. This endpoint doesn't match any route and returns 405.

- [ ] **Step 1: Fix the URL via patchNodeField**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Fix manager lookup URL from /api/managers to /api/managers/me",
  "operations": [{
    "type": "patchNodeField",
    "nodeName": "HTTP: Lookup Manager",
    "fieldPath": "parameters.url",
    "patches": [{
      "find": "http://api:8000/api/managers",
      "replace": "http://api:8000/api/managers/me"
    }]
  }]
}
```

- [ ] **Step 2: Verify the fix**

Read the node back with `n8n_get_workflow` mode=`structure` and confirm URL is correct.

---

### Task 2: Add early manager lookup node (new node)

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

Insert a new HTTP Request node between Webhook and Filter & Route that fetches the manager profile on every webhook call.

- [ ] **Step 1: Add the node**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Add early manager lookup node for sender detection",
  "operations": [{
    "type": "addNode",
    "node": {
      "id": "http_lookup_mgr_early",
      "name": "HTTP: Pridobi Upravljalca",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [360, 300],
      "parameters": {
        "method": "GET",
        "url": "http://api:8000/api/managers/me",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBasicAuth",
        "sendBody": false,
        "options": {}
      },
      "credentials": {
        "httpBasicAuth": {
          "id": "UqZlwzClZfiYKanN",
          "name": "BelPro API (Basic Auth)"
        }
      }
    }
  }]
}
```

- [ ] **Step 2: Rewire — remove old Webhook → Filter & Route connection**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Remove direct connection from Webhook to Filter & Route",
  "operations": [{
    "type": "removeConnection",
    "source": "Webhook: WhatsApp",
    "target": "Filter & Route",
    "sourceIndex": 0,
    "targetIndex": 0
  }]
}
```

- [ ] **Step 3: Add Webhook → Lookup Manager connection**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Connect Webhook to new early manager lookup",
  "operations": [{
    "type": "addConnection",
    "source": "Webhook: WhatsApp",
    "target": "HTTP: Pridobi Upravljalca"
  }]
}
```

- [ ] **Step 4: Add Lookup Manager → Filter & Route connection**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Connect early manager lookup to Filter & Route",
  "operations": [{
    "type": "addConnection",
    "source": "HTTP: Pridobi Upravljalca",
    "target": "Filter & Route"
  }]
}
```

- [ ] **Step 5: Validate workflow structure**

Run `n8n_validate_workflow` on `Lw6qRiO9ozSr6EeW` to confirm no connection errors.

---

### Task 3: Modify Filter & Route code for manager detection

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

Add manager detection BEFORE any other routing. The manager phone must be normalized (remove `+`, spaces) before comparison.

- [ ] **Step 1: Update the jsCode with manager detection**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Add manager detection to Filter & Route — check sender phone before all other routing",
  "operations": [{
    "type": "updateNode",
    "nodeName": "Filter & Route",
    "updates": {
      "parameters": {
        "jsCode": "const body = $input.first().json.body;\nif (!body || body.event !== 'messages.upsert') return [];\nconst data = body.data;\nif (!data || !data.key || data.key.fromMe === true) return [];\nconst rawJid = data.key.remoteJid || '';\n// v2.3.7: remoteJidAlt contains @s.whatsapp.net when remoteJid is @lid\nconst resolvedJid = (rawJid.endsWith('@lid') && data.remoteJidAlt)\n  ? data.remoteJidAlt\n  : rawJid;\nconst remoteJid = resolvedJid;\nconst phone = resolvedJid.split('@')[0].split(':')[0];\nif (!phone || phone.length < 5) return [];\n\n// --- Manager detection (runs first, before any volunteer routing) ---\nconst mgrResp = $('HTTP: Pridobi Upravljalca').first().json;\nconst mgrPhoneRaw = mgrResp.phone || '';\nconst mgrPhone = mgrPhoneRaw.replace(/[^0-9]/g, '');\nif (phone === mgrPhone) {\n  const msg = data.message || {};\n  const messageType = data.messageType || Object.keys(msg)[0] || '';\n  let text = '';\n  if (messageType === 'conversation' || messageType === 'extendedTextMessage') {\n    text = msg.conversation || ((msg.extendedTextMessage || {}).text) || '';\n  }\n  const t = text.trim().toLowerCase();\n  let action = '';\n  if (t === '1' || t === 'odobri') { action = 'odobri'; }\n  else if (t === '2' || t === 'zavrni') { action = 'zavrni'; }\n  else { action = 'unknown'; }\n  return [{json: {phone, remoteJid, route: 'manager', text, action, mgrPhone, messageKey: data.key, messageData: msg}}];\n}\n// --- End manager detection ---\n\nconst msg = data.message || {};\nconst messageType = data.messageType || Object.keys(msg)[0] || '';\nlet route = 'skip', text = '', responseType = '';\nif (messageType === 'audioMessage' || messageType === 'pttMessage') {\n  route = 'audio';\n} else if (messageType === 'buttonsResponseMessage') {\n  responseType = ((msg.buttonsResponseMessage || {}).selectedButtonId || '').toLowerCase();\n  if (!['confirm','edit','cancel'].includes(responseType)) responseType = 'unknown';\n  route = 'response';\n} else if (messageType === 'conversation' || messageType === 'extendedTextMessage') {\n  text = msg.conversation || ((msg.extendedTextMessage || {}).text) || '';\n  const t = text.trim().toLowerCase();\n  if (t === '1' || t === 'potrdi') { route = 'response'; responseType = 'confirm'; }\n  else if (t === '2' || t === 'popravi') { route = 'response'; responseType = 'edit'; }\n  else if (t === '3' || t.startsWith('prekli')) { route = 'response'; responseType = 'cancel'; }\n  else { route = 'text_new'; }\n} else { return []; }\nif (route === 'skip') return [];\nreturn [{json: {phone, remoteJid, route, text, responseType, messageKey: data.key, messageData: msg}}];"
      }
    }
  }]
}
```

- [ ] **Step 2: Validate the updated workflow**

Run `n8n_validate_workflow` on `Lw6qRiO9ozSr6EeW`. Expect warnings about the unreachable Upravljalec branch (not yet connected), no critical errors.

---

### Task 4: Add Upravljalec branch to Razpotje switch

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

- [ ] **Step 1: Add a fourth rule for route === "manager" using updateNode with complete parameters**

Since `patchNodeField` with find/replace is fragile for complex nested JSON, use `updateNode` to set the complete parameters with all 4 rules:

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Add Upravljalec output branch to Razpotje switch with all 4 rules",
  "operations": [{
    "type": "updateNode",
    "nodeName": "Razpotje",
    "updates": {
      "parameters": {
        "mode": "rules",
        "rules": {
          "values": [
            {
              "conditions": {
                "options": {"caseSensitive": true, "leftValue": "", "typeValidation": "strict"},
                "combinator": "and",
                "conditions": [{"id": "r1c1", "leftValue": "={{ $json.route }}", "rightValue": "audio", "operator": {"type": "string", "operation": "equals", "name": "filter.operator.equals"}}]
              },
              "renameOutput": true,
              "outputKey": "Audio"
            },
            {
              "conditions": {
                "options": {"caseSensitive": true, "leftValue": "", "typeValidation": "strict"},
                "combinator": "and",
                "conditions": [{"id": "r2c1", "leftValue": "={{ $json.route }}", "rightValue": "text_new", "operator": {"type": "string", "operation": "equals", "name": "filter.operator.equals"}}]
              },
              "renameOutput": true,
              "outputKey": "Besedilo"
            },
            {
              "conditions": {
                "options": {"caseSensitive": true, "leftValue": "", "typeValidation": "strict"},
                "combinator": "and",
                "conditions": [{"id": "r3c1", "leftValue": "={{ $json.route }}", "rightValue": "response", "operator": {"type": "string", "operation": "equals", "name": "filter.operator.equals"}}]
              },
              "renameOutput": true,
              "outputKey": "Odziv"
            },
            {
              "conditions": {
                "options": {"caseSensitive": true, "leftValue": "", "typeValidation": "strict"},
                "combinator": "and",
                "conditions": [{"id": "r4c1", "leftValue": "={{ $json.route }}", "rightValue": "manager", "operator": {"type": "string", "operation": "equals", "name": "filter.operator.equals"}}]
              },
              "renameOutput": true,
              "outputKey": "Upravljalec"
            }
          ]
        },
        "options": {}
      }
    }
  }]
}
```

- [ ] **Step 2: Validate**

Run `n8n_validate_workflow` on `Lw6qRiO9ozSr6EeW`. Confirm the switch has 4 outputs now.

---

### Task 5: Add Parse Manager Action code node

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

This node reads the manager's reply text, determines action (odobri/zavrni), looks up the pending entry from workflow static data (keyed by manager phone), and prepares the payload for the manager_approval workflow.

- [ ] **Step 1: Add the Code node**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Add Code node that parses manager action and looks up pending entry from state",
  "operations": [{
    "type": "addNode",
    "node": {
      "id": "code_parse_mgr_action",
      "name": "Code: Parse Manager Action",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [760, 460],
      "parameters": {
        "jsCode": "const filterData = $input.first().json;\nconst action = filterData.action;\nconst mgrPhone = filterData.mgrPhone;\n\n// Look up the pending entry for this manager from static data\nconst sd = $getWorkflowStaticData('global');\nconst stateKey = 'mgr_' + mgrPhone;\nconst state = sd[stateKey];\n\nif (!state) {\n  return [{json: {\n    error: true,\n    message: 'Ni aktivnega vnosa za odobritev.',\n    mgrJid: filterData.remoteJid\n  }}];\n}\n\n// Normalize manager JID for Evolution API\nconst mgrJid = mgrPhone + '@s.whatsapp.net';\n\nreturn [{json: {\n  error: false,\n  action,\n  entry_id: state.entry_id,\n  manager_phone: mgrPhone,\n  manager_remoteJid: mgrJid,\n  volunteer_name: state.volunteer_name,\n  volunteer_remoteJid: state.remoteJid,\n  entry_date: state.entry_date,\n  hours: state.hours,\n  activity_description: state.activity_description,\n  location: state.location\n}}];"
      }
    }
  }]
}
```

- [ ] **Step 2: Add a no-state error handler path (optional for v1)**

For now, if the manager replies but there's no state, we reply with an error message. We'll add this WhatsApp error node in a later task. 

---

### Task 6: Add Execute Workflow node

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

This node calls the `manager_approval` workflow with the parsed action data.

- [ ] **Step 1: Add the node**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Add Execute Workflow node that calls manager_approval",
  "operations": [{
    "type": "addNode",
    "node": {
      "id": "exec_mgr_approval",
      "name": "Execute Workflow: Manager Approval",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [1020, 460],
      "parameters": {
        "operation": "call",
        "source": "database",
        "workflowId": "",
        "mode": "each",
        "options": {}
      }
    }
  }]
}
```

Note: The `workflowId` is empty because the manager_approval workflow doesn't exist yet. We'll update this in Task 13 after creating that workflow.

- [ ] **Step 2: Wire: Razpotje[3] → Parse Manager Action → Execute Workflow**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Connect manager branch: Razpotje Upravljalec → Parse Manager Action → Execute Workflow",
  "operations": [
    {
      "type": "addConnection",
      "source": "Razpotje",
      "target": "Code: Parse Manager Action",
      "branch": "Upravljalec"
    },
    {
      "type": "addConnection",
      "source": "Code: Parse Manager Action",
      "target": "Execute Workflow: Manager Approval"
    }
  ]
}
```

---

### Task 7: Add error WhatsApp node for no-state case

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

When the manager replies but there's no pending entry in state, send a WhatsApp message explaining the issue.

- [ ] **Step 1: Add the HTTP node**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Add WhatsApp error node for when manager replies but no entry is pending",
  "operations": [{
    "type": "addNode",
    "node": {
      "id": "http_wa_mgr_nostate",
      "name": "HTTP: WA Ni Aktivnega Vnosa (Mgr)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1020, 560],
      "parameters": {
        "method": "POST",
        "url": "http://evolution-api:8080/message/sendText/belpro",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            {"name": "number", "value": "={{ $json.mgrJid }}"},
            {"name": "text", "value": "={{ $json.message }}"}
          ]
        },
        "options": {}
      },
      "credentials": {
        "httpHeaderAuth": {
          "id": "QXGVac2NwnJcQf9V",
          "name": "BelPro Evolution API"
        }
      }
    }
  }]
}
```

- [ ] **Step 2: Add IF node to route error path**

First add a new IF node after Code: Parse Manager Action, then connect its false (no error) output to Execute Workflow and its true (error) output to the error WhatsApp node.

Since we're iterating, we can add this as a simpler alternative: connect Parse Manager Action to both the error handler and Execute Workflow. The error handler checks `$json.error` in a Switch/IF.

Actually, the Execute Workflow node will simply not process the error case (it only has meaningful data when error=false). And the Parse Manager Action output can fork. But n8n Code nodes have a single output.

**Simpler approach for v1:** Add an IF node between Parse Manager Action and Execute Workflow.

Let's defer this to post-MVP. The parse node will output error data, and the Execute Workflow will call manager_approval which will handle or fail gracefully. For now, if there's no state, nothing happens (the Execute Workflow call will pass error=true data to manager_approval, which we handle there).

---

### Task 8: Modify Code: Pripravi Obvestilo Upravljalcu (state storage + phone fix)

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

Update the manager notification code to:
1. Store state keyed by manager phone (so manager replies can be associated with the entry)
2. Normalize the manager phone to digits-only for WhatsApp
3. Add approve/reject reply options to the message

- [ ] **Step 1: Update the jsCode**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Update manager notification to store state, normalize phone, and add reply options",
  "operations": [{
    "type": "updateNode",
    "nodeName": "Code: Pripravi Obvestilo Upravljalcu",
    "updates": {
      "parameters": {
        "jsCode": "const mgrResp = $input.first().json;\nconst mgrPhoneRaw = mgrResp.phone || '';\n// Remove + and all non-digits for WhatsApp JID / state key\nconst mgrPhone = mgrPhoneRaw.replace(/[^0-9]/g, '');\nconst mgrJid = mgrPhone + '@s.whatsapp.net';\n\nconst vol = $('Code: Clear State Confirm').first().json;\n// Clear State Confirm doesn't include entry_id — get it from Nalozi Stanje\nconst stateData = $('Nalozi Stanje').first().json;\n\nconst {entry_date, hours, activity_description, location, volunteer_name} = vol;\n\n// Store state for manager reply handling (keyed by mgr_ + manager phone)\nconst sd = $getWorkflowStaticData('global');\nconst stateKey = 'mgr_' + mgrPhone;\nsd[stateKey] = {\n  entry_id: stateData.entry_id,\n  volunteer_name,\n  remoteJid: vol.remoteJid,\n  entry_date,\n  hours,\n  activity_description,\n  location\n};\n\nconst d = new Date((entry_date||'2000-01-01')+'T12:00:00Z');\nconst dateStr = `${d.getUTCDate()}. ${d.getUTCMonth()+1}. ${d.getUTCFullYear()}`;\nconst mgrMsg = `Nov vnos čaka na odobritev:\\n\\n👤 ${volunteer_name||'Prostovoljec'}\\n📅 ${dateStr} — ${hours} ur\\n📝 ${activity_description||''}\\n📍 ${location||'ni navedeno'}\\n\\n1 - Odobri\\n2 - Zavrni`;\nreturn [{json: {phone: mgrJid, text: mgrMsg}}];"
      }
    }
  }]
}
```

Note: This also fixes the existing bug where `HTTP: WA Upravljalcu` referenced `$json.remoteJid` but the Code node only output `{phone, text}`. Now the Code node outputs `{phone, text}` where `phone` is the JID (`38530369632@s.whatsapp.net`). We also need to fix the HTTP node (next task).

---

### Task 9: Fix HTTP: WA Upravljalcu body parameter

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

The node currently references `$json.remoteJid` but the Code node outputs `phone` as the JID. Fix the body parameter.

- [ ] **Step 1: Fix the number parameter**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Fix WhatsApp manager notification to use correct phone field from Code node output",
  "operations": [{
    "type": "patchNodeField",
    "nodeName": "HTTP: WA Upravljalcu",
    "fieldPath": "parameters.bodyParameters.parameters",
    "patches": [{
      "find": "={{ $json.remoteJid }}",
      "replace": "={{ $json.phone }}"
    }]
  }]
}
```

---

### Task 10: Validate volunteer_entry workflow

**Files:** `volunteer_entry` workflow in n8n

- [ ] **Step 1: Run full validation**

```text
Tool: n8n_validate_workflow
Args: {"id": "Lw6qRiO9ozSr6EeW"}
```

Expected: No critical errors. May have warnings about:
- `Execute Workflow: Manager Approval` referencing a workflow that doesn't exist yet (we'll fix in Task 13)
- `Code: Pripravi Obvestilo Upravljalcu` referencing `Code: Clear State Confirm` — this is correct from existing flow

- [ ] **Step 2: Export the workflow to JSON and commit**

```bash
Tool: n8n_get_workflow with mode="full" → save to n8n/workflows/volunteer_entry.json
git add n8n/workflows/volunteer_entry.json
git commit -m "feat: add manager detection and routing to volunteer_entry workflow"
```

---

### Task 11: Create manager_approval workflow

**Files:** Create `n8n/workflows/manager_approval.json` via n8n-mcp

Create the workflow with all nodes in one shot using `n8n_create_workflow`.

- [ ] **Step 1: Create the workflow with all nodes and connections**

```text
Tool: n8n_create_workflow
Args: {
  "name": "BelPro — Odobritev Upravljalca",
  "nodes": [
    {
      "id": "exec_trigger",
      "name": "Execute Workflow Trigger",
      "type": "n8n-nodes-base.executeWorkflowTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {}
    },
    {
      "id": "manual_trigger",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [240, 500],
      "parameters": {}
    },
    {
      "id": "code_parse_action",
      "name": "Code: Parse Action",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [500, 400],
      "parameters": {
        "jsCode": "const data = $input.first().json;\n\n// Extract common fields (present from both triggers)\nconst entry_id = data.entry_id;\nconst action = data.action || '';\n\n// If this came from the volunteer_entry parse node, data is already complete\n// If from Manual Trigger, data should include all fields\nconst payload = {\n  entry_id,\n  action,\n  manager_phone: data.manager_phone || '',\n  manager_remoteJid: data.manager_remoteJid || '',\n  volunteer_name: data.volunteer_name || '',\n  volunteer_remoteJid: data.volunteer_remoteJid || '',\n  entry_date: data.entry_date || '',\n  hours: data.hours || 0,\n  activity_description: data.activity_description || '',\n  location: data.location || ''\n};\n\n// Validate required fields\nif (!entry_id || !action) {\n  throw new Error('Missing required fields: entry_id and action');\n}\n\nreturn [{json: payload}];"
      }
    },
    {
      "id": "switch_action",
      "name": "Switch: Action",
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3,
      "position": [760, 400],
      "parameters": {
        "mode": "rules",
        "rules": {
          "values": [
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict"
                },
                "combinator": "and",
                "conditions": [
                  {
                    "id": "r1c1",
                    "leftValue": "={{ $json.action }}",
                    "rightValue": "odobri",
                    "operator": {
                      "type": "string",
                      "operation": "equals",
                      "name": "filter.operator.equals"
                    }
                  }
                ]
              },
              "renameOutput": true,
              "outputKey": "Odobri"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict"
                },
                "combinator": "and",
                "conditions": [
                  {
                    "id": "r2c1",
                    "leftValue": "={{ $json.action }}",
                    "rightValue": "zavrni",
                    "operator": {
                      "type": "string",
                      "operation": "equals",
                      "name": "filter.operator.equals"
                    }
                  }
                ]
              },
              "renameOutput": true,
              "outputKey": "Zavrni"
            }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "http_approve",
      "name": "HTTP: PATCH /approve",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1020, 240],
      "parameters": {
        "method": "PATCH",
        "url": "={{ 'http://api:8000/api/log-entries/' + $json.entry_id + '/approve' }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBasicAuth",
        "sendBody": false,
        "options": {}
      },
      "credentials": {
        "httpBasicAuth": {
          "id": "UqZlwzClZfiYKanN",
          "name": "BelPro API (Basic Auth)"
        }
      }
    },
    {
      "id": "http_reject",
      "name": "HTTP: PATCH /reject",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1020, 560],
      "parameters": {
        "method": "PATCH",
        "url": "={{ 'http://api:8000/api/log-entries/' + $json.entry_id + '/reject' }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBasicAuth",
        "sendBody": false,
        "options": {}
      },
      "credentials": {
        "httpBasicAuth": {
          "id": "UqZlwzClZfiYKanN",
          "name": "BelPro API (Basic Auth)"
        }
      }
    },
    {
      "id": "code_vol_msg",
      "name": "Code: Build Volunteer Msg",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1280, 400],
      "parameters": {
        "jsCode": "const payload = $('Code: Parse Action').first().json;\nconst isApproved = payload.action === 'odobri';\n\nlet volMsg;\nif (isApproved) {\n  volMsg = `Vaš vnos z dne ${payload.entry_date} je bil odobren. ✅\\n📝 ${payload.activity_description}, ${payload.hours} ur`;\n} else {\n  volMsg = `Vaš vnos z dne ${payload.entry_date} je bil zavrnjen. ❌\\nUpravljalec vas bo kontaktiral za podrobnosti.`;\n}\n\nreturn [{\n  json: {\n    ...payload,\n    action: isApproved ? 'approved' : 'rejected',\n    volMsg,\n    volunteerJid: payload.volunteer_remoteJid\n  }\n}];"
      }
    },
    {
      "id": "http_wa_volunteer",
      "name": "HTTP: WA Notify Volunteer",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1540, 400],
      "parameters": {
        "method": "POST",
        "url": "http://evolution-api:8080/message/sendText/belpro",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            {"name": "number", "value": "={{ $json.volunteerJid }}"},
            {"name": "text", "value": "={{ $json.volMsg }}"}
          ]
        },
        "options": {}
      },
      "credentials": {
        "httpHeaderAuth": {
          "id": "QXGVac2NwnJcQf9V",
          "name": "BelPro Evolution API"
        }
      }
    },
    {
      "id": "code_mgr_confirm",
      "name": "Code: Build Manager Confirm",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1800, 400],
      "parameters": {
        "jsCode": "const payload = $('Code: Parse Action').first().json;\nconst actionLabel = payload.action === 'odobri' ? 'odobren' : 'zavrnjen';\nconst mgrMsg = `Vnos za ${payload.volunteer_name} je bil ${actionLabel}.`;\n\nreturn [{\n  json: {\n    managerJid: payload.manager_remoteJid,\n    mgrMsg,\n    ...payload\n  }\n}];"
      }
    },
    {
      "id": "http_wa_manager",
      "name": "HTTP: WA Confirm to Manager",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [2060, 400],
      "parameters": {
        "method": "POST",
        "url": "http://evolution-api:8080/message/sendText/belpro",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            {"name": "number", "value": "={{ $json.managerJid }}"},
            {"name": "text", "value": "={{ $json.mgrMsg }}"}
          ]
        },
        "options": {}
      },
      "credentials": {
        "httpHeaderAuth": {
          "id": "QXGVac2NwnJcQf9V",
          "name": "BelPro Evolution API"
        }
      }
    }
  ],
  "connections": {
    "Execute Workflow Trigger": {
      "main": [[{"node": "Code: Parse Action", "type": "main", "index": 0}]]
    },
    "Manual Trigger": {
      "main": [[{"node": "Code: Parse Action", "type": "main", "index": 0}]]
    },
    "Code: Parse Action": {
      "main": [[{"node": "Switch: Action", "type": "main", "index": 0}]]
    },
    "Switch: Action": {
      "main": [
        [{"node": "HTTP: PATCH /approve", "type": "main", "index": 0}],
        [{"node": "HTTP: PATCH /reject", "type": "main", "index": 0}]
      ]
    },
    "HTTP: PATCH /approve": {
      "main": [[{"node": "Code: Build Volunteer Msg", "type": "main", "index": 0}]]
    },
    "HTTP: PATCH /reject": {
      "main": [[{"node": "Code: Build Volunteer Msg", "type": "main", "index": 0}]]
    },
    "Code: Build Volunteer Msg": {
      "main": [[{"node": "HTTP: WA Notify Volunteer", "type": "main", "index": 0}]]
    },
    "HTTP: WA Notify Volunteer": {
      "main": [[{"node": "Code: Build Manager Confirm", "type": "main", "index": 0}]]
    },
    "Code: Build Manager Confirm": {
      "main": [[{"node": "HTTP: WA Confirm to Manager", "type": "main", "index": 0}]]
    }
  }
}
```

- [ ] **Step 2: Validate the new workflow**

```text
Tool: n8n_validate_workflow
Args: {"id": "<workflow-id-from-create>"}
```

- [ ] **Step 3: Auto-fix any issues**

```text
Tool: n8n_autofix_workflow
Args: {"id": "<workflow-id-from-create>", "applyFixes": true}
```

- [ ] **Step 4: Export to JSON and commit**

```bash
n8n_get_workflow with mode="full" → save to n8n/workflows/manager_approval.json
git add n8n/workflows/manager_approval.json
git commit -m "feat: add manager_approval workflow with WhatsApp approve/reject"
```

---

### Task 12: Link Execute Workflow node to manager_approval

**Files:** Modify `volunteer_entry` workflow via n8n-mcp

Now that manager_approval exists, update the Execute Workflow node with the real workflow ID.

- [ ] **Step 1: Get manager_approval workflow ID**

```text
Tool: n8n_list_workflows
→ Find "BelPro — Odobritev Upravljalca" → get its ID
```

- [ ] **Step 2: Update the Execute Workflow node**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "Lw6qRiO9ozSr6EeW",
  "intent": "Link Execute Workflow node to the real manager_approval workflow ID",
  "operations": [{
    "type": "patchNodeField",
    "nodeName": "Execute Workflow: Manager Approval",
    "fieldPath": "parameters.workflowId",
    "patches": [{
      "find": "",
      "replace": "<manager-approval-workflow-id>"
    }]
  }]
}
```

- [ ] **Step 3: Commit the updated volunteer_entry**

```bash
n8n_get_workflow with mode="full" → save to n8n/workflows/volunteer_entry.json
git add n8n/workflows/volunteer_entry.json
git commit -m "fix: link Execute Workflow node to manager_approval workflow"
```

---

### Task 13: Manual test — approve flow

**Files:** None (testing only)

- [ ] **Step 1: Ensure a test entry exists in pending_manager status**

Check the database for entries with `status = 'pending_manager'`. If none exist, create one via the volunteer flow:
- Send a voice message from volunteer test phone (38630369632)
- Go through the confirmation flow (reply "1" to confirm)

- [ ] **Step 2: Activate the manager_approval workflow**

```text
Tool: n8n_update_partial_workflow
Args: {
  "id": "<manager-approval-id>",
  "operations": [{"type": "activateWorkflow"}]
}
```

- [ ] **Step 3: Test via Manual Trigger**

Open `BelPro — Odobritev Upravljalca` in n8n UI. Use Manual Trigger with this payload (adjust `entry_id`, `volunteer_remoteJid` from real data):

```json
{
  "entry_id": "<real-entry-uuid>",
  "action": "odobri",
  "manager_phone": "38530369632",
  "manager_remoteJid": "38530369632@s.whatsapp.net",
  "volunteer_name": "Slavko Pridni",
  "volunteer_remoteJid": "38630369632@s.whatsapp.net",
  "entry_date": "07.05.2026",
  "hours": 3,
  "activity_description": "Testno okopavanje",
  "location": "Radece"
}
```

Expected:
- HTTP: PATCH /approve returns 200 with status `approved`
- WhatsApp messages sent to both volunteer and manager

- [ ] **Step 4: Test via Manual Trigger — reject path**

Same payload but with `action: "zavrni"`. Expected:
- HTTP: PATCH /reject returns 200 with status `rejected`
- Rejection message sent to volunteer
- Confirmation sent to manager

---

### Task 14: End-to-end test via WhatsApp (requires manager phone)

**Files:** None (testing only)

- [ ] **Step 1: Submit a volunteer entry via WhatsApp**
  - Send voice message from volunteer phone → confirm with "1"

- [ ] **Step 2: Verify manager receives notification**
  - Manager phone (38530369632) should receive: "Nov vnos čaka na odobritev: ..." with "1 - Odobri / 2 - Zavrni"

- [ ] **Step 3: Manager replies "1" to approve**
  - Volunteer should receive: "Vaš vnos z dne ... je bil odobren. ✅"
  - Manager should receive: "Vnos za Slavko Pridni je bil odobren."

- [ ] **Step 4: Submit another entry, manager replies "2" to reject**
  - Volunteer should receive: "Vaš vnos z dne ... je bil zavrnjen. ❌"
  - Manager should receive: "Vnos za Slavko Pridni je bil zavrnjen."

- [ ] **Step 5: Verify manager messages don't trigger "not registered"**
  - Manager sends a random text → should not receive "Niste registrirani" message
  - Manager sends "hello" → should parse action as "unknown" and silently be ignored (or get an appropriate error)

---

### Task 15: Final validation and cleanup

- [ ] **Step 1: Validate both workflows**

```text
n8n_validate_workflow(id="Lw6qRiO9ozSr6EeW")
n8n_validate_workflow(id="<manager-approval-id>")
```

- [ ] **Step 2: Export and commit final state**

```bash
n8n_get_workflow → save both JSON files
git add n8n/workflows/volunteer_entry.json n8n/workflows/manager_approval.json
git commit -m "feat: WhatsApp manager approval flow complete

- volunteer_entry: manager detection, routing, state management
- manager_approval: new workflow with dual triggers, approve/reject, notifications

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

- [ ] **Step 3: Update graphify**

```bash
graphify update .
```

- [ ] **Step 4: Clean up temp file**

```bash
rm _node_dump.txt
```
