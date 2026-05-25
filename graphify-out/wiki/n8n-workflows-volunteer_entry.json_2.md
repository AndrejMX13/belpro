# n8n/workflows/volunteer_entry.json

> God node · 34 connections · `n8n/workflows/volunteer_entry.json`

**Community:** [[n8n/workflows/volunteer_entry.json]]

## Connections by Relation

### calls
- [[GET /api/log-entries (list_log_entries)]] `EXTRACTED`
- [[GET /api/managers/me (get_manager)]] `EXTRACTED`
- [[PATCH /api/log-entries/{id}/notify (notify_log_entry)]] `EXTRACTED`
- [[GET /api/volunteers/{id} (get_volunteer)]] `EXTRACTED`
- [[POST /api/log-entries (create_log_entry)]] `EXTRACTED`
- [[POST /api/log-entries/{id}/confirm (confirm_log_entry)]] `EXTRACTED`
- [[DELETE /api/log-entries/{id} (delete_log_entry)]] `EXTRACTED`
- [[GET /api/volunteers (list_volunteers)]] `EXTRACTED`
- [[GET /api/log-entries/{id} (get_log_entry)]] `EXTRACTED`

### calls_api_endpoints
- [[api]]

### calls_as_sub_workflow
- [[n8n/workflows/manager_approval.json]]

### calls_for_transcription
- [[whisper]]

### contains
- [[connections]] `EXTRACTED`
- [[activeVersion]] `EXTRACTED`
- [[settings]] `EXTRACTED`
- [[staticData]] `EXTRACTED`
- [[pinData]] `EXTRACTED`
- [[updatedAt]] `EXTRACTED`
- [[createdAt]] `EXTRACTED`
- [[id]] `EXTRACTED`
- [[name]] `EXTRACTED`
- [[description]] `EXTRACTED`
- [[active]] `EXTRACTED`
- [[isArchived]] `EXTRACTED`
- [[nodes]] `EXTRACTED`
- [[meta]] `EXTRACTED`
- [[versionId]] `EXTRACTED`
- [[activeVersionId]] `EXTRACTED`
- [[versionCounter]] `EXTRACTED`
- [[triggerCount]] `EXTRACTED`
- [[shared]] `EXTRACTED`
- [[tags]] `EXTRACTED`

### imports_or_exports
- [[scripts/n8n_workflows.py]]

### sends_whatsapp_via
- [[evolution-api]]

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*