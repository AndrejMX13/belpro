# Release notes — v0.12.0-beta.0

**Centralised error handling, automated install, configurable WhatsApp instance, and an expanded test suite.**

---

### Ops & reliability

- **n8n error handler sub-workflow (BelPro - Napake):** all n8n workflow exceptions are now automatically routed to a centralised error handler via n8n's `errorWorkflow` setting. Errors are written to the `error_log` table with a Slovenian human-readable title and structured detail — they show up as dashboard notifications like any other operational error.
- **Explicit logic error reporting in volunteer_entry:** manager-facing logic errors (e.g. approving when no entry is pending) are now explicitly reported to the error log, not just silently swallowed.
- **Backup retention floor:** ops sidecar always keeps the 5 newest backups regardless of the configured retention period — a safety net against misconfiguration deleting everything.

### Setup & installation

- **Automated n8n setup:** `setup.sh` now creates the three core n8n credentials (`BelPro Postgres`, `BelPro API (Basic Auth)`, `BelPro API Internal Key`) automatically via the n8n API, then imports all workflows. A fresh install no longer requires any manual n8n steps beyond WhatsApp (Evolution API) and SMTP — both of which require values that aren't available at install time.
- **Credentials documentation fixed:** `BelPro API (Basic Auth)` was missing from the credentials README entirely — a fresh install would have had broken workflows with no explanation. Added and corrected.

### Configuration

- **Configurable Evolution API instance name:** `evolution_instance_name` is now a setting in Sistemske nastavitve. Both the volunteer_entry and manager_approval workflows fetch it dynamically at runtime instead of using a hardcoded value — changing the instance no longer requires editing workflow JSON.

### n8n workflow fixes

- Fixed `Code: Parse Action` reading from the wrong upstream node in manager_approval.
- Fixed manual manager notification path missing a `Fetch Config` step.
- Fixed `instance_name` not being passed through `Build Msg` nodes, causing cross-node reference errors.

### Test suite

- Alembic migration roundtrip test on an isolated database (`belpro_test_migrations`).
- EMŠO stored encrypted and not exposed by API.
- Approve/reject on a `pending_volunteer` entry returns 409.
- Rejected hours excluded from monthly totals; all-rejected month returns 0 hours.
- Photo limit tests isolated to `tmp_path` via monkeypatch — never touch the real logo or photo directory.
- Password change test; migration fixture idempotency fix.

### Documentation

- Mermaid architecture diagrams (EN + SL) added to docs, rendered to SVG via `scripts/render_diagrams.py`.
- WhatsApp conversation flow table and pending-approvals screenshot added to README.
- SPEC updated to document the two-source error log architecture (ops sidecar + n8n sub-workflow).

---

**Full changelog:** [CHANGELOG.md](../CHANGELOG.md)
