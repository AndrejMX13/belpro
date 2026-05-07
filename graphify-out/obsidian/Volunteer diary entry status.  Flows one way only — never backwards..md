---
source_file: "api\models\log_entry.py"
type: "rationale"
community: "Community None"
location: "L33"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Volunteer diary entry status.  Flows one way only — never backwards.

## Connections
- [[Base]] - `uses` [INFERRED]
- [[EntryStatus]] - `rationale_for` [EXTRACTED]
- [[LogEntryPhoto]] - `uses` [INFERRED]
- [[Volunteer]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Community_None