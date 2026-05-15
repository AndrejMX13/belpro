# Design: BelPro Version-Bump Skill

**Date:** 2026-05-15
**Status:** Approved

---

## Purpose

A project-specific skill that guides the user through a version bump in BelPro, ensuring nothing is forgotten (CHANGELOG, file completeness, commit message review). Covers optional tagging and optional GitHub release drafting as independent, separate decisions.

---

## Trigger

User asks for a version bump (e.g. "let's do a version bump", "bump the version", "time to bump").

---

## Approach

Checklist-driven: the skill works through each step in order, executes the mechanical parts, and pauses for explicit confirmation at every decision point. No commit, tag, or release action is taken without the user's approval.

---

## Step-by-Step Flow

### Step 0 — Pre-flight: test suite check

1. Check conversation context first — if tests were run earlier in this session, note that and proceed without asking.
2. If there is no evidence of a recent test run (new session, context was compacted): ask the user whether tests have been run since the last code change.
   - If yes: proceed.
   - If no: suggest running them (`docker compose exec api pytest tests/ -v`) and ask whether to run now or proceed anyway. Do not block — this is the user's call.

### Step 1 — Orient and suggest version

1. Read `__version__` from `api/main.py`.
2. Read `CHANGELOG.md` — find the most recent entry to understand scope of changes since last bump.
3. Suggest a new version string with a one-line rationale (patch / minor / major / prerelease suffix), following semantic versioning.
4. Wait for user confirmation or override before proceeding.

### Step 2 — Update files

Work through each file in order. Update where needed; note explicitly if no change is required.

| File | What to check / update |
|------|------------------------|
| `api/main.py` | `__version__` string |
| `CHANGELOG.md` | New section: version, today's date, commits categorised under Added / Changed / Fixed / Removed |
| `SPEC.md` | Check if any described behaviour has changed and needs updating |
| `README.md` | Read the file and compare against what changed in this bump. If anything described there has changed (features, setup steps, behaviour), suggest the update. If the version number appears explicitly, update it. If uncertain whether a change warrants a README mention, ask. |

### Step 3 — Pre-commit review

1. Run `git status` — show all staged, unstaged, and untracked files.
2. Flag anything unexpected:
   - Untracked files that look like they should be committed — ask if they should be staged.
   - Untracked files that look like they should be ignored — suggest adding to `.gitignore`.
   - Modified files not yet staged — ask if they were intentionally left out.
3. Draft the commit message and show it to the user.
4. **Wait for explicit confirmation before committing.**
5. Commit only after approval.

### Step 4 — Tag? (optional)

Ask: "Do you want to tag this commit as `v<version>`?"

- If yes: create the tag locally. Ask if it should be pushed to `central`.
- If no: skip.

### Step 5 — GitHub release? (optional, only if Step 4 was yes)

Ask: "Do you want to draft release notes for a GitHub release?"

- If yes:
  1. Ask: "What was the last version that had a GitHub release?" (user checks GitHub if unsure).
  2. Aggregate all CHANGELOG entries from that version up to the current one.
  3. Propose formatted release notes — discuss and revise with the user before they paste into GitHub.
  4. Remind user that GitHub releases are created manually via the web UI.
- If no: done.

### Step 6 — Offer container rebuild

Offer the rebuild command regardless of whether a tag or release was created:

> "Do you want to rebuild the API container now so the new version appears in `/docs`?
> `docker compose up -d --build api`"

Execute only if the user says yes.

---

## BelPro-Specific Constraints

- Git remote is named `central`, not `origin`.
- All AI-assisted commits must include a `Co-Authored-By` trailer. Use the model identity from the current session context:
  - Anthropic models: `Co-Authored-By: <Model Name> <noreply@anthropic.com>` (e.g. `Claude Sonnet 4.6`)
  - Third-party or unknown model: `Co-Authored-By: AI Assistant <noreply@ai>`
- Never commit secrets. Version bump touches no secrets, but the unstaged-file review should flag any `.env` variants.
- Version string lives only in `api/main.py` (`__version__`). No other file embeds it programmatically.

---

## Reminders (skill mentions, does not execute)

- **Branch push:** After the commit step, remind the user to push the branch when ready (`git push central main`). The skill handles tag push separately in Step 4.

---

## Out of Scope

- Running the test suite (assumed done before the bump is initiated).
- Rebuilding Docker containers without asking (Step 6 offers it explicitly).
- Pushing the branch (execute — user decides when to push).
