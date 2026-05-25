# scripts/gen_diagrams_sl.py

> 32 nodes

## Key Concepts

- **BelPro - Odobritev Upravljalca (Manager Approval Workflow)** (13 connections) — `n8n/workflows/manager_approval.json`
- **Manager WhatsApp Approval Implementation Plan** (11 connections) — `docs/superpowers/plans/2026-05-07-manager-approval.md`
- **Manager WhatsApp Approval Workflow Design** (11 connections) — `docs/superpowers/specs/2026-05-07-manager-approval-design.md`
- **GET /api/log-entries (list_log_entries)** (10 connections) — `api/routers/log_entries.py`
- **PATCH /api/log-entries/{id}/notify (notify_log_entry)** (8 connections) — `api/routers/log_entries.py`
- **Shared LogEntry Data Structure (volunteer_id, work_date, hours, activity_description, location, status, raw_transcript)** (8 connections) — `api/routers/log_entries.py`
- **PATCH /api/log-entries/{id}/approve (approve_log_entry)** (7 connections) — `api/routers/log_entries.py`
- **PATCH /api/log-entries/{id}/reject (reject_log_entry)** (7 connections) — `api/routers/log_entries.py`
- **manager_approval n8n Workflow** (6 connections) — `docs/superpowers/plans/2026-05-07-manager-approval.md`
- **manager_approval.json n8n Workflow** (6 connections) — `docs/superpowers/specs/2026-05-07-manager-approval-design.md`
- **Evolution API WhatsApp** (4 connections) — `docs/evolution-lid-resolution.md`
- **n8n: PATCH /api/log-entries/{id}/approve** (4 connections) — `n8n/workflows/manager_approval.json`
- **n8n: PATCH /api/log-entries/{id}/reject** (4 connections) — `n8n/workflows/manager_approval.json`
- **volunteer_entry n8n Workflow** (3 connections) — `docs/superpowers/plans/2026-05-07-manager-approval.md`
- **Evolution API lid JID Resolution** (2 connections) — `docs/evolution-lid-resolution.md`
- **Volunteer Entry Workflow Manager Routing Change** (2 connections) — `docs/superpowers/specs/2026-05-07-manager-approval-design.md`
- **n8n Workflow Import Export Script Design** (2 connections) — `docs/superpowers/specs/2026-05-16-n8n-workflow-scripts-design.md`
- **n8n: GET /api/log-entries?status=pending_manager (Post-Action Queue Check)** (2 connections) — `n8n/workflows/manager_approval.json`
- **POST /api/log-entries/{id}/photos/base64 (upload_photo_base64)** (2 connections) — `api/routers/log_entries.py`
- **analytics_summary** (2 connections) — `api/routers/analytics.py`
- **scripts/n8n_workflows.py Import Export Script** (1 connections) — `docs/superpowers/specs/2026-05-16-n8n-workflow-scripts-design.md`
- **Evolution API and N8N Phone Identification Solutions** (1 connections) — `Evolution_API_and_N8N_phone_identification_solutions.pdf`
- **n8n: GET /api/log-entries?status=pending_manager (Manual Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: PATCH /api/log-entries/{id}/notify (Manual Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- **n8n: GET /api/log-entries?status=pending_manager (Auto Notify)** (1 connections) — `n8n/workflows/volunteer_entry.json`
- *... and 7 more nodes in this community*

## Relationships

- [[Code Reviewer Skill]] (8 shared connections)
- [[report_pdf.py]] (6 shared connections)
- [[connections]] (4 shared connections)
- [[GET /log-entries]] (3 shared connections)
- [[merge_semantic.py]] (1 shared connections)

## Source Files

- `Evolution_API_and_N8N_phone_identification_solutions.pdf`
- `api/routers/analytics.py`
- `api/routers/log_entries.py`
- `api/routers/reports.py`
- `docs/evolution-lid-resolution.md`
- `docs/superpowers/plans/2026-05-07-manager-approval.md`
- `docs/superpowers/specs/2026-05-07-manager-approval-design.md`
- `docs/superpowers/specs/2026-05-16-n8n-workflow-scripts-design.md`
- `frontend/js/analytics.js`
- `n8n/workflows/manager_approval.json`
- `n8n/workflows/volunteer_entry.json`

## Audit Trail

- EXTRACTED: 108 (86%)
- INFERRED: 18 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*