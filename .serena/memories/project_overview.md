# Belpro — Project Overview

**Purpose:** Self-hosted, single-tenant system for Slovenian NGOs to automate volunteer work diaries (*Dnevnik prostovoljskega dela*) required by law. Volunteers log hours via WhatsApp voice notes/photos. Manager approves via WhatsApp + web dashboard. Monthly PDF reports generated for CSD submission.

**Key constraints:**
- Single-tenant (one NGO per deployment)
- Slovenian language only
- No cloud storage — all data local
- EMŠO (Slovenian national ID) encrypted at rest (AES-256)
- Governed by ZVOP-2 / GDPR

**Spec:** `SPEC.md` — read before adding features
**Project instructions:** `CLAUDE.md`
