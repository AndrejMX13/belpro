---
name: Evolution API QR code fix
description: How to connect WhatsApp in Evolution API v2.2.3 — QR never shows without CONFIG_SESSION_PHONE_VERSION fix
type: project
originSessionId: ef7602a9-8b61-44a8-bbfc-155b7717175a
---
Evolution API v2.2.3 (atendai/evolution-api:latest) requires `CONFIG_SESSION_PHONE_VERSION` set in docker-compose.yml or Baileys gets rejected by WhatsApp and never generates a QR code. Dashboard QR modal is also broken by a separate UI bug — QR must be fetched via API.

**Why:** WhatsApp rejects the stale client version shipped with Baileys in v2.2.3. The dashboard UI bug is tracked in Evolution API issue #1602.

**How to apply:** See [EVOLUTION_QR_TROUBLESHOOTING.md](../../../../../vsCode-workspace/BelPro/EVOLUTION_QR_TROUBLESHOOTING.md) for all commands. Current working version value: `2.3000.1035194821` (check https://raw.githubusercontent.com/WhiskeySockets/Baileys/master/src/Defaults/baileys-version.json for latest). Note: this var was removed in Evolution API v2.3.1+ — only needed for v2.2.x.
