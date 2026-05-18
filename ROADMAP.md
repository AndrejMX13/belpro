# BelPro Roadmap

BelPro is a self-hosted system that helps Slovenian NGOs manage volunteer work diaries — collecting hours via WhatsApp, getting them approved, and generating the monthly reports required by law.

This page shows what's coming before the first stable release and what has already shipped. For the technical detail behind each item, see `OPEN_ISSUES.md`.

---

## Coming up — v1.0

### Reliability
- Multiple volunteers can submit voice notes at the same time without stepping on each other
- If a voice note isn't understood, the system guides the volunteer through fixing just the missing part — not re-recording everything
- Daily backups run automatically — no cron jobs, no manual setup, works on any operating system

### Manager experience
- Dashboard shows a live health summary of all services — enough to diagnose a problem over the phone without opening Docker
- Errors in message delivery or report generation show up as notifications in the dashboard
- System upgrades handled by a single script — no missed steps

### Security & data protection
- Login sessions protected against script-based attacks on the local network
- Photo uploads per entry are limited to a sensible maximum
- Photos are automatically cleaned up after the legal retention period
- EMŠO validated at entry — a bad number is caught immediately, not days later
- A safe procedure exists for rotating the encryption key if ever needed
- GDPR consent document generated for each volunteer, ready to print and sign

### Polish
- NGO logo appears on the dashboard and on all printed documents
- Documentation includes screenshots, example conversations, and a sample report

---

## Done

- v0.10.0-beta — full volunteer entry flow via WhatsApp voice notes, manager approval dashboard, monthly PDF report generation and delivery, photo uploads with EXIF support, AES-256-GCM EMŠO encryption, backup and restore scripts, full automated test suite

---

## On the radar (post-1.0)

- **WhatsApp phone number routing** — the NGO's WhatsApp number is already stored in settings but not yet used to drive anything; depends on Evolution API stabilising its multi-instance handling
- **Active push notification** — alerting the manager when something breaks and nobody is logged into the dashboard; requires a notification channel that survives the app being down
- **Manager signature and stamp on documents** — held until a real user asks for it
