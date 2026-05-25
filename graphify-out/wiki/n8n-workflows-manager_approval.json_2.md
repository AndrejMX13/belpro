# n8n/workflows/manager_approval.json

> God node · 31 connections · `n8n/workflows/manager_approval.json`

**Community:** [[n8n/workflows/manager_approval.json]]

## Connections by Relation

### calls
- [[GET /api/log-entries (list_log_entries)]] `EXTRACTED`
- [[GET /api/managers/me (get_manager)]] `EXTRACTED`
- [[PATCH /api/log-entries/{id}/approve (approve_log_entry)]] `EXTRACTED`
- [[PATCH /api/log-entries/{id}/reject (reject_log_entry)]] `EXTRACTED`

### calls_as_sub_workflow
- [[n8n/workflows/volunteer_entry.json]]

### contains
- [[connections]] `EXTRACTED`
- [[activeVersion]] `EXTRACTED`
- [[settings]] `EXTRACTED`
- [[pinData]] `EXTRACTED`
- [[updatedAt]] `EXTRACTED`
- [[createdAt]] `EXTRACTED`
- [[id]] `EXTRACTED`
- [[name]] `EXTRACTED`
- [[description]] `EXTRACTED`
- [[active]] `EXTRACTED`
- [[isArchived]] `EXTRACTED`
- [[nodes]] `EXTRACTED`
- [[staticData]] `EXTRACTED`
- [[meta]] `EXTRACTED`
- [[versionId]] `EXTRACTED`
- [[activeVersionId]] `EXTRACTED`
- [[versionCounter]] `EXTRACTED`
- [[triggerCount]] `EXTRACTED`
- [[shared]] `EXTRACTED`
- [[tags]] `EXTRACTED`

### implements
- [[Manager WhatsApp Approval Implementation Plan]] `EXTRACTED`
- [[manager_approval n8n Workflow]] `EXTRACTED`

### imports_or_exports
- [[scripts/n8n_workflows.py]]

### sends_whatsapp_notifications_via
- [[evolution-api]]

### specifies
- [[manager_approval.json n8n Workflow]] `EXTRACTED`

### updates_entry_status_via
- [[api]]

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*