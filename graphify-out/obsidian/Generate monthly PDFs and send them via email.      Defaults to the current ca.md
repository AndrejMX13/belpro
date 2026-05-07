---
source_file: "D:\Andrej\vsCode-workspace\BelPro\api\routers\reports.py"
type: "rationale"
community: "Community None"
location: "L171"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Generate monthly PDFs and send them via email.      Defaults to the current ca

## Connections
- [[EntryStatus]] - `uses` [INFERRED]
- [[LogEntry]] - `uses` [INFERRED]
- [[Manager]] - `uses` [INFERRED]
- [[MonthlyReportSummary]] - `uses` [INFERRED]
- [[NGOInfo]] - `uses` [INFERRED]
- [[SmtpNotConfiguredError]] - `uses` [INFERRED]
- [[Volunteer]] - `uses` [INFERRED]
- [[VolunteerMonthlySummary]] - `uses` [INFERRED]
- [[send_monthly_reports()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Community_None