#!/usr/bin/env bash
# BelPro initial setup wizard.
# Run once from the project root: ./scripts/setup.sh
# Requires: docker, docker compose, python or openssl (for secret generation).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"
COMPOSE="docker compose -f $PROJECT_DIR/docker-compose.yml"

# ── Colours ────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}▸${RESET} $*"; }
ok()      { echo -e "${GREEN}✓${RESET} $*"; }
warn()    { echo -e "${YELLOW}!${RESET} $*"; }
heading() { echo -e "\n${BOLD}$*${RESET}"; }
die()     { echo -e "${RED}ERROR:${RESET} $*" >&2; exit 1; }

# ── Helpers ────────────────────────────────────────────────────────────────
gen_hex32() {
  if command -v python &>/dev/null; then
    python -c "import secrets; print(secrets.token_hex(32))"
  else
    openssl rand -hex 32
  fi
}

gen_b64_key() {
  # 32-byte base64url-encoded key for AES-256 (EMSO_ENCRYPTION_KEY)
  if command -v python &>/dev/null; then
    python -c "import secrets,base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
  else
    openssl rand -base64 32 | tr '+/' '-_' | tr -d '='
  fi
}

gen_hex24() {
  if command -v python &>/dev/null; then
    python -c "import secrets; print(secrets.token_hex(24))"
  else
    openssl rand -hex 24
  fi
}

