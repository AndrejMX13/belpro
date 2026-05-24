---
name: Run graphify update after code changes
description: graphify update . must be run at the end of every session that modifies code files — not optional
type: feedback
originSessionId: fb05c0f9-51cf-4b5a-abfb-32ff0916b5f7
---
Always run `graphify update .` from the project root at the end of any session where code files were modified.

**Why:** The CLAUDE.md rule is explicit about this, and skipping it leaves the knowledge graph stale. A stale graph means future sessions navigate the codebase from an outdated index, defeating the primary discovery tool.

**How to apply:** Treat it as a mandatory last step — same category as committing migration files. If a session modifies any `.py`, `.js`, `.css`, or `.html` file, run `graphify update .` before closing out the session. Do not wait for the user to ask.

**Commit format for graphify updates:** The commit title must summarise the session's work, with `— graphify update` appended. The body should describe what changed in the session. Example:

```
feat: report delivery error visibility — graphify update

Surface email and WhatsApp delivery failures in Docker logs and
Dnevnik napak. SmtpNotConfiguredError no longer aborts the batch.
4 new tests, all 210 passing.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Why:** A bare `graphify update` commit title gives no information about what changed — the graphify output files are secondary; what matters is what code change triggered them.

---

## Known version issue (2026-05-21)

graphify **0.4.23** was broken in two ways:
- `to_html()` crashed with `TypeError: expected string or bytes-like object, got 'NoneType'` on edges where `source_file=None`
- `to_wiki()` crashed with `UnicodeEncodeError` on Slovenian characters (missing `encoding='utf-8'` in file writes)

`python -m graphify update .` reported "Nothing to update or rebuild failed" and exited 1. The workaround was running the pipeline manually step by step.

**Fix:** upgrade to **0.8.14** (`pip install graphifyy==0.8.14`). Both bugs are gone and the command works cleanly end-to-end.

**Diagnostic:** if `graphify update .` fails, first check `pip show graphifyy` — if the version is behind, upgrading is likely the fix. Don't touch the version if the command is working cleanly.
