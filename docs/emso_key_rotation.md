# EMŠO Encryption Key Rotation — Procedure Guide

This document covers everything you need to know before, during, and after rotating the EMŠO encryption key. Read it in full before starting.

---

## When to use this

Only when you need to replace the `EMSO_ENCRYPTION_KEY` — for example after a suspected key compromise or a security audit requirement. This is not routine maintenance. Under normal operation the key never needs to change.

---

## Prerequisites

All of the following must be true before you start:

- The full Docker stack is running (`docker compose ps` shows all services healthy).
- The `api` container image is **current** — it must have been built after `api/scripts/rotate_emso_key.py` was added to the repository. If you just cloned or pulled the repo, run `docker compose up -d --build api` before proceeding.
- You have a working terminal with access to the project directory.
- You have a second terminal window available for the mid-rotation steps (updating `.env` and restarting the container).

---

## Step 1 — Save the current key

Before generating anything, retrieve the current key and store it somewhere safe outside the terminal (password manager, encrypted note):

```bash
grep EMSO_ENCRYPTION_KEY .env
```

Write it down. Without it, you cannot roll back if something goes wrong.

---

## Step 2 — Generate a new key

Generate the new key into a shell variable so you avoid copy-paste errors. A base64url-encoded 32-byte key must be exactly **44 characters** (43 data + one `=` padding).

```bash
NEW_KEY=$(python3 -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())")

# Verify: must print 44
echo -n "$NEW_KEY" | wc -c

# Show the key so you can also save it
echo "$NEW_KEY"
```

Save the new key alongside the old one before continuing.

---

## Step 3 — Run the rotation script

Pass the old key directly and the new key via the variable:

```bash
bash scripts/rotate_emso_key.sh <OLD_KEY> "$NEW_KEY"
```

Replace `<OLD_KEY>` with the value from Step 1.

The script will:

1. Ask you to confirm you have the old key saved — type `DA`.
2. Take a full database backup automatically.
3. Create a targeted backup of the volunteers table (with the old key) inside the container at `/app/pdfs/temp/`.
4. Validate every stored EMŠO (checksum + format) before touching anything.
5. Re-encrypt all EMŠOs with the new key in a single atomic transaction.
6. Verify a sample of re-encrypted records before committing.
7. **Pause** — and instruct you to complete Steps 4 and 5 before typing anything further.

---

## Step 4 — Update `.env` and restart the API (while script is paused)

Open a **second terminal**, then:

```bash
# Edit .env — change EMSO_ENCRYPTION_KEY to the new value
# Then restart the api container:
docker compose up -d api

# Verify it started cleanly:
docker compose logs api --tail 20
```

Look for the startup line confirming the API is listening. There should be no errors about encryption or database connectivity.

---

## Step 5 — Confirm cleanup in the first terminal

Once the API is verified healthy in the second terminal, return to the first terminal and answer the cleanup prompt with `DA`.

The script will delete the targeted backup file from `/app/pdfs/temp/`. That file contains the old encryption key and the old ciphertext — treat it as sensitive for as long as it exists.

---

## If something goes wrong

If the rotation fails mid-way, the database is not changed — the Python script uses an all-or-nothing transaction. Your old key still works. Simply fix the problem and re-run.

If the rotation succeeded but the API fails to start with the new key:

```bash
bash scripts/rotate_emso_key.sh --restore
```

The script will prompt for the path to the targeted backup file (printed during the rotation run, e.g. `/app/pdfs/temp/emso_rotation_20260518_170050.json`). It will restore the old ciphertext in a single transaction. After restore, set `EMSO_ENCRYPTION_KEY` back to the old value in `.env` and restart the API.

---

## Known issues encountered during development

These were discovered during the first live test and are already fixed in the codebase — recorded here for reference:

| Problem | Cause | Fix applied |
|---------|-------|-------------|
| `No module named 'services'` | `docker compose exec` does not use the container's `WORKDIR` as the Python path | Script now passes `-e PYTHONPATH=/app` on all exec calls |
| `Invalid base64-encoded string` | `load_key()` used `base64.b64decode` which rejects `-` and `_` from base64url keys | `load_key()` now normalises `-`→`+` and `_`→`/` before decoding |
| Key mangled by copy-paste | Terminal line-wrapping or clipboard truncation drops characters | Generate key into a shell variable and pass it as `"$NEW_KEY"` |
| `No such file or directory` for the Python script | Container image was built before the script was added to the repo | Always run `docker compose up -d --build api` after a fresh clone or pull |
