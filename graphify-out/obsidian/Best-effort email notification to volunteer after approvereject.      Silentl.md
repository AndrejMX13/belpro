---
source_file: "D:\Andrej\vsCode-workspace\BelPro\api\routers\log_entries.py"
type: "rationale"
community: "Community None"
location: "L40"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Best-effort email notification to volunteer after approve/reject.      Silentl

## Connections
- [[EntryStatus]] - `uses` [INFERRED]
- [[LogEntry]] - `uses` [INFERRED]
- [[LogEntryCreate]] - `uses` [INFERRED]
- [[LogEntryListResponse]] - `uses` [INFERRED]
- [[LogEntryPhoto]] - `uses` [INFERRED]
- [[LogEntryResponse]] - `uses` [INFERRED]
- [[LogEntryUpdate]] - `uses` [INFERRED]
- [[Manager]] - `uses` [INFERRED]
- [[PhotoResponse]] - `uses` [INFERRED]
- [[SmtpNotConfiguredError]] - `uses` [INFERRED]
- [[Volunteer]] - `uses` [INFERRED]
- [[_notify_volunteer_email()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Community_None