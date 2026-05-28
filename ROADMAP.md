# BelPro Roadmap

BelPro is a self-hosted system that helps Slovenian NGOs manage volunteer work diaries — collecting hours via WhatsApp, getting them approved, and generating the monthly reports required by law.

This page shows what's coming before the first stable release and what has already shipped.

---

## Coming up — v1.0

### Reliability
- ✓ Daily backups run automatically — no cron jobs, no manual setup, works on any operating system

### Manager experience
- ✓ Dashboard shows a live health summary of all services — enough to diagnose a problem over the phone without opening Docker
- ✓ Errors in message delivery or report generation show up as notifications in the dashboard
- ✓ System upgrades handled by a single script — no missed steps


### Security & data protection
- ✓ Login sessions protected against script-based attacks on the local network
- ✓ Photo uploads per entry are limited to a sensible maximum
- ✓ Photos are automatically cleaned up after the legal retention period
- ✓ EMŠO validated with checksum at entry — a bad number is caught immediately, not days later
- ✓ Tax number (davčna) validated with checksum at entry
- ✓ A safe procedure exists for rotating the encryption key if ever needed
- ✓ GDPR consent document generated for each volunteer, ready to print and sign

### System architecture
- ✓ Central service for loading configuration settings related to the application

### Polish
- ✓ NGO logo appears on the dashboard and on all printed documents
- ✓ Dashboard screenshots added to documentation
- ✓ Example PDF reports added to documentation (consolidated manager report + per-volunteer CSD report)

---

## Done

- v0.12.0-beta — centralised n8n error handler sub-workflow (BelPro - Napake) routing all workflow exceptions to the error log; explicit logic error path in volunteer entry; automated credential creation and workflow import in setup.sh; configurable Evolution API instance name from admin UI

- v0.11.1-beta — configurable cron schedule (report day/period/hour, backup hour, cleanup hour, retention period) from admin UI without container restart; ops notification server; report delivery error visibility; dashboard screenshot gallery in README

- v0.11.0-beta — ops sidecar (automated nightly backup + photo cleanup), error log with dashboard notifications, live health widget on the admin page, GDPR consent PDF, settings table with runtime-tunable config, n8n photo confirmation fixes

- v0.10.2-beta — PDF report archive (all previously generated reports listed on the reports page and downloadable at any time)

- v0.10.0-beta — full volunteer entry flow via WhatsApp voice notes, manager approval dashboard, monthly PDF report generation and delivery, photo uploads with EXIF support, AES-256-GCM EMŠO encryption, backup and restore scripts, full automated test suite

---

## On the radar (post-1.0)

- **Emergency SMS alert** — when something breaks and nobody is logged into the dashboard, send an alert via the router's built-in SIM gateway, independent of the WAN connection (ISS-025)

- **Volunteer feedback when Whisper is unreachable** — currently the volunteer receives no reply and has no way of knowing their voice note was not processed; add an error-handler branch that sends a WhatsApp message asking them to retry with a text message

- **Atomic photo batch handling** — when a volunteer sends multiple photos at once that collectively exceed the limit, reject the entire batch and prompt to re-send within the remaining slots, rather than accepting some and rejecting others individually

- **Single public port for Evolution API** — route inbound WhatsApp webhooks through nginx so only port 80 needs to be open externally, instead of exposing 8180 as well

- **Whisper concurrent transcription** — the service intentionally runs single-threaded (serialises requests, avoids OOM); a Redis-backed task queue would improve burst latency but adds significant complexity — implement only if a real deployment reports it as a problem
- **Evolution API deeper integration** — the connected WhatsApp number is already observed, stored (`ngo_whatsapp_phone`), and auto-synced from Evolution API whenever the instance is in `open` state; the settings page shows it as read-only when connected and provides a direct link to the Evolution API admin. What is not yet possible: (1) pre-configuring the phone number from our side — Evolution API owns the number and we can only read it back after connection; (2) interactive message buttons — not supported in Evolution API v2.3.7 which the current stack uses, so confirmation dialogs are plain-text numbered menus. Both improvements depend on a stable Evolution API version that reliably supports phone pre-configuration and the buttons API.
- **Manager signature and stamp on documents** — held until a real user asks for it
- **Conversation state table** — replace in-workflow JS state management with a persistent `conversation_state` DB table; prerequisite for ISS-018 (partial extraction recovery) and eventual workflow decomposition into focused sub-workflows
- **Incomplete voice note recovery (ISS-018)** — when extraction misses a field, prompt the volunteer for just that piece rather than re-recording everything; requires conversation state table first
