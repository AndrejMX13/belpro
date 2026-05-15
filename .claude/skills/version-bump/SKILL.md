---
name: version-bump
description: "Guide through a BelPro version bump. Use when the user asks to bump the version, cut a release, or do a version bump. Covers: version suggestion, file updates (main.py, CHANGELOG, SPEC, README), pre-commit review, optional tagging, optional GitHub release note drafting, and optional container rebuild."
metadata:
  role: procedure
  scope: project
  domain: release
---

# BelPro Version Bump

A step-by-step release procedure for BelPro. Work through each step in order. Pause for explicit user confirmation at every decision point — never commit, tag, or execute a command without approval.

---

## Step 0 — Pre-flight: test suite check

Check the conversation context first.

- If tests were run earlier in this session, note that and proceed without asking.
- If there is no evidence of a recent test run (new session, context was compacted): ask the user — "Have tests been run since the last code change?"
  - If yes: proceed.
  - If no: suggest running them and ask whether to run now or proceed anyway:
    ```
    docker compose exec api pytest tests/ -v
    ```
    Do not block on this — it is the user's call.

---

## Step 1 — Orient and suggest version

1. Read `__version__` from `api/main.py`.
2. Read `CHANGELOG.md` — find the most recent section to understand the scope of changes since the last bump.
3. Suggest a new version string with a one-line rationale. Follow semantic versioning:
   - **patch** (x.y.Z): bug fixes only
   - **minor** (x.Y.0): new features, backwards-compatible
   - **major** (X.0.0): breaking changes
   - **prerelease suffix**: `-alpha.N`, `-beta.N`, `-rc.N`
4. Wait for user confirmation or override before proceeding.

---

## Step 2 — Update files

Work through each file in order. Update where needed; note explicitly if no change is required.

### `api/main.py`
Update `__version__` to the confirmed version string.

### `CHANGELOG.md`
Add a new section at the top (immediately below the `---` separator after the file header):

```
## [<version>] — <today's date YYYY-MM-DD>

### Added

### Changed

### Fixed

### Removed
```

Populate from the git log since the previous CHANGELOG entry:
```
git log <previous-version-tag>..HEAD --oneline
```
If no tag exists for the previous version, use the date of the previous CHANGELOG entry as a reference. Remove any empty sections (Added/Changed/Fixed/Removed) after populating.

### `SPEC.md`
Read the file. Check whether any behaviour described there has changed with this bump. If yes, update it. If unsure, ask the user.

### `README.md`
Read the file. Compare it against what changed in this bump:
- If anything described (features, setup steps, behaviour) has changed, suggest the update.
- If the version number appears explicitly, update it.
- If uncertain whether a change warrants a README mention, ask the user.

---

## Step 3 — Pre-commit review

1. Run `git status` and show the full output.
2. Flag anything unexpected:
   - **Untracked files that look committable** — ask: "Should this be staged?"
   - **Untracked files that look like generated/local output** — suggest: "Should this be added to `.gitignore`?"
   - **Modified files not yet staged** — ask: "Was this intentionally left out?"
   - **`.env` variants** — never stage; warn the user if one appears untracked.
3. Draft the commit message in this format and show it to the user:
   ```
   chore: bump version to <version>

   Co-Authored-By: <Model Name> <noreply@anthropic.com>
   ```
   Determine `<Model Name>` from the current session context (e.g. `Claude Sonnet 4.6`). If the model is unknown or third-party, use `AI Assistant <noreply@ai>` instead.
4. **Wait for explicit confirmation before committing.**
5. After approval, commit. Example (adapt to actual staged files):
   ```
   git add api/main.py CHANGELOG.md
   git commit -m "$(cat <<'EOF'
   chore: bump version to <version>

   Co-Authored-By: <Model Name> <noreply@anthropic.com>
   EOF
   )"
   ```
6. After the commit, remind the user: "Push the branch when ready: `git push central main`"

---

## Step 4 — Tag? (optional)

Ask: "Do you want to tag this commit as `v<version>`?"

- If **yes**:
  ```
  git tag v<version>
  ```
  Then ask: "Push the tag to central?"
  ```
  git push central v<version>
  ```
- If **no**: skip to Step 5.

---

## Step 5 — GitHub release? (optional, only if Step 4 was yes)

Ask: "Do you want to draft release notes for a GitHub release?"

- If **yes**:
  1. Ask: "What was the last version that had a GitHub release?" (user checks GitHub if unsure).
  2. Read all CHANGELOG entries from that version up to the current one and aggregate them.
  3. Propose formatted release notes. Use this structure:
     ```markdown
     ## What's new in <version>

     ### Added
     - ...

     ### Changed
     - ...

     ### Fixed
     - ...
     ```
     Discuss and revise with the user until they are happy.
  4. Remind: "GitHub releases are created manually via the web UI at github.com — paste the notes there."
- If **no**: skip.

---

## Step 6 — Offer container rebuild

Ask: "Do you want to rebuild the API container now so the new version appears in `/docs`?"

```
docker compose up -d --build api
```

Execute only if the user says yes.
