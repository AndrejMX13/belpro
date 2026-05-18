#!/usr/bin/env bash
# BelPro EMŠO key rotation script.
# ONE-TIME EMERGENCY TOOL — use only when the encryption key must be changed.
#
# Rotate:  ./scripts/rotate_emso_key.sh <OLD_KEY> <NEW_KEY>
# Restore: ./scripts/rotate_emso_key.sh --restore
#
# Both keys are base64url-encoded 32-byte AES-256 keys (EMSO_ENCRYPTION_KEY value).
# Security: OLD_KEY and NEW_KEY are passed as positional arguments and are briefly
# visible in process listings (ps aux). Acceptable for an interactive emergency tool;
# do not use in automated pipelines.

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

if ! $COMPOSE ps --status running api 2>/dev/null | grep -q "api"; then
  die "API vsebnik ne teče. Zaženite stack: docker compose up -d"
fi
ok "Pogoji so izpolnjeni."

[[ -t 0 ]] || die "Ta skript mora biti zagnan interaktivno (brez preusmeritve vhoda)."

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
  $COMPOSE exec -T -e PYTHONPATH=/app api python /app/scripts/rotate_emso_key.py --restore "$BACKUP_FILE" \
    || die "Obnovitev ni uspela. Preverite zgornje napake."
  ok "Obnovitev uspešna."
  echo ""
  warn "Ne pozabite posodobiti EMSO_ENCRYPTION_KEY v .env na stari ključ"
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
# Intentional: operator must write this down. Key also lands in terminal scrollback
# and shell history — same accepted trade-off as the ps aux note in the header.
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
  -e PYTHONPATH=/app \
  -e OLD_EMSO_KEY="$OLD_KEY" \
  api python /app/scripts/rotate_emso_key.py --backup "$BACKUP_FILE" \
  || die "Ciljna varnostna kopija ni uspela — rotacija prekinjena."
ok "Ciljna varnostna kopija je shranjena."

# ── Rotation ──────────────────────────────────────────────────────────────
heading "3. Rotacija ključa"
info "Zaganjam rotacijo znotraj API vsebnika ..."
$COMPOSE exec -T \
  -e PYTHONPATH=/app \
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
echo -e "  ${BOLD}4.${RESET} Šele ko so koraki 1–3 zaključeni in API deluje brez napak,"
echo -e "     se vrni sem in potrdi brisanje varnostne kopije."
echo ""
echo -e "  Varnostna kopija je shranjena na: ${CYAN}${BACKUP_FILE}${RESET}"
echo -e "  Dostop: ${CYAN}docker compose exec api cat ${BACKUP_FILE}${RESET}"
echo ""
warn "Datoteka vsebuje stari šifrirni ključ in šifrirane podatke — je zaupna."
echo ""
warn "Preden odgovoriš 'DA': preveri, da si že posodobil .env, znova zagnal API vsebnik"
warn "in da v logu ni napak. Varnostna kopija je edina pot nazaj."
echo ""
read -r -p "  Koraki 1–3 so zaključeni, API deluje. Izbrišem varnostno kopijo? Vpišite 'DA' za brisanje: " cleanup
if [[ "$cleanup" == "DA" ]]; then
  $COMPOSE exec -T api rm -f "$BACKUP_FILE"
  $COMPOSE exec -T api rmdir /app/pdfs/temp 2>/dev/null || true
  ok "Varnostna kopija je izbrisana."
else
  warn "Varnostna kopija NI izbrisana. Ko bo vse v redu, jo izbrišite ročno:"
  warn "  docker compose exec api rm -f ${BACKUP_FILE}"
fi
echo ""
