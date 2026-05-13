# Fix Image Upload — $env Access Denied in Code Node

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `$env.MANAGER_PASSWORD` in Code node with HTTP Request node using n8n credential-based Basic Auth.

**Architecture:** Split the Code node that called BelPro API into: (1) Code node that prepares data, (2) HTTP Request node with `BelPro API (Basic Auth)` credential that makes the API call. Same pattern every other API call in the workflow uses.

**Tech Stack:** n8n workflow editing via MCP tools (`n8n_update_partial_workflow`)

---

**Workflow ID:** `Lw6qRiO9ozSr6EeW`
**Credential:** `BelPro API (Basic Auth)` / `httpBasicAuth` / ID `UqZlwzClZfiYKanN`

## Current State (Already Applied)

- `Code: Upload Photo` renamed to `Code: Pripravi Upload Slike`, jsCode patched to only prepare data (strip base64, pass through `{image_base64, filename, phone, remoteJid, entry_id}`)
- Current connections: `HTTP: Fetch Image` → `Code: Pripravi Upload Slike` → `Code: Slika Prejeta` → `HTTP: WA Slika Prejeta`

---

### Task 1: Add HTTP: Upload Photo Node

**Files:** n8n workflow `Lw6qRiO9ozSr6EeW` (live, via MCP)

- [ ] **Step 1: Add the HTTP Request node**

```
n8n_update_partial_workflow with addNode:
  name: "HTTP: Upload Photo"
  type: "n8n-nodes-base.httpRequest"
  typeVersion: 4.2
  position: [2192, 400]
  credentials:
    httpBasicAuth:
      id: "UqZlwzClZfiYKanN"
      name: "BelPro API (Basic Auth)"
  parameters:
    method: "POST"
    url: "={{ 'http://api:8000/api/log-entries/' + $json.entry_id + '/photos/base64' }}"
    sendBody: true
    bodyParameters:
      parameters:
        - name: "image_base64"
          value: "={{ $json.image_base64 }}"
        - name: "filename"
          value: "={{ $json.filename }}"
    options:
      redirect:
        redirect: {}
```

- [ ] **Step 2: Verify** — workflow still has `Code: Pripravi Upload Slike` → `Code: Slika Prejeta` direct connection

---

### Task 2: Rewire Connections

**Files:** n8n workflow `Lw6qRiO9ozSr6EeW` (live, via MCP)

- [ ] **Step 1: Remove old connection** — source: `Code: Pripravi Upload Slike`, target: `Code: Slika Prejeta`

- [ ] **Step 2: Add first new connection** — source: `Code: Pripravi Upload Slike`, target: `HTTP: Upload Photo`

- [ ] **Step 3: Add second new connection** — source: `HTTP: Upload Photo`, target: `Code: Slika Prejeta`

- [ ] **Step 4: Verify** — image path is now: `HTTP: Fetch Image` → `Code: Pripravi Upload Slike` → `HTTP: Upload Photo` → `Code: Slika Prejeta` → `HTTP: WA Slika Prejeta`

---

### Task 3: Update Code: Slika Prejeta

**Files:** n8n workflow `Lw6qRiO9ozSr6EeW` (live, via MCP)

- [ ] **Step 1: Patch jsCode** — change `$input.first().json` to `$('Code: Pripravi Upload Slike').first().json`

New jsCode:
```javascript
const d = $('Code: Pripravi Upload Slike').first().json;
return [{json: {phone: d.phone, remoteJid: d.remoteJid, text: "Sprejeto.\n1 - Potrdi\n3 - Več slik\n4 - Prekliči"}}];
```

The input is now the HTTP response (no `phone`/`remoteJid`), so we reference the Code node directly.

---

### Task 4: Validate and Export

**Files:** n8n workflow `Lw6qRiO9ozSr6EeW` (live), `n8n/workflows/volunteer_entry.json` (git)

- [ ] **Step 1: Validate** workflow — expect 0 errors

- [ ] **Step 2: Export** workflow JSON to `n8n/workflows/volunteer_entry.json`

- [ ] **Step 3: Run** `graphify update .`
