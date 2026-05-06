# Evolution API — @lid JID Resolution for BelPro

## The Problem

Android WhatsApp users send messages with `remoteJid: "245616546422929@lid"` instead of `38630369632@s.whatsapp.net`. Evolution API's `sendText` endpoint rejects `@lid` as a recipient (`exists: false`). This breaks both volunteer DB lookup (we store real E.164 phones) and WA reply sending.

## Priority Fix: Upgrade to v2.3.7

Our current version is **v2.2.3**. Starting in **v2.3.x**, Evolution API populates `remoteJidAlt` in the webhook payload alongside `remoteJid`:

```json
{
  "data": {
    "key": { "remoteJid": "245616546422929@lid" },
    "remoteJidAlt": "38630369632@s.whatsapp.net",
    "addressingMode": "lid"
  }
}
```

With v2.3.7, `Filter & Route` becomes trivial:
```js
const rawJid = data.key.remoteJid;
const remoteJid = (rawJid.endsWith('@lid') && data.remoteJidAlt)
  ? data.remoteJidAlt
  : rawJid;
const phone = remoteJid.split('@')[0];
```

v2.3.7 also fixes Typebot/n8n `@lid` routing internally — it may even send replies to `@lid` correctly without needing `remoteJidAlt` at all.

**How to upgrade:** change `image: atendai/evolution-api:latest` → `atendai/evolution-api:2.3.7` in `docker-compose.yml`, then `docker compose up -d evolution-api`. Volumes and DB schema are unchanged between 2.2.x and 2.3.x.

## Environment Variables to Add on Upgrade

Add to `evolution-api` service in `docker-compose.yml`:

```yaml
WPP_LID_MODE: "false"            # Instructs underlying WPP to prefer phone-based JIDs
DATABASE_SAVE_DATA_CONTACTS: "true"  # Persists LID↔phone mapping in DB for fast lookups
DATABASE_SAVE_IS_ON_WHATSAPP: "true" # Caches existence checks, reduces protocol overhead
```

`WPP_LID_MODE=false` won't eliminate `@lid` entirely (Meta enforces it server-side), but combined with `remoteJidAlt` it provides a reliable fallback chain.

## Current Workaround (v2.2.3, active in workflow)

`Filter & Route` does a two-step `findContacts` call when it detects `@lid`:
1. Fetch contact by LID → get `pushName`
2. Fetch contacts by `pushName` → find `@s.whatsapp.net` entry

**This is unreliable** — `pushName` is not unique (multiple "Andrej Mejač" exist in the wild). It works for the current test but will misfire when two volunteers share a name. Remove this logic after upgrading to v2.3.7.

## Sendback: @lid as Direct Recipient

v2.3.7 also updated `sendText` to accept `@lid` directly as the `number` field, routing internally without an existence check. So even without `remoteJidAlt`, replying to the original `@lid` `remoteJid` should work after upgrade. This means the `remoteJidAlt` path is for DB lookup; the `@lid` itself can be used for WA sending.

## Future: Volunteer Registration Flow

Longer-term fix: add a registration workflow where a new volunteer sends "registracija" via WhatsApp. The webhook captures their `remoteJid` (or `remoteJidAlt`) at that moment and stores it against their record. This permanently solves LID ambiguity for that volunteer and removes reliance on phone-number matching entirely. Low priority while the v2.3.7 upgrade holds.

## What Does NOT Work

- **Name-based lookup via `findContacts`**: `pushName` is not unique. Do not use.
- **`data.sender` / `data.senderPn` fields**: Present in some Evolution versions but absent in v2.2.3. Not reliable as a primary strategy.
- **Community fork `drikosv8/evolution-api-fix--lid`**: Backport of 2.3.6 fix, prefer official 2.3.7.
