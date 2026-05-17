[Slovenščina](EVOLUTION_QR_TROUBLESHOOTING_SL.md)

# Evolution API — WhatsApp QR Code Troubleshooting

> **Status (2026-05-17):** Upgraded to Evolution API v2.3.7. `CONFIG_SESSION_PHONE_VERSION` is still present and required in the working config. Root Causes #2 and #3 and the reconnection procedure (step 5) remain relevant.

## The Problem

After setting up a new Evolution API instance with Baileys integration, the QR code never appeared. Symptoms:

- Dashboard "Get QR Code" button opens a modal with only a title, no QR image
- "Get Pairing Code" button shows a busy animation forever
- `GET /instance/connect/belpro` returns `{"count":0}`
- `GET /instance/connectionState/belpro` returns `{"instance":{"instanceName":"belpro","state":"connecting"}}`

## Root Causes

### 1. Outdated WhatsApp client version (the real blocker)

Evolution API v2.2.3 ships with Baileys using WhatsApp client version `2.3000.1015901307`. WhatsApp's servers reject this version — Baileys connects, attempts registration, and immediately receives `Error: Connection Failure`. This loop repeats indefinitely and no QR is ever generated.

**Fix:** Set `CONFIG_SESSION_PHONE_VERSION` in docker-compose.yml to match the current Baileys version.

Check the current correct value at:
```
https://raw.githubusercontent.com/WhiskeySockets/Baileys/master/src/Defaults/baileys-version.json
```

The value is an array like `[2, 3000, 1035194821]` — join with dots: `2.3000.1035194821`.

In `docker-compose.yml` under the `evolution-api` service:
```yaml
environment:
  CONFIG_SESSION_PHONE_VERSION: "2.3000.1035194821"
```

> **Note:** Still present and required in v2.3.7 — do not remove it.

### 2. Dashboard UI bug (separate issue)

Even after fixing the version, the dashboard modal does not render the QR image — it receives the base64 string from the backend but fails to display it. This is a known bug tracked in [Evolution API issue #1602](https://github.com/EvolutionAPI/evolution-api/issues/1602).

**Workaround:** Fetch the QR via API and render it manually (see below).

### 3. Wrong env var mapping (found during investigation)

`docker-compose.yml` had `AUTHENTICATION_API_KEY: ${EVOLUTION_API_KEY}` — mapping the global admin key to the per-instance token variable. These are two different things:

- `AUTHENTICATION_API_KEY` — global Evolution API admin key (used in curl `-H "apikey: ..."`)
- `EVOLUTION_API_KEY` — per-instance token used by n8n to call a specific instance

Fixed to `AUTHENTICATION_API_KEY: ${AUTHENTICATION_API_KEY}` in docker-compose.yml.

---

## Setup Steps (clean instance from scratch)

### 1. Ensure docker-compose.yml has the correct environment variables

```yaml
evolution-api:
  environment:
    CONFIG_SESSION_PHONE_VERSION: "2.3000.1035194821"
    AUTHENTICATION_API_KEY: ${AUTHENTICATION_API_KEY}
```

### 2. Restart Evolution API

```bash
docker compose up -d evolution-api
```

### 3. Delete any existing broken instance

```bash
curl -X DELETE \
  -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/delete/belpro
```

### 4. Create instance and connect in one shot

```bash
curl -s -X POST \
  -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"instanceName":"belpro","integration":"WHATSAPP-BAILEYS"}' \
  http://localhost:8180/instance/create \
&& sleep 3 \
&& curl -s \
  -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connect/belpro
```

### 5. Get QR code and scan it

The dashboard won't show the QR. Use this instead — it saves the QR as an HTML file you can open in the browser:

```bash
curl -s -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connect/belpro \
  | python /tmp/makeqr.py \
  && cp /tmp/qr.html /path/to/BelPro/qr.html
```

Where `/tmp/makeqr.py` contains:

```python
import json, sys

data = json.load(sys.stdin)
html = '<html><body><img src="' + data['base64'] + '" style="width:300px"></body></html>'
with open('/tmp/qr.html', 'w') as f:
    f.write(html)
print('saved, count=' + str(data['count']))
```

Open `qr.html` in a browser and scan with WhatsApp: **Settings → Linked Devices → Link a Device**. QR expires in ~60 seconds.

---

## Reconnecting (phone unlinked, session expired)

Just re-run step 5 — no need to delete/recreate the instance:

```bash
curl -s -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connect/belpro \
  | python /tmp/makeqr.py \
  && cp /tmp/qr.html /mnt/d/Andrej/vsCode-workspace/BelPro/qr.html \
  && echo "Open qr.html in browser"
```

---

## Checking instance status

```bash
# Connection state
curl -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/connectionState/belpro

# Full instance info
curl -H "apikey: YOUR_AUTHENTICATION_API_KEY" \
  http://localhost:8180/instance/fetchInstances
```

Expected connected state: `{"instance":{"instanceName":"belpro","state":"open"}}`

---

## Key env vars in .env

```
AUTHENTICATION_API_KEY=...   # Global Evolution API admin key — used in all curl -H "apikey: ..." calls
EVOLUTION_API_KEY=...        # Per-instance token — used by n8n workflows to send messages
EVOLUTION_INSTANCE_NAME=belpro
EVOLUTION_SERVER_URL=http://localhost:8180
```

---

## Version info

- Evolution API: `2.3.7` (image: `evoapicloud/evolution-api:v2.3.7`)
- Upgraded from `2.2.3` on 2026-05-17; `CONFIG_SESSION_PHONE_VERSION` still required
- Baileys version in use: `2.3000.1035194821`
- Related GitHub issues: [#1602](https://github.com/EvolutionAPI/evolution-api/issues/1602), [#2068](https://github.com/EvolutionAPI/evolution-api/issues/2068), [#2380](https://github.com/EvolutionAPI/evolution-api/issues/2380)
