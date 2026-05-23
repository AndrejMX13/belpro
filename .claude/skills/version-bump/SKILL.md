---
name: version-bump
description: "Guide through a BelPro version bump. Use when the user asks to bump the version, cut a release, or do a version bump. Covers: version suggestion, file updates (main.py, CHANGELOG, SPEC, SPEC_SL, README, README_SL, ROADMAP), pre-commit review, optional tagging, optional GitHub release note drafting, and optional container rebuild."
metadata:
  role: procedure
  scope: project
  domain: release
---

# BelPro Version Bump

A step-by-step release procedure for BelPro. Work through each step in order.

**Hard rules — never break these:**
- **Do not commit anything until Step 3 is complete and the user has explicitly approved the commit message.**
- **Do not make intermediate commits during file updates.** All version bump changes go in one single commit.
- **Never push.** Pushing is always the user's responsibility. Do not offer to push, do not execute a push command.
- **Always show the full commit message and wait for explicit approval before running `git commit`.**

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

Work through each file in order. **Do not commit anything yet.** Update where needed; note explicitly if no change is required.

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
If no tag exists for the previous version:
```
git log --since="YYYY-MM-DD" --oneline
```
Use the date from the previous CHANGELOG section header as the `--since` value. Remove any empty sections (Added/Changed/Fixed/Removed) after populating.

### `SPEC.md`
Read the file. Check whether any behaviour described there has changed with this bump. If yes, update it. If unsure, ask the user.

### `SPEC_SL.md`
Apply the same changes made to `SPEC.md`, translated into Slovenian. Never update one without the other.

### `README.md`
Read the file. Compare it against what changed in this bump:
- If anything described (features, setup steps, behaviour) has changed, suggest the update.
- If the version number appears explicitly, update it.
- If uncertain whether a change warrants a README mention, ask the user.

### `README_SL.md`
Apply the same changes made to `README.md`, translated into Slovenian. Never update one without the other.

### `ROADMAP.md`
Read the file. Tick any items that are now complete (add `✓`) and move newly completed versions into the Done section if applicable. If unsure whether something is done, ask the user.

### `graphify-out/`
Check `git status` — if any `graphify-out/` files appear as modified, they must be included in the release commit. Do not skip them.

---

## Step 3 — Pre-commit review

1. Run `git status` and show the full output.
2. Flag anything unexpected:
   - **Untracked files that look committable** — ask: "Should this be staged?"
   - **Untracked files that look like generated/local output** — suggest: "Should this be added to `.gitignore`?"
   - **Modified files not yet staged** — ask: "Was this intentionally left out?"
   - **`.env` variants** — never stage; warn the user if one appears untracked.
3. Draft the commit message and show it to the user. The title should be `chore: release <version>`. The body should list all changed files and what was done in each, as bullet points. For a release with meaningful scope, this body is not optional — it is the changelog for the commit itself. Use this structure:

   ```
   chore: release <version>

   - Version bump: api/main.py __version__ → <version>
   - CHANGELOG: add <version> entry (<one-line summary of scope>)
   - SPEC / SPEC_SL: <what changed, if anything>
   - README / README_SL: <what changed, if anything>
   - ROADMAP: <what was ticked, if anything>
   - graphify-out: incremental update (if included)

   Co-Authored-By: <Model Name> <email>
   ```

   Determine the Co-Authored-By trailer from the current session context:
   - Anthropic model → `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` (use actual model name from context)
   - Third-party or unknown model → `Co-Authored-By: AI Assistant <noreply@ai>`

4. **Show the full message to the user and wait for explicit approval before doing anything else.**
5. After approval, stage all updated files and commit using the Bash tool:
   ```bash
   git add api/main.py CHANGELOG.md SPEC.md SPEC_SL.md README.md README_SL.md ROADMAP.md
   # also: git add graphify-out/ if modified
   git commit -m "$(cat <<'EOF'
   chore: release <version>

   - ...bullet points...

   Co-Authored-By: <Model Name> <email>
   EOF
   )"
   ```

---

## Step 4 — Tag? (optional)

Ask: "Do you want to tag this commit as `v<version>`?"

- If **yes**:
  ```
  git tag v<version>
  ```
  Note: pushing the tag is the user's responsibility, same as pushing commits.
- If **no**: skip to Step 5.

---

## Step 5 — GitHub release? (optional, only if Step 4 was yes)

Ask: "Do you want to draft release notes for a GitHub release?"

If Step 4 was skipped (no tag was created), note this: "GitHub releases are typically tied to a tag. Should we go back and create the tag first, or do you want to draft the notes now for later use?"

- If **yes**:
  1. Ask: "What was the last version that had a GitHub release?" (user checks GitHub if unsure).
  2. Run `git log <last-release-tag>..HEAD --oneline` and read all relevant CHANGELOG entries from that version up to the current one.
  3. Propose formatted release notes. When the release covers many changes across multiple versions, use **thematic grouping** rather than Added/Changed/Fixed — it reads better for a large release. Example structure:

     ```markdown
     **<one-line summary of what this release is about>**

     ### <Theme 1 — e.g. Ops & reliability>
     - ...

     ### <Theme 2 — e.g. Manager dashboard>
     - ...

     ### <Theme N>
     - ...

     ---
     **Full changelog:** [CHANGELOG.md](CHANGELOG.md)
     ```

     For a small patch release, Added/Changed/Fixed is fine.

  4. Save the release notes to `docs/release-notes-v<version>.md` for easy pasting into the GitHub release UI.
  5. Remind: "GitHub releases are created manually via the web UI — open the release, paste from `docs/release-notes-v<version>.md`."
- If **no**: skip.

---

## Step 6 — Offer container rebuild

Ask: "Do you want to rebuild the API container now so the new version appears in `/docs`?"

```
docker compose up -d --build api
```

Execute only if the user says yes.
