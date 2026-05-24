---
name: feedback_issue_workflow
description: "How to handle issue markers, OPEN_ISSUES, ROADMAP ticks, and manual testing reminders at end of feature work"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d0df1aaf-d949-4f0a-a6a7-98526ac1d9e6
---

Keep ISS-NNN markers in commit messages — they're useful for later review and glue related commits together without needing a public tracker.

After all automated tests pass, remind the user to do manual testing before closing the issue. Phrase it as: "Ready for manual testing — once you're happy, delete the issue from OPEN_ISSUES and tick the Roadmap."

Only after the user confirms manual tests pass:
- Delete the issue entry from OPEN_ISSUES.md (don't mark as ✅ resolved — delete it entirely; deletion is more visible)
- Add the tick in ROADMAP.md

Either the user or Claude can do this final step — no preference, just don't do it before manual sign-off.

**Why:** Automated tests catch regressions but miss UX gaps and flow issues that only surface with real human use. Ticking the roadmap prematurely happened on ISS-015.

**How to apply:** At the end of any feature implementation, after tests pass, add a reminder: "Ready for manual testing. Once you've verified it in the browser, I can delete the issue and tick the Roadmap — or you can do it yourself."