prompt_password() {
  local label="$1" var_name="$2" default="$3"
  local pw=""
  while true; do
    read -r -s -p "  $label: " pw; echo ""
    if [[ -z "$pw" && -n "$default" ]]; then
      pw="$default"
      warn "Using default '$default' — change this before production use."
      break
    fi
    if [[ ${#pw} -lt 8 ]]; then
      warn "Password must be at least 8 characters. Try again."; continue
    fi
    local pw2=""
    read -r -s -p "  Confirm $label: " pw2; echo ""
    if [[ "$pw" == "$pw2" ]]; then break
    else warn "Passwords do not match. Try again."; fi
  done
  printf -v "$var_name" '%s' "$pw"
}

set_env() {
  # Replace or append a key=value in .env
  local key="$1" val="$2"
  if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
    sed -i "s|^${key}=.*|${key}=${val}|" "$ENV_FILE"
  else
    echo "${key}=${val}" >> "$ENV_FILE"
  fi
}

get_env() {
  grep -E "^${1}=" "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d '"'
}

# ── Banner ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║       BelPro — Začetna konfiguracija      ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""
warn "Ta skripta bo konfigurirala BelPro za prvo zagotovitev."
warn "Za produkcijsko nameščanje preberite SPEC.md."
echo ""

# ── Prerequisites ──────────────────────────────────────────────────────────
heading "0. Preverjanje zahtev"

command -v docker &>/dev/null  || die "Docker ni nameščen."
docker info &>/dev/null        || die "Docker daemon ne teče. Zaženite Docker Desktop."
docker compose version &>/dev/null || die "Docker Compose ni na voljo."
ok "Docker in Docker Compose sta na voljo."

# ── .env setup ─────────────────────────────────────────────────────────────
heading "1. Konfiguracija okolja (.env)"

if [[ -f "$ENV_FILE" ]]; then
  warn ".env že obstaja."
  read -r -p "  Prepiši obstoječi .env? [da/NE] " overwrite
  if [[ "$overwrite" != "da" ]]; then
    info "Obstoječi .env ohranjen. Nadaljujem z namestitvijo..."
    SKIP_ENV_GENERATION=true
  else
    cp "$ENV_FILE" "${ENV_FILE}.bak.$(date +%Y%m%d_%H%M%S)"
    ok "Varnostna kopija shranjena."
    cp "$PROJECT_DIR/.env.example" "$ENV_FILE"
    SKIP_ENV_GENERATION=false
  fi
else
  cp "$PROJECT_DIR/.env.example" "$ENV_FILE"
  ok ".env ustvarjen iz .env.example"
  SKIP_ENV_GENERATION=false
fi

if [[ "${SKIP_ENV_GENERATION:-false}" == "false" ]]; then

  # -- PostgreSQL password --
  heading "2. Gesla in skrivnosti"
  echo ""
  info "PostgreSQL geslo (za bazo podatkov):"
  prompt_password "POSTGRES_PASSWORD" PG_PASS "$(gen_hex24)"
  set_env "POSTGRES_PASSWORD" "$PG_PASS"
  # Update DATABASE_URL consistently
  PG_DB="$(get_env POSTGRES_DB)"
  PG_USER="$(get_env POSTGRES_USER)"
  set_env "DATABASE_URL" "postgresql+asyncpg://${PG_USER}:${PG_PASS}@postgres:5432/${PG_DB}"
  ok "PostgreSQL geslo nastavljeno."

  # -- Manager dashboard password --
  echo ""
  info "Geslo za BelPro upravitelja (vpis v nadzorno ploščo):"
  prompt_password "MANAGER_PASSWORD" MGR_PASS ""
  set_env "MANAGER_PASSWORD" "$MGR_PASS"
  ok "Geslo upravitelja nastavljeno."

  # -- n8n password --
  echo ""
  info "Geslo za n8n (spletni vmesnik na :5678):"
  prompt_password "N8N_BASIC_AUTH_PASSWORD" N8N_PASS ""
  set_env "N8N_BASIC_AUTH_PASSWORD" "$N8N_PASS"
  ok "n8n geslo nastavljeno."

  # -- SMTP password --
  echo ""
  info "SMTP geslo (za pošiljanje e-pošte — pustite prazno, če boste nastavili pozneje):"
  read -r -s -p "  SMTP_PASSWORD (Enter za preskočiti): " SMTP_PASS; echo ""
  if [[ -n "$SMTP_PASS" ]]; then
    set_env "SMTP_PASSWORD" "$SMTP_PASS"
    ok "SMTP geslo nastavljeno."
  else
    warn "SMTP geslo preskočeno — nastavite SMTP_PASSWORD v .env pred pošiljanjem e-pošte."
  fi

  # -- Auto-generated secrets --
  heading "3. Generiranje kriptografskih skrivnosti"
  info "Generiram EMSO_ENCRYPTION_KEY..."
  set_env "EMSO_ENCRYPTION_KEY" "$(gen_b64_key)"
  ok "EMSO_ENCRYPTION_KEY generiran."

  info "Generiram API_SECRET_KEY..."
  set_env "API_SECRET_KEY" "$(gen_hex32)"
  ok "API_SECRET_KEY generiran."

  info "Generiram AUTHENTICATION_API_KEY (za dostop do Evolution API strežnika)..."
  set_env "AUTHENTICATION_API_KEY" "$(gen_hex24)"
  ok "AUTHENTICATION_API_KEY generiran."

  warn "EVOLUTION_API_KEY (ključ instance) je treba vnesti ročno po ustvaritvi instance v Evolution API."
  warn "Pustite privzeto vrednost — po namestitvi sledite navodilom za WhatsApp nastavitev."

fi  # end SKIP_ENV_GENERATION

# ── Start stack ────────────────────────────────────────────────────────────
heading "4. Zagon Docker storitev"
info "Gradim in zaganjam vse storitve (to lahko traja nekaj minut ob prvem zagonu)..."
$COMPOSE up -d --build
ok "Storitve zaganjamo v ozadju."

# ── Wait for postgres ──────────────────────────────────────────────────────
heading "5. Čakanje na PostgreSQL"
info "Čakam, da je PostgreSQL pripravljen..."
MAX_WAIT=60
ELAPSED=0
until $COMPOSE exec -T postgres pg_isready -U "$(get_env POSTGRES_USER)" -d "$(get_env POSTGRES_DB)" &>/dev/null; do
  if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    die "PostgreSQL ni bil pripravljen v ${MAX_WAIT}s. Preverite: $COMPOSE logs postgres"
  fi
  sleep 2; ELAPSED=$((ELAPSED + 2))
done
ok "PostgreSQL je pripravljen."

# ── Wait for api ───────────────────────────────────────────────────────────
heading "6. Čakanje na API"
info "Čakam, da API zažene..."
ELAPSED=0
until $COMPOSE exec -T api curl -sf http://localhost:8000/health &>/dev/null; do
  if [[ $ELAPSED -ge 60 ]]; then
    warn "API se ni odzval v 60s. Preverite: $COMPOSE logs api"
    break
  fi
  sleep 3; ELAPSED=$((ELAPSED + 3))
done
ok "API je pripravljen."

# ── Alembic migrations ─────────────────────────────────────────────────────
heading "7. Zaganjam Alembic migracije"
$COMPOSE exec -T api alembic upgrade head
ok "Migracije baze podatkov so uspešno izvedene."

# ── Wait for n8n ──────────────────────────────────────────────────────────
heading "8. n8n — konfiguracija in uvoz delovnih tokov"
info "Čakam na n8n..."
ELAPSED=0
until curl -sf http://localhost:5678/healthz &>/dev/null; do
  if [[ $ELAPSED -ge 90 ]]; then
    warn "n8n se ni odzval v 90s. Preverite: $COMPOSE logs n8n"
    break
  fi
  sleep 3; ELAPSED=$((ELAPSED + 3))
done
ok "n8n je pripravljen."
echo ""
info "Odprite n8n: http://localhost:5678"
info "Prijavite se z N8N_BASIC_AUTH_USER / N8N_BASIC_AUTH_PASSWORD iz .env"
echo ""

# ── n8n API key ────────────────────────────────────────────────────────────
EXISTING_N8N_KEY="$(get_env N8N_API_KEY)"
if [[ -z "$EXISTING_N8N_KEY" || "$EXISTING_N8N_KEY" == "FILL_IN_AFTER_FIRST_N8N_RUN" ]]; then
  info "Ustvarite API ključ: Settings → API → Create an API key"
  read -r -p "  Prilepite N8N_API_KEY: " N8N_KEY
  set_env "N8N_API_KEY" "$N8N_KEY"
  ok "N8N_API_KEY shranjen v .env."
else
  N8N_KEY="$EXISTING_N8N_KEY"
  ok "N8N_API_KEY je že nastavljen v .env."
fi
echo ""

# ── Create n8n credentials ─────────────────────────────────────────────────
info "Ustvarjam prijavne podatke v n8n..."
POSTGRES_DB="$(get_env POSTGRES_DB)" \
POSTGRES_USER="$(get_env POSTGRES_USER)" \
POSTGRES_PASSWORD="$(get_env POSTGRES_PASSWORD)" \
MANAGER_PASSWORD="$(get_env MANAGER_PASSWORD)" \
API_SECRET_KEY="$(get_env API_SECRET_KEY)" \
N8N_API_KEY="$N8N_KEY" \
python - <<'PYEOF'
import os, urllib.request, urllib.error, json

API_KEY = os.environ["N8N_API_KEY"]
BASE    = "http://localhost:5678/api/v1"

def create_cred(name, ctype, data):
    payload = json.dumps({"name": name, "type": ctype, "data": data}).encode()
    req = urllib.request.Request(f"{BASE}/credentials", data=payload, method="POST")
    req.add_header("X-N8N-API-KEY", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10):
            print(f"  \033[32m✓\033[0m {name}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        if e.code in (400, 409):
            print(f"  \033[33m~\033[0m {name}: že obstaja ali napaka ({e.code})")
        else:
            print(f"  \033[31m✗\033[0m {name}: HTTP {e.code} — {body[:120]}")
    except Exception as exc:
        print(f"  \033[31m✗\033[0m {name}: {exc}")

create_cred("BelPro Postgres", "postgres", {
    "host": "postgres", "port": 5432,
    "database": os.environ["POSTGRES_DB"],
    "user":     os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "ssl": False,
})
create_cred("BelPro API (Basic Auth)", "httpBasicAuth", {
    "user":     "manager",
    "password": os.environ["MANAGER_PASSWORD"],
})
create_cred("BelPro API Internal Key", "httpHeaderAuth", {
    "name":  "X-Internal-Key",
    "value": os.environ["API_SECRET_KEY"],
})
PYEOF
echo ""

# ── Import workflows ───────────────────────────────────────────────────────
info "Uvažam delovne tokove..."
python "$PROJECT_DIR/scripts/n8n_workflows.py" import
echo ""

# ── Seed console URLs into admin settings ──────────────────────────────────
info "Nastavljam naslove storitvenih konzol..."
_N8N_PROTO="$(get_env N8N_PROTOCOL)"
_N8N_HOST="$(get_env N8N_HOST)"
_N8N_ADMIN_URL="${_N8N_PROTO:-http}://${_N8N_HOST:-localhost}:5678"
_API_DOCS_URL="${_N8N_PROTO:-http}://${_N8N_HOST:-localhost}:8100/docs"
_MGR_PASS="$(get_env MANAGER_PASSWORD)"
$COMPOSE exec -T api curl -sf \
  -X PATCH \
  -H "Content-Type: application/json" \
  -u "manager:${_MGR_PASS}" \
  -d "{\"n8n_admin_url\":\"${_N8N_ADMIN_URL}\",\"api_docs_url\":\"${_API_DOCS_URL}\"}" \
  "http://localhost:8000/api/admin/settings" > /dev/null \
  && ok "n8n: ${_N8N_ADMIN_URL}  |  API docs: ${_API_DOCS_URL}" \
  || warn "Nastavitev konzol ni uspela — nastavite ročno v Sistemske nastavitve."
echo ""

# ── Remaining manual steps ─────────────────────────────────────────────────
warn "Preostalo (ročno) — WhatsApp (Evolution API):"
echo "   Ko dobite telefonsko številko:"
echo "   a) Odprite: http://localhost:8180/manager/"
echo "      Prijavite se z AUTHENTICATION_API_KEY iz .env"
echo "   b) Ustvarite instanco in kopirajte ključ instance"
echo "   c) Vpišite ključ v .env kot EVOLUTION_API_KEY"
echo "   d) Zaženite: $COMPOSE up -d --build api"
echo "   e) Skenirajte QR kodo s telefonom (glejte EVOLUTION_QR_TROUBLESHOOTING.md)"
echo "   f) V n8n ustvarite credential 'BelPro Evolution API' (HTTP Header Auth):"
echo "      Ime glave: apikey   Vrednost: EVOLUTION_API_KEY iz .env"
echo "   g) Zaženite: python scripts/n8n_workflows.py import"
echo ""
warn "Preostalo (ročno) — SMTP (e-pošta):"
echo "   V n8n ustvarite credential 'BelPro SMTP' (SMTP) z geslom iz SMTP_PASSWORD v .env."
echo "   Gostitelja, vrata in uporabnika nastavite v BelPro Nastavitvah (nadzorna plošča)."

# ── Summary ────────────────────────────────────────────────────────────────
heading "✓ Namestitev dokončana"
echo ""
echo -e "  ${BOLD}BelPro nadzorna plošča${RESET}  →  http://localhost:80"
echo -e "  ${BOLD}FastAPI dokumentacija${RESET}    →  http://localhost:8100/docs"
echo -e "  ${BOLD}n8n${RESET}                      →  http://localhost:5678"
echo ""
echo -e "  Geslo upravitelja: ${YELLOW}nastavljeno v .env (MANAGER_PASSWORD)${RESET}"
echo ""
warn "Nikoli ne commitajte .env v git!"
echo ""
