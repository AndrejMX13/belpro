---
source_file: "D:\Andrej\vsCode-workspace\BelPro\api\routers\log_entries.py"
type: "rationale"
community: "Community None"
location: "L484"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Delete a pending_volunteer entry (cancelled or corrected by volunteer).

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
- [[delete_log_entry()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Community_None