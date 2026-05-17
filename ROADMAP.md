# BelPro — Things Worth Considering

Informal parking lot for ideas that are worth doing eventually but not right now.
No deadlines, no commitments, no particular order.

---

## UI / Manager experience

**Delivery failure indicator on volunteer detail page**
If a message to a volunteer fails (wrong phone number, unrecognized contact, bad email address),
surface a red banner or warning on their detail page in the dashboard. The manager can then fix
the contact data directly from the UI rather than hunting through logs. Straightforward to implement
once there's a reliable failure signal to consume.

**n8n error reporting to UI**
Right now n8n execution failures live in n8n's own logs. If the bot goes quiet — delivery failure,
workflow error, Evolution API hiccup — the manager only notices when volunteers stop getting messages.
Worth building a small feedback channel: n8n calls back to a `/api/errors` endpoint on failure,
the dashboard shows a banner when something is actively broken. Needs some design work first
(error schema, retention, what's worth showing vs. noise). More involved than the above.

---

## Evolution API

**Phone number routing via API**
`ngo_whatsapp_phone` is already stored in the DB and shown in the settings UI, but not yet used
for anything functional — Evolution API had too many rough edges to rely on it. When they sort out
the dashboard QR bug, button issues, and Baileys version handling, revisit whether the field can
drive anything useful.

**Version maintenance reminder**
`CONFIG_SESSION_PHONE_VERSION` in docker-compose.yml needs to stay in sync with the current Baileys
version (`baileys-version.json` on their repo). Meta occasionally forces old client versions off
the network — when that happens the symptom is Baileys connecting and immediately failing with no
QR generated. Worth checking after any Evolution API upgrade.

---

