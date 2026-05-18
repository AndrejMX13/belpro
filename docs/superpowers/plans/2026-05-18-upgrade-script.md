# Upgrade Script Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `scripts/upgrade.sh` — an idempotent, safe upgrade script that pulls the latest code, rebuilds Docker images, runs Alembic migrations, and health-checks the stack before declaring success.

**Architecture:** Single Bash script following the exact style of the existing `scripts/setup.sh` (same colour helpers, same `set -euo pipefail`, same `docker compose -f` pattern). Steps are ordered to be safe: pre-flight → backup → git pull → rebuild → wait for postgres → wait for API → migrate → health check → summary. Idempotent: running it when already up-to-date is harmless (Docker layer cache makes rebuild fast; Alembic is a no-op at head).

**Tech Stack:** Bash, Docker Compose v2, git, Alembic (via `docker compose exec`), curl (inside the api container)

---

## File Map

| Action | Path | Responsibility |
|--------|------|---------------|
| Create | `scripts/upgrade.sh` | Full upgrade orchestration |
| Modify | `README_SL.md` | Add upgrade.sh to Maintenance section |

---

### Task 1: Script skeleton — shebang, helpers, pre-flight checks

**Files:**
- Create: `scripts/upgrade.sh`

**Context:** The existing `scripts/setup.sh` defines the colour helpers (`info`, `ok`, `warn`, `heading`, `die`) and the `get_env` helper that reads a value from `.env`. Copy these verbatim — do not reinvent them. The git remote is named `central`, not `origin` (project convention). Pre-flight must check: `.env` exists, Docker is running, Docker Compose is available, and warn (with confirmation prompt) if there are uncommitted local changes that would block `git pull`.

- [ ] **Step 1: Create the file with skeleton**

```bash
#!/usr/bin/env bash
# BelPro upgrade script.
# Run from the project root: ./scripts/upgrade.sh
# Pulls latest code, rebuilds images, runs migrations, health-checks.
# Safe to run repeatedly — idempotent where possible.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE="docker compose -f $PROJECT_DIR/docker-compose.yml"
ENV_FILE="$PROJECT_DIR/.env"

# ── Colours (matches setup.sh) ─────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}▸${RESET} $*"; }
ok()      { echo -e "${GREEN}✓${RESET} $*"; }
warn()    { echo -e "${YELLOW}!${RESET} $*"; }
heading() { echo -e "\n${BOLD}$*${RESET}"; }
die()     { echo -e "${RED}ERROR:${RESET} $*" >&2; exit 1; }

get_env() {
  grep -E "^${1}=" "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d '"'
}
```

- [ ] **Step 2: Add pre-flight section**

Append to `scripts/upgrade.sh`:

```bash
# ── Banner ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║         BelPro — Nadgradnja sistema       ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""

# ── Pre-flight ──────────────────────────────────────────────────────────────
heading "0. Preverjanje zahtev"

[[ -f "$ENV_FILE" ]] || die ".env ni najden na $ENV_FILE — najprej zaženite setup.sh."
command -v docker &>/dev/null || die "Docker ni nameščen."
docker info &>/dev/null       || die "Docker daemon ne teče. Zaženite Docker Desktop."
docker compose version &>/dev/null || die "Docker Compose ni na voljo."
ok "Docker je aktiven."

if ! git -C "$PROJECT_DIR" diff --quiet HEAD 2>/dev/null; then
  warn "Obstajajo lokalne spremembe, ki niso shranjene v git:"
  git -C "$PROJECT_DIR" diff --stat HEAD
  echo ""
  read -r -p "  Nadaljujem kljub temu? git pull lahko ne uspe pri konfliktih. [da/NE] " confirm
  [[ "$confirm" == "da" ]] || die "Nadgradnja prekinjena."
fi
ok "Delovno drevo je čisto."
```

- [ ] **Step 3: Syntax check**

```bash
bash -n scripts/upgrade.sh
```

Expected: no output, exit 0.

- [ ] **Step 4: Make executable**

```bash
chmod +x scripts/upgrade.sh
```

- [ ] **Step 5: Commit**

```bash
git add scripts/upgrade.sh
git commit -m "feat(infra): add upgrade.sh skeleton with pre-flight checks"
```

---

### Task 2: Backup and git pull steps

**Files:**
- Modify: `scripts/upgrade.sh`

**Context:** The backup step must call `scripts/backup.sh` (same directory as `upgrade.sh`). If it fails, abort — never upgrade without a backup. The git pull uses the `central` remote (not `origin` — this is a project convention). Get the current branch dynamically with `git branch --show-current` so the script works on any branch.

- [ ] **Step 1: Append backup section**

```bash
# ── Backup ──────────────────────────────────────────────────────────────────
heading "1. Varnostna kopija pred nadgradnjo"
info "Zaganjam backup.sh ..."
bash "$SCRIPT_DIR/backup.sh" || die "Varnostna kopija ni uspela — nadgradnja prekinjena."
ok "Varnostna kopija je shranjena."
```

- [ ] **Step 2: Append git pull section**

```bash
# ── Git pull ─────────────────────────────────────────────────────────────────
heading "2. Prenos najnovejše kode"
REMOTE="central"
BRANCH="$(git -C "$PROJECT_DIR" branch --show-current)"
info "Prenašam $REMOTE/$BRANCH ..."
git -C "$PROJECT_DIR" pull "$REMOTE" "$BRANCH" \
  || die "git pull ni uspel — razrešite konflikte in ponovite."
ok "Koda je posodobljena."
```

- [ ] **Step 3: Syntax check**

```bash
bash -n scripts/upgrade.sh
```

Expected: no output, exit 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/upgrade.sh
git commit -m "feat(infra): add backup and git pull steps to upgrade.sh"
```

---

### Task 3: Docker rebuild and service readiness wait

**Files:**
- Modify: `scripts/upgrade.sh`

**Context:** `docker compose pull` updates base images (postgres, redis, n8n). `--ignore-pull-failures` prevents abort if a base image tag is temporarily unavailable. `docker compose up -d --build` then rebuilds custom images (api, whisper, frontend) and restarts all services in dependency order. The postgres and api readiness waits are copied verbatim from `scripts/setup.sh` (lines 192–211) — do not reinvent them.

- [ ] **Step 1: Append docker rebuild section**

```bash
# ── Rebuild images ───────────────────────────────────────────────────────────
heading "3. Posodabljanje in gradnja Docker slik"
info "Prenašam posodobljene bazne slike ..."
$COMPOSE pull --ignore-pull-failures 2>/dev/null || true
info "Gradim slike po meri in ponovni zagon storitev ..."
$COMPOSE up -d --build
ok "Storitve so posodobljene."
```

- [ ] **Step 2: Append postgres readiness wait**

```bash
# ── Wait for PostgreSQL ──────────────────────────────────────────────────────
heading "4. Čakanje na PostgreSQL"
PG_USER="$(get_env POSTGRES_USER)"
PG_DB="$(get_env POSTGRES_DB)"
MAX_WAIT=60; ELAPSED=0
until $COMPOSE exec -T postgres pg_isready -U "$PG_USER" -d "$PG_DB" &>/dev/null; do
  if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    die "PostgreSQL ni bil pripravljen v ${MAX_WAIT}s. Preverite: $COMPOSE logs postgres"
  fi
  sleep 2; ELAPSED=$((ELAPSED + 2))
done
ok "PostgreSQL je pripravljen."
```

- [ ] **Step 3: Append API readiness wait**

```bash
# ── Wait for API ─────────────────────────────────────────────────────────────
heading "5. Čakanje na API"
ELAPSED=0
until $COMPOSE exec -T api curl -sf http://localhost:8000/health &>/dev/null; do
  if [[ $ELAPSED -ge 60 ]]; then
    warn "API se ni odzval v 60s. Preverite: $COMPOSE logs api"
    break
  fi
  sleep 3; ELAPSED=$((ELAPSED + 3))
done
ok "API je pripravljen."
```

- [ ] **Step 4: Syntax check**

```bash
bash -n scripts/upgrade.sh
```

Expected: no output, exit 0.

- [ ] **Step 5: Commit**

```bash
git add scripts/upgrade.sh
git commit -m "feat(infra): add docker rebuild and service readiness waits to upgrade.sh"
```

---

### Task 4: Migrations, health check, and summary

**Files:**
- Modify: `scripts/upgrade.sh`

**Context:** Alembic is run inside the api container via `docker compose exec -T api alembic upgrade head`. This is idempotent — if already at head it prints "No new upgrade ops." and exits 0. The final health check hits `http://localhost:8100/api/health` from the host (port 8100 is the externally mapped API port, as defined in `docker-compose.yml`). Print the raw JSON so the operator can see the response. The summary mirrors the style of `setup.sh`.

- [ ] **Step 1: Append migrations section**

```bash
# ── Alembic migrations ───────────────────────────────────────────────────────
heading "6. Migracije baze podatkov"
$COMPOSE exec -T api alembic upgrade head
ok "Migracije baze podatkov so dokončane."
```

- [ ] **Step 2: Append health check section**

```bash
# ── Health check ─────────────────────────────────────────────────────────────
heading "7. Preverjanje stanja sistema"
HEALTH="$(curl -sf http://localhost:8100/api/health 2>/dev/null || echo '{"status":"nedosegljiv"}')"
echo "  $HEALTH"
ok "Preverjanje stanja je dokončano."
```

- [ ] **Step 3: Append summary**

```bash
# ── Summary ───────────────────────────────────────────────────────────────────
heading "✓ Nadgradnja uspešno zaključena"
echo ""
echo -e "  ${BOLD}BelPro nadzorna plošča${RESET}  →  http://localhost:80"
echo -e "  ${BOLD}FastAPI dokumentacija${RESET}    →  http://localhost:8100/docs"
echo -e "  ${BOLD}n8n${RESET}                      →  http://localhost:5678"
echo ""
```

- [ ] **Step 4: Final syntax check**

```bash
bash -n scripts/upgrade.sh
```

Expected: no output, exit 0.

- [ ] **Step 5: Verify complete script structure by reading it**

Check that sections appear in this order: shebang → helpers → banner → pre-flight → backup → git pull → rebuild → postgres wait → api wait → migrations → health check → summary.

- [ ] **Step 6: Commit**

```bash
git add scripts/upgrade.sh
git commit -m "feat(infra): complete upgrade.sh with migrations, health check, and summary"
```

---

### Task 5: Documentation — add upgrade.sh to both READMEs

**Files:**
- Modify: `README_SL.md`
- Modify: `README.md`

**Context:** Both READMEs have a Maintenance section with subsections for backup, restore, logs, rebuild, and password reset. Add `upgrade.sh` as the first subsection in both — it's the most important maintenance operation. Also update the project structure listing in both files to include `upgrade.sh`. `README_SL.md` Maintenance section is "## Vzdrževanje" (around line 236); `README.md` Maintenance section is "## Maintenance" (around line 233). The project structure `scripts/` line in `README.md` is around line 299.

- [ ] **Step 1: Add upgrade subsection to Vzdrževanje section**

In `README_SL.md`, find the `## Vzdrževanje` heading. Insert the following immediately after that heading (before the `### Varnostno kopiranje` subsection):

```markdown
### Nadgradnja sistema

```bash
bash scripts/upgrade.sh
```

Skripta samodejno:
1. Naredi varnostno kopijo pred kakršno koli spremembo
2. Prenese najnovejšo kodo (`git pull central main`)
3. Posodobi in ponovno zgradi Docker slike
4. Počaka, da sta PostgreSQL in API pripravljena
5. Zažene Alembic migracije baze podatkov
6. Preveri stanje sistema in izpiše povzetek

Varno za večkratno izvajanje — zaženite vsakič, ko posodobite kodo iz repozitorija.

```

- [ ] **Step 2: Update project structure listing**

In `README_SL.md`, find the `belpro/` code block in the "Struktura projekta" section. Change the `scripts/` line from:

```
├── scripts/                # Skripte: setup.sh, backup.sh, restore.sh
```

to:

```
├── scripts/                # Skripte: setup.sh, upgrade.sh, backup.sh, restore.sh
```

- [ ] **Step 3: Add upgrade subsection to English README.md Maintenance section**

In `README.md`, find the `## Maintenance` heading. Insert the following immediately after that heading (before the `### Backup` subsection):

```markdown
### Upgrade

```bash
bash scripts/upgrade.sh
```

Automatically: takes a backup, pulls the latest code (`git pull central main`), rebuilds Docker images, waits for PostgreSQL and API readiness, runs Alembic migrations, and prints a health check summary. Safe to run repeatedly.

```

- [ ] **Step 4: Update project structure listing in README.md**

In `README.md`, find the `scripts/` line in the project layout code block. Change:

```
├── scripts/                # setup.sh, backup.sh, restore.sh
```

to:

```
├── scripts/                # setup.sh, upgrade.sh, backup.sh, restore.sh
```

- [ ] **Step 5: Commit**

```bash
git add README_SL.md README.md
git commit -m "docs: add upgrade.sh to maintenance sections in both READMEs"
```

---

## Self-Review

**Spec coverage check (against ISS-011):**
- ✅ Pull latest code → Task 2, git pull step
- ✅ Rebuild affected Docker images → Task 3, `docker compose up -d --build`
- ✅ Run Alembic migrations inside API container → Task 4
- ✅ Restart services in correct order → handled by `docker compose up -d --build` dependency graph
- ✅ Basic health check before exiting → Task 4, curl to `/api/health`
- ✅ Safe to run repeatedly (idempotent) → Docker layer cache + Alembic no-op at head
- ✅ Enumerate steps that caused issues manually → covered: backup-first, correct remote name (`central`), dependency-ordered restart via compose

**Placeholder scan:** No TBDs, no "add appropriate handling" — every step has exact code.

**Type consistency:** No shared types across tasks (pure bash). Helper function `get_env` defined in Task 1, used in Task 3 — consistent naming.
