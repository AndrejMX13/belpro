---
source_file: "D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py"
type: "rationale"
community: "Community None"
location: "L35"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Return per-volunteer totals of approved entries for the given year/month.

## Connections
- [[EntryStatus]] - `uses` [INFERRED]
- [[LogEntry]] - `uses` [INFERRED]
- [[Manager]] - `uses` [INFERRED]
- [[MonthlyReportSummary]] - `uses` [INFERRED]
- [[NGOInfo]] - `uses` [INFERRED]
- [[SmtpNotConfiguredError]] - `uses` [INFERRED]
- [[Volunteer]] - `uses` [INFERRED]
- [[VolunteerMonthlySummary]] - `uses` [INFERRED]
- [[monthly_summary()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Community_None