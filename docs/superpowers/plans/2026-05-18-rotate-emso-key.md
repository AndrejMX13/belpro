# EMŠO Key Rotation Script Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `scripts/rotate_emso_key.sh` (bash operator wrapper) and `api/scripts/rotate_emso_key.py` (Python rotation logic) — a one-off emergency tool that safely re-encrypts all stored EMŠOs from an old key to a new key in a single atomic DB transaction, with a targeted backup/restore safety net.

**Architecture:** The bash script handles the operator interface (warning banner, "save your old key" reminder, explicit confirmation, automatic full backup, targeted table backup, rotation, cleanup prompt). The Python script runs inside the api container and supports three modes via `--backup FILE` / `--restore FILE` / no-flag (rotate). The targeted backup writes `{old_key, volunteers rows}` as JSON to `/app/pdfs/temp/emso_rotation_TIMESTAMP.json` — within the existing `api_pdfs` named volume, so it survives container rebuilds. The directory is created on demand and deleted after the operator confirms everything is green. Restore reads the same file and rewrites `emso` + `emso_hash` for all rows in a single transaction, then prints the old key so the operator can revert `.env`. All underlying functions (`load_key`, `encrypt_emso`, `decrypt_emso`, `hash_emso`, `emso_checksum_valid`) are already tested — no new tests added (YAGNI).

**Tech Stack:** Bash (`set -euo pipefail`, same helpers as `upgrade.sh`), Python 3.11 (asyncpg, cryptography, json, argparse), Docker Compose v2 (`docker compose exec`)

---

## Pre-requisite: test data preparation

> **Dev environment only.** The rotation script validates the mod-11 checksum on every EMŠO after decryption. Test volunteers registered with made-up numbers will fail this check and abort the rotation. Run Task 0 once before testing. Skip in production — real data already has valid EMŠOs.

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `api/scripts/rotate_emso_key.py` | Three modes: backup, restore, rotate |
| Create | `scripts/rotate_emso_key.sh` | Operator UI: warnings, backup, rotation, cleanup |
| Modify | `README_SL.md` | Add to Vzdrževanje section + update scripts/ line |
| Modify | `README.md` | Add to Maintenance section + update scripts/ line |

---

### Task 0: Patch test volunteers with valid EMŠOs (dev only)

**Files:** none — DB-only operation, no committed changes.

**Context:** EMŠOs in the DB are AES-256-GCM encrypted. A plain SQL `UPDATE` with a plaintext value would corrupt the record. The command below runs inside the api container which already has `EMSO_ENCRYPTION_KEY` in its environment and the encryption service on its PYTHONPATH (`/app` is the working directory).

The following five EMŠOs are verified against the mod-11 formula in `api/utils/emso.py`:

| EMŠO            | total | mod | check |
|-----------------|-------|-----|-------|
| `0101905000005` | 72    | 6   | 5 ✓   |
| `1505006500003` | 129   | 8   | 3 ✓   |
| `0102805000004` | 73    | 7   | 4 ✓   |
| `0101755000001` | 76    | 10  | 1 ✓   |
| `2303685000008` | 113   | 3   | 8 ✓   |

If there are more than 5 test volunteers the list wraps (`i % 5`) — fine for a dev environment.

- [ ] **Step 1: Patch all test volunteers with valid encrypted EMŠOs**

Run from the project root (stack must be up):

```bash
docker compose exec -T api python - <<'PYEOF'
import asyncio, os
import asyncpg
from services.encryption import load_key, encrypt_emso, hash_emso

VALID_EMSOS = [
    "0101905000005",
    "1505006500003",
    "0102805000004",
    "0101755000001",
    "2303685000008",
]

async def main():
    key = load_key(os.environ["EMSO_ENCRYPTION_KEY"])
    db_url = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(db_url)
    rows = await conn.fetch("SELECT id FROM volunteers ORDER BY id")
    if not rows:
        print("No volunteers found.")
        return
    updates = [
        (encrypt_emso(VALID_EMSOS[i % len(VALID_EMSOS)], key),
         hash_emso(VALID_EMSOS[i % len(VALID_EMSOS)], key),
         str(row["id"]))
        for i, row in enumerate(rows)
    ]
    async with conn.transaction():
        for ct, h, vid in updates:
            await conn.execute(
                "UPDATE volunteers SET emso = $1, emso_hash = $2 WHERE id = $3::uuid",
                ct, h, vid,
            )
    print(f"Updated {len(updates)} volunteer(s) with valid EMSOs.")
    await conn.close()

asyncio.run(main())
PYEOF
```

Expected output: `Updated N volunteer(s) with valid EMSOs.`

- [ ] **Step 2: Verify one record decrypts to a valid EMŠO**

```bash
docker compose exec -T api python - <<'PYEOF'
import asyncio, os
import asyncpg
from services.encryption import load_key, decrypt_emso
from utils.emso import emso_checksum_valid

async def main():
    key = load_key(os.environ["EMSO_ENCRYPTION_KEY"])
    db_url = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(db_url)
    row = await conn.fetchrow("SELECT emso FROM volunteers LIMIT 1")
    if not row:
        print("No volunteers.")
        return
    plain = decrypt_emso(row["emso"], key)
    print(f"Decrypted: {plain[:4]}... valid={emso_checksum_valid(plain)}")
    await conn.close()

asyncio.run(main())
PYEOF
```

Expected output: `Decrypted: XXXX... valid=True`

---

### Task 1: Python rotation script

**Files:**
- Create: `api/scripts/rotate_emso_key.py`

**Context:**
- `WORKDIR /app` + `COPY . .` in the Dockerfile — `api/scripts/rotate_emso_key.py` becomes `/app/scripts/rotate_emso_key.py` in the container. Run as a script (`python /app/scripts/rotate_emso_key.py`), not imported as a module — no `__init__.py` needed.
- Imports resolve from `/app`: `from services.encryption import ...` → `/app/services/encryption.py`.
- `DATABASE_URL` in the container uses `postgresql+asyncpg://` — strip to `postgresql://` for asyncpg.
- **Three modes** selected via argparse:
  - `--backup FILE` — dump `{created_at, old_key, volunteers:[{id, emso, emso_hash}]}` to FILE. Reads `OLD_EMSO_KEY` from env (set by bash wrapper). Creates `/app/pdfs/temp/` if needed.
  - `--restore FILE` — read the JSON backup, restore `emso` + `emso_hash` for every row in a single transaction, print the old key so the operator can revert `.env`.
  - *(no flag)* — rotate: decrypt all with `OLD_EMSO_KEY`, validate checksums, re-encrypt with `NEW_EMSO_KEY`, single transaction, verify sample.
- `hash_emso(plaintext, key)` uses the key as the HMAC key — `emso_hash` must be updated alongside `emso` on both rotation and restore.

- [ ] **Step 1: Create the script**

```python
#!/usr/bin/env python3
"""EMŠO encryption key rotation — one-off emergency tool.

Run via scripts/rotate_emso_key.sh. Do not invoke directly.

Modes:
  (no flag)        rotate: re-encrypt all EMŠOs from OLD_EMSO_KEY to NEW_EMSO_KEY
  --backup FILE    dump targeted backup (old ciphertexts + old key) to FILE
  --restore FILE   restore ciphertexts from FILE backup

Exit codes: 0 success, 1 error.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import asyncpg

from services.encryption import decrypt_emso, encrypt_emso, hash_emso, load_key
from utils.emso import emso_checksum_valid

SAMPLE_VERIFY_COUNT = 5
TEMP_DIR = Path("/app/pdfs/temp")


def _db_url() -> str:
    return os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")


async def cmd_backup(out_path: Path) -> None:
    """Dump volunteers table + old key to out_path as JSON."""
    old_b64 = os.environ.get("OLD_EMSO_KEY", "")
    if not old_b64:
        print("NAPAKA: OLD_EMSO_KEY ni nastavljen.", file=sys.stderr)
        sys.exit(1)

    conn = await asyncpg.connect(_db_url())
    try:
        rows = await conn.fetch(
            "SELECT id, emso, emso_hash FROM volunteers ORDER BY id"
        )
        data = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "old_key": old_b64,
            "volunteers": [
                {"id": str(r["id"]), "emso": r["emso"], "emso_hash": r["emso_hash"]}
                for r in rows
            ],
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        out_path.chmod(0o600)
        print(f"Varnostna kopija shranjena: {out_path} ({len(rows)} zapisov)")
    finally:
        await conn.close()


async def cmd_restore(backup_path: Path) -> None:
    """Restore emso + emso_hash for all volunteers from backup_path."""
    if not backup_path.exists():
        print(f"NAPAKA: Datoteka {backup_path} ne obstaja.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(backup_path.read_text(encoding="utf-8"))
    volunteers = data["volunteers"]
    old_key_hint = data.get("old_key", "")

    conn = await asyncpg.connect(_db_url())
    try:
        async with conn.transaction():
            for v in volunteers:
                await conn.execute(
                    "UPDATE volunteers SET emso = $1, emso_hash = $2 WHERE id = $3::uuid",
                    v["emso"],
                    v["emso_hash"],
                    v["id"],
                )
        print(f"Obnovljenih {len(volunteers)} zapisov iz varnostne kopije.")
        print()
        print("OPOMNIK: Stari ključ (za .env):")
        print(f"  EMSO_ENCRYPTION_KEY={old_key_hint}")
        print("Posodobite .env in znova zaženite API vsebnik.")
    finally:
        await conn.close()


async def cmd_rotate(old_key: bytes, new_key: bytes) -> int:
    """Re-encrypt all EMŠOs from old_key to new_key. Returns count of rotated records."""
    conn = await asyncpg.connect(_db_url())
    try:
        rows = await conn.fetch("SELECT id, emso FROM volunteers ORDER BY id")

        if not rows:
            print("Ni prostovoljcev za posodobitev — zaključujem.")
            return 0

        total = len(rows)
        print(
            f"Najdenih {total} prostovoljcev. "
            "Dešifriranje in preverjanje s STARIM ključem ..."
        )

        # Phase 1: decrypt all, validate checksums — abort on first failure
        decrypted: dict[str, str] = {}
        for row in rows:
            vid = str(row["id"])
            try:
                plaintext = decrypt_emso(row["emso"], old_key)
            except Exception as exc:
                print(
                    f"NAPAKA: Dešifriranje za prostovoljca {vid} ni uspelo: {exc}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if not emso_checksum_valid(plaintext):
                print(
                    f"NAPAKA: EMŠO prostovoljca {vid} ni prestalo kontrolne vsote. Prekinjam.",
                    file=sys.stderr,
                )
                sys.exit(1)
            decrypted[vid] = plaintext

        print(
            f"Vseh {total} EMŠO vrednosti dešifriranih in preverjenih. "
            "Šifriranje z NOVIM ključem ..."
        )

        # Phase 2: re-encrypt and compute new hashes
        updates: list[tuple[str, str, str]] = [
            (encrypt_emso(pt, new_key), hash_emso(pt, new_key), vid)
            for vid, pt in decrypted.items()
        ]

        # Phase 3: write all in a single atomic transaction
        async with conn.transaction():
            for new_ct, new_hash, vid in updates:
                await conn.execute(
                    "UPDATE volunteers SET emso = $1, emso_hash = $2 WHERE id = $3::uuid",
                    new_ct,
                    new_hash,
                    vid,
                )

        print(f"Vseh {total} zapisov posodobljenih v eni transakciji.")

        # Phase 4: verify sample with new key
        sample_vids = list(decrypted.keys())[:SAMPLE_VERIFY_COUNT]
        print(f"Preverjanje {len(sample_vids)} vzorčnih zapisov z NOVIM ključem ...")
        for vid in sample_vids:
            row = await conn.fetchrow(
                "SELECT emso FROM volunteers WHERE id = $1::uuid", vid
            )
            if decrypt_emso(row["emso"], new_key) != decrypted[vid]:
                print(
                    f"NAPAKA: Preverjanje ni uspelo za prostovoljca {vid}!",
                    file=sys.stderr,
                )
                sys.exit(1)

        print(
            f"Vzorčno preverjanje uspešno. "
            f"Rotacija zaključena: {total} zapis(ov) rotiranih."
        )
        return total

    finally:
        await conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="EMSO key rotation tool")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--backup", metavar="FILE", help="Write targeted backup to FILE")
    group.add_argument("--restore", metavar="FILE", help="Restore from backup FILE")
    args = parser.parse_args()

    if args.backup:
        asyncio.run(cmd_backup(Path(args.backup)))
        return

    if args.restore:
        asyncio.run(cmd_restore(Path(args.restore)))
        return

    # Rotate mode
    old_b64 = os.environ.get("OLD_EMSO_KEY", "")
    new_b64 = os.environ.get("NEW_EMSO_KEY", "")

    if not old_b64:
        print("NAPAKA: OLD_EMSO_KEY ni nastavljen.", file=sys.stderr)
        sys.exit(1)
    if not new_b64:
        print("NAPAKA: NEW_EMSO_KEY ni nastavljen.", file=sys.stderr)
        sys.exit(1)
    if old_b64 == new_b64:
        print("NAPAKA: Oba ključa sta enaka — ni kaj zavrteti.", file=sys.stderr)
        sys.exit(1)

    try:
        old_key = load_key(old_b64)
    except ValueError as exc:
        print(f"NAPAKA: OLD_EMSO_KEY je neveljaven: {exc}", file=sys.stderr)
        sys.exit(1)
    try:
        new_key = load_key(new_b64)
    except ValueError as exc:
        print(f"NAPAKA: NEW_EMSO_KEY je neveljaven: {exc}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(cmd_rotate(old_key, new_key))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax check on host**

```bash
python -m py_compile api/scripts/rotate_emso_key.py && echo "OK"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add api/scripts/rotate_emso_key.py
git commit -m "feat(infra): add EMSO key rotation Python script"
```

---

### Task 2: Bash wrapper script

**Files:**
- Create: `scripts/rotate_emso_key.sh`

**Context:**
- Same style as `scripts/upgrade.sh` — same colour helpers, `set -euo pipefail`, `docker compose -f` pattern.
- **Two invocation modes:**
  - Rotate: `./scripts/rotate_emso_key.sh <OLD_KEY> <NEW_KEY>`
  - Restore: `./scripts/rotate_emso_key.sh --restore`
- Passing keys as positional args makes them briefly visible in `ps aux` — accepted trade-off for an emergency tool.
- **Pre-flight adds a prominent reminder** to write down the old key before proceeding — if the rotation succeeds but `.env` is then updated with a typo, the only recovery path is the targeted backup, which itself needs the old key printed in the restore output. Belt and suspenders.
- **Targeted backup path inside container:** `BACKUP_FILE="/app/pdfs/temp/emso_rotation_$(date +%Y%m%d_%H%M%S).json"` — within the `api_pdfs` named volume, persists across container rebuilds.
- **Restore mode** reads the backup path from the operator (prompted interactively), calls Python `--restore FILE`, then reminds operator to revert `.env` to old key and restart api.
- **Cleanup prompt** after successful rotation: asks operator to confirm everything is green before deleting the targeted backup.
- Key format/length validation delegated to Python (`load_key()`). Bash checks: two args, non-empty, non-identical.

- [ ] **Step 1: Create the script**

```bash
#!/usr/bin/env bash
# BelPro EMŠO key rotation script.
# ONE-TIME EMERGENCY TOOL — use only when the encryption key must be changed.
#
# Rotate:  ./scripts/rotate_emso_key.sh <OLD_KEY> <NEW_KEY>
# Restore: ./scripts/rotate_emso_key.sh --restore
#
# Both keys are base64url-encoded 32-byte AES-256 keys (EMSO_ENCRYPTION_KEY value).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE="docker compose -f $PROJECT_DIR/docker-compose.yml"
ENV_FILE="$PROJECT_DIR/.env"

# ── Colours (matches setup.sh / upgrade.sh) ────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}▸${RESET} $*"; }
ok()      { echo -e "${GREEN}✓${RESET} $*"; }
warn()    { echo -e "${YELLOW}!${RESET} $*"; }
heading() { echo -e "\n${BOLD}$*${RESET}"; }
die()     { echo -e "${RED}NAPAKA:${RESET} $*" >&2; exit 1; }

# ── Banner ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${RED}${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
echo -e "${RED}${BOLD}║     BelPro — Rotacija ključa za šifriranje EMŠO      ║${RESET}"
echo -e "${RED}${BOLD}║        ENKRATNO ORODJE — NE ZA REDNO VZDRŽEVANJE      ║${RESET}"
echo -e "${RED}${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
echo ""

# ── Pre-flight ─────────────────────────────────────────────────────────────
heading "0. Preverjanje zahtev"

[[ -f "$ENV_FILE" ]] || die ".env ni najden na $ENV_FILE."
command -v docker &>/dev/null || die "Docker ni nameščen."
docker info &>/dev/null       || die "Docker daemon ne teče. Zaženite Docker Desktop."
docker compose version &>/dev/null || die "Docker Compose ni na voljo."

if ! $COMPOSE ps api 2>/dev/null | grep -q "running\|Up"; then
  die "API vsebnik ne teče. Zaženite stack: docker compose up -d"
fi
ok "Pogoji so izpolnjeni."

# ── Restore mode ───────────────────────────────────────────────────────────
if [[ "${1:-}" == "--restore" ]]; then
  heading "OBNOVITEV IZ VARNOSTNE KOPIJE"
  echo ""
  warn "Ta operacija bo prepisala vse EMŠO zapise s podatki iz varnostne kopije."
  echo ""
  read -r -p "  Pot do datoteke varnostne kopije (znotraj vsebnika, npr. /app/pdfs/temp/emso_rotation_....json): " BACKUP_FILE
  [[ -n "$BACKUP_FILE" ]] || die "Pot do datoteke je prazna."
  echo ""
  read -r -p "  Nadaljujem z obnovo? Vpišite 'DA' za nadaljevanje: " confirm
  [[ "$confirm" == "DA" ]] || die "Obnovitev prekinjena."

  info "Zaganjam obnovitev ..."
  $COMPOSE exec -T api python /app/scripts/rotate_emso_key.py --restore "$BACKUP_FILE" \
    || die "Obnovitev ni uspela. Preverite zgornje napake."
  ok "Obnovitev uspešna."
  echo ""
  warn "Ne pozabite posodobiti EMSO_ENCRYPTION_KEY v .env na STARI ključ (izpisan zgoraj)"
  warn "in znova zagnati API vsebnik: docker compose up -d api"
  echo ""
  exit 0
fi

# ── Rotate mode: argument validation ──────────────────────────────────────
[[ $# -eq 2 ]] || die "Uporaba: $0 <STAR_KLJUC> <NOV_KLJUC>
       ali: $0 --restore
  STAR_KLJUC — trenutna vrednost EMSO_ENCRYPTION_KEY v .env
  NOV_KLJUC  — nov ključ, ustvarite z:
               python3 -c \"import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())\""

OLD_KEY="$1"
NEW_KEY="$2"

[[ -n "$OLD_KEY" ]] || die "STAR_KLJUC ne sme biti prazen."
[[ -n "$NEW_KEY" ]] || die "NOV_KLJUC ne sme biti prazen."
[[ "$OLD_KEY" != "$NEW_KEY" ]] || die "Oba ključa sta enaka — ni kaj zavrteti."

# ── Warning + confirmation ─────────────────────────────────────────────────
heading "! OPOZORILO"
echo ""
warn "PRED nadaljevanjem si zapišite trenutni stari ključ na varno mesto:"
echo ""
echo -e "  ${BOLD}EMSO_ENCRYPTION_KEY=${OLD_KEY}${RESET}"
echo ""
warn "Brez starega ključa ne morete obnoviti podatkov, če gre kaj narobe."
echo ""
warn "Ta operacija je DESTRUKTIVNA in NEPOPRAVLJIVA:"
echo "  • Vsi šifrirani EMŠO zapisi bodo prepisani z novim ključem."
echo "  • Po rotaciji MORATE posodobiti EMSO_ENCRYPTION_KEY v .env"
echo "    in znova zagnati API vsebnik."
echo ""
read -r -p "  Stari ključ sem si zapomnil/a in razumem tveganje. Vpišite 'DA' za nadaljevanje: " confirm
[[ "$confirm" == "DA" ]] || die "Rotacija prekinjena."

# ── Full backup ────────────────────────────────────────────────────────────
heading "1. Polna varnostna kopija"
info "Zaganjam backup.sh ..."
bash "$SCRIPT_DIR/backup.sh" || die "Varnostna kopija ni uspela — rotacija prekinjena."
ok "Polna varnostna kopija je shranjena."

# ── Targeted backup ───────────────────────────────────────────────────────
heading "2. Ciljna varnostna kopija tabele prostovoljcev"
BACKUP_FILE="/app/pdfs/temp/emso_rotation_$(date +%Y%m%d_%H%M%S).json"
info "Shranjujem varnostno kopijo v $BACKUP_FILE ..."
$COMPOSE exec -T \
  -e OLD_EMSO_KEY="$OLD_KEY" \
  api python /app/scripts/rotate_emso_key.py --backup "$BACKUP_FILE" \
  || die "Ciljna varnostna kopija ni uspela — rotacija prekinjena."
ok "Ciljna varnostna kopija je shranjena."

# ── Rotation ──────────────────────────────────────────────────────────────
heading "3. Rotacija ključa"
info "Zaganjam rotacijo znotraj API vsebnika ..."
$COMPOSE exec -T \
  -e OLD_EMSO_KEY="$OLD_KEY" \
  -e NEW_EMSO_KEY="$NEW_KEY" \
  api python /app/scripts/rotate_emso_key.py \
  || die "Rotacija ni uspela. Preverite zgornje napake — baza podatkov ni bila spremenjena."
ok "Rotacija je bila uspešna."

# ── Post-rotation steps ───────────────────────────────────────────────────
heading "4. Obvezni koraki po rotaciji"
echo ""
warn "Posodobi .env in znova zaženi API vsebnik — ZDAJ:"
echo ""
echo -e "  ${BOLD}1.${RESET} V .env nastavi:"
echo -e "     ${CYAN}EMSO_ENCRYPTION_KEY=${NEW_KEY}${RESET}"
echo ""
echo -e "  ${BOLD}2.${RESET} Znova zaženi API:"
echo -e "     ${CYAN}docker compose up -d api${RESET}"
echo ""
echo -e "  ${BOLD}3.${RESET} Preveri, da se API uspešno zažene:"
echo -e "     ${CYAN}docker compose logs api --tail 20${RESET}"
echo ""
echo -e "  ${BOLD}4.${RESET} Ko je vse zeleno, se vrni sem in potrdite brisanje varnostne kopije."
echo ""
echo -e "  Varnostna kopija je shranjena na: ${CYAN}${BACKUP_FILE}${RESET}"
echo -e "  Dostop: ${CYAN}docker compose exec api cat ${BACKUP_FILE}${RESET}"
echo ""
warn "Datoteka vsebuje stari šifrirni ključ in šifrirane podatke — je zaupna."
echo ""
read -r -p "  Je vse zeleno? Izbrišem varnostno kopijo? Vpišite 'DA' za brisanje: " cleanup
if [[ "$cleanup" == "DA" ]]; then
  $COMPOSE exec -T api rm -f "$BACKUP_FILE"
  $COMPOSE exec -T api rmdir /app/pdfs/temp 2>/dev/null || true
  ok "Varnostna kopija je izbrisana."
else
  warn "Varnostna kopija NI izbrisana. Ko bo vse v redu, jo izbrišite ročno:"
  warn "  docker compose exec api rm -f ${BACKUP_FILE}"
fi
echo ""
```

- [ ] **Step 2: Syntax check**

```bash
bash -n scripts/rotate_emso_key.sh
```

Expected: no output, exit 0.

- [ ] **Step 3: Make executable**

```bash
chmod +x scripts/rotate_emso_key.sh
```

- [ ] **Step 4: Commit**

```bash
git add scripts/rotate_emso_key.sh
git commit -m "feat(infra): add EMSO key rotation bash wrapper with backup and restore"
```

---

### Task 3: Documentation

**Files:**
- Modify: `README_SL.md`
- Modify: `README.md`

**Context:**
- Both READMEs have a Maintenance/Vzdrževanje section. Place the new subsection **last** — it is a rare emergency tool, not routine maintenance.
- `README_SL.md`: scripts/ line in project structure currently reads `# Skripte: setup.sh, upgrade.sh, backup.sh, restore.sh`.
- `README.md`: scripts/ line currently reads `# setup.sh, upgrade.sh, backup.sh, restore.sh`.

- [ ] **Step 1: Add to README_SL.md Vzdrževanje section**

Find the last subsection in `## Vzdrževanje` and append after it (before the next `##` heading):

```markdown
### Rotacija ključa za šifriranje EMŠO

**Enkratno orodje — samo v primeru nujne zamenjave šifrirnega ključa.**

```bash
bash scripts/rotate_emso_key.sh <STAR_KLJUC> <NOV_KLJUC>
```

`STAR_KLJUC` je trenutna vrednost `EMSO_ENCRYPTION_KEY` iz `.env`. `NOV_KLJUC` je nov ključ, ustvarjen z:

```bash
python3 -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
```

Skripta pred rotacijo **samodejno naredi polno varnostno kopijo** in **ciljno kopijo tabele prostovoljcev** (z vključenim starim ključem) v `/app/pdfs/temp/`. Po uspešni rotaciji vas vodi skozi posodobitev `.env` in ponovni zagon API vsebnika. Ko potrdite, da je vse v redu, ponudi brisanje zaupne varnostne kopije.

Obnovitev (če gre kaj narobe po rotaciji):

```bash
bash scripts/rotate_emso_key.sh --restore
```
```

- [ ] **Step 2: Update scripts/ line in README_SL.md project structure**

Find:
```
├── scripts/                # Skripte: setup.sh, upgrade.sh, backup.sh, restore.sh
```

Replace with:
```
├── scripts/                # Skripte: setup.sh, upgrade.sh, backup.sh, restore.sh, rotate_emso_key.sh
```

- [ ] **Step 3: Add to README.md Maintenance section**

Find the last subsection in `## Maintenance` and append after it (before the next `##` heading):

```markdown
### EMŠO Key Rotation

**Emergency tool — use only when the encryption key must be replaced.**

```bash
bash scripts/rotate_emso_key.sh <OLD_KEY> <NEW_KEY>
```

`OLD_KEY` is the current `EMSO_ENCRYPTION_KEY` from `.env`. Generate a new key with:

```bash
python3 -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
```

The script takes a full backup, creates a targeted backup of the volunteers table (including the old key) in `/app/pdfs/temp/`, re-encrypts all EMŠOs in a single atomic transaction, verifies a sample, then guides you through updating `.env` and restarting the api container. Once you confirm everything is green it offers to delete the sensitive backup file.

To restore if something goes wrong after rotation:

```bash
bash scripts/rotate_emso_key.sh --restore
```
```

- [ ] **Step 4: Update scripts/ line in README.md project structure**

Find:
```
├── scripts/                # setup.sh, upgrade.sh, backup.sh, restore.sh
```

Replace with:
```
├── scripts/                # setup.sh, upgrade.sh, backup.sh, restore.sh, rotate_emso_key.sh
```

- [ ] **Step 5: Commit**

```bash
git add README_SL.md README.md
git commit -m "docs: add EMSO key rotation to maintenance sections in both READMEs"
```

---

## Self-Review

**Spec coverage (against ISS-013):**
- ✅ Warn operator clearly — destructive, irreversible → red banner + "save your old key" block + `[[ "$confirm" == "DA" ]]`
- ✅ Validate both keys before touching anything → `main()` calls `load_key()` on both; bash checks non-empty + non-identical
- ✅ Take automatic DB backup → bash calls `backup.sh` (full) + Python `--backup` (targeted) before any DB writes
- ✅ Decrypt every EMŠO with OLD_KEY and verify checksum — abort if any fails → Phase 1 in `cmd_rotate()`, `sys.exit(1)` on first failure
- ✅ Re-encrypt all with NEW_KEY in a single DB transaction → Phase 3, `async with conn.transaction()`
- ✅ Verify sample before reporting success → Phase 4, `SAMPLE_VERIFY_COUNT = 5`
- ✅ Report count of rotated records → printed at end of `cmd_rotate()`
- ✅ Documented as one-time emergency tool → bash banner + README placement (last subsection) + wording

**Additional coverage (beyond spec):**
- ✅ Targeted backup with old key included → `cmd_backup()` writes JSON to `/app/pdfs/temp/`
- ✅ Restore mode → `cmd_restore()` + bash `--restore` path
- ✅ Cleanup prompt → operator confirms before backup deletion
- ✅ Old key printed prominently before confirmation → operator cannot miss it

**Placeholder scan:** No TBDs, no vague steps — all code blocks are complete.

**Type consistency:**
- `cmd_rotate(old_key: bytes, new_key: bytes) -> int` — defined and called consistently
- `cmd_backup(out_path: Path) -> None` — `Path` used throughout, `out_path.parent.mkdir()`
- `cmd_restore(backup_path: Path) -> None` — `Path` used, `backup_path.exists()` guard
- `updates: list[tuple[str, str, str]]` — `(new_ct, new_hash, vid)` — Phase 2 → Phase 3
- `decrypted: dict[str, str]` — keyed by `str(row["id"])`, accessed in Phase 4
