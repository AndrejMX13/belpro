---
name: Commit the plan file after subagent-driven development
description: Plan files created in docs/superpowers/plans/ are not automatically committed by subagents — must be added manually at the end.
type: feedback
originSessionId: cb52b61d-67f2-4ef0-a1d9-112f8bbe20cf
---
After running superpowers:subagent-driven-development, the plan file in `docs/superpowers/plans/` is left untracked. Subagents only commit the files they explicitly create or modify — they are never told to add the plan document.

**Why:** The plan file is created by the controller (writing-plans skill) before subagents run, and no subagent task covers committing it.

**How to apply:** After all tasks complete and before the final push, check `git status docs/superpowers/plans/` and commit any untracked plan files. Do this as part of the finishing-a-development-branch step, or add it as a reminder at the end of subagent-driven runs.
