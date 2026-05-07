---
source_file: "D:\Andrej\vsCode-workspace\BelPro\api\routers\log_entries.py"
type: "rationale"
community: "Community None"
location: "L92"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Extract timestamp and GPS from image EXIF. All best-effort — never raises.

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
- [[_extract_exif()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Community_None