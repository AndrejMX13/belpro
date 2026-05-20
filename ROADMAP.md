# BelPro Roadmap

BelPro is a self-hosted system that helps Slovenian NGOs manage volunteer work diaries — collecting hours via WhatsApp, getting them approved, and generating the monthly reports required by law.

This page shows what's coming before the first stable release and what has already shipped.

---

## Coming up — v1.0

### Reliability
- Daily backups run automatically — no cron jobs, no manual setup, works on any operating system

### Manager experience
- Dashboard shows a live health summary of all services — enough to diagnose a problem over the phone without opening Docker
- Errors in message delivery or report generation show up as notifications in the dashboard
- ✓ System upgrades handled by a single script — no missed steps

### Security & data protection
- ✓ Login sessions protected against script-based attacks on the local network
- ✓ Photo uploads per entry are limited to a sensible maximum
- Photos are automatically cleaned up after the legal retention period
- ✓ EMŠO validated with checksum at entry — a bad number is caught immediately, not days later
- ✓ Tax number (davčna) validated with checksum at entry
- ✓ A safe procedure exists for rotating the encryption key if ever needed
- ✓ GDPR consent document generated for each volunteer, ready to print and sign

### System architecure
- ✓ Central service for loading configuration settings related to the application

### Polish
- ✓ NGO logo appears on the dashboard and on all printed documents
- Documentation includes screenshots, example conversations, and a sample report

---

## Done

- v0.10.0-beta — full volunteer entry flow via WhatsApp voice notes, manager approval dashboard, monthly PDF report generation and delivery, photo uploads with EXIF support, AES-256-GCM EMŠO encryption, backup and restore scripts, full automated test suite

---

## On the radar (post-1.0)

- **Atomic photo batch handling** — when a volunteer sends multiple photos at once that collectively exceed the limit, reject the entire batch and prompt to re-send within the remaining slots, rather than accepting some and rejecting others individually

- **Whisper concurrent transcription** — the service intentionally runs single-threaded (serialises requests, avoids OOM); a Redis-backed task queue would improve burst latency but adds significant complexity — implement only if a real deployment reports it as a problem
- **WhatsApp phone number routing** — the NGO's WhatsApp number is already stored in settings but not yet used to drive anything; depends on Evolution API stabilising its multi-instance handling
- **Active push notification** — alerting the manager when something breaks and nobody is logged into the dashboard; requires a notification channel that survives the app being down
- **Manager signature and stamp on documents** — held until a real user asks for it
- **Conversation state table** — replace in-workflow JS state management with a persistent `conversation_state` DB table; prerequisite for ISS-018 (partial extraction recovery) and eventual workflow decomposition into focused sub-workflows
- **Incomplete voice note recovery (ISS-018)** — when extraction misses a field, prompt the volunteer for just that piece rather than re-recording everything; requires conversation state table first
