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
else
  ok "Delovno drevo je čisto."
fi
