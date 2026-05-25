# BelPro System Specification

> 17 nodes · cohesion 0.17

## Key Concepts

- **BelPro System Specification** (29 connections) — `SPEC.md`
- **DB Table: volunteers** (5 connections) — `SPEC.md`
- **WhatsApp Volunteer Entry Flow** (4 connections) — `SPEC.md`
- **Faster-Whisper (CPU Speech-to-Text)** (4 connections) — `SPEC.md`
- **Monthly PDF Reports Generation and Delivery** (3 connections) — `SPEC.md`
- **DB Table: log_entries** (3 connections) — `SPEC.md`
- **DB Table: monthly_reports** (3 connections) — `SPEC.md`
- **Entry Status Flow (pending_volunteer → pending_manager → approved/rejected)** (2 connections) — `SPEC.md`
- **DB Table: managers** (2 connections) — `SPEC.md`
- **DB Table: log_entry_photos** (2 connections) — `SPEC.md`
- **DB Table: settings** (2 connections) — `SPEC.md`
- **BelPro System Specification (Slovenian)** (1 connections) — `SPEC_SL.md`
- **CSD — Centre for Social Work** (1 connections) — `SPEC.md`
- **Single-Tenant Architecture** (1 connections) — `SPEC.md`
- **WeasyPrint (HTML to PDF)** (1 connections) — `CLAUDE.md`
- **DB Table: error_log** (1 connections) — `SPEC.md`
- **Whisper Single-Threaded Design (deliberate trade-off)** (1 connections) — `SPEC.md`

## Relationships

- [[Docker Compose (all services containerised)]] (9 shared connections)
- [[AppSettings — Runtime-Tunable Configuration (DB-first, env-fallback)]] (4 shared connections)
- [[EMŠO Encryption (AES-256-GCM at rest)]] (3 shared connections)
- [[BelPro README (English)]] (1 shared connections)
- [[CLAUDE.md — Project AI Instructions]] (1 shared connections)
- [[GDPR Consent PDF (Dogovor o prostovoljstvu)]] (1 shared connections)

## Source Files

- `CLAUDE.md`
- `SPEC.md`
- `SPEC_SL.md`

## Audit Trail

- EXTRACTED: 63 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*