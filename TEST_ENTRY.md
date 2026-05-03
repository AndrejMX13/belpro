# Test Entry Helper

When testing the manager WhatsApp approval flow without a third phone number, use a test entry endpoint instead of going through the full volunteer → Whisper → n8n pipeline.

## What to build

A FastAPI endpoint (e.g. `POST /test/inject-entry`) that:
1. Inserts a realistic `work_entries` row with status `pending_manager` into the DB (linked to a real volunteer in the DB)
2. Fires the same n8n webhook that the real volunteer flow would trigger, so the manager receives the WhatsApp notification normally

No special-casing in main code — just a test helper that bypasses voice recognition and volunteer-side automation.

## Testing phases

| Phase | Numbers needed | What is tested |
|-------|---------------|----------------|
| 1 | Belpro bot + tester phone (volunteer) | Full volunteer WhatsApp flow → approve via web dashboard |
| 2 | Belpro bot + tester phone (manager) | Manager receives WhatsApp notification → approves/rejects via WhatsApp |

Phase 2 uses the injected test entry instead of a real volunteer submission.

## Context

Volunteer and manager cannot share the same WhatsApp number — n8n routes messages by sender phone lookup against `volunteers.phone` and `managers.phone`. Same number = routing conflict.
