#!/usr/bin/env bash
# BelPro restore — PostgreSQL + photos from a backup directory.
# Run from the project root: ./scripts/restore.sh <backup-dir>
# WARNING: This overwrites the current database and photos. No undo.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${1:-}"

# ── Validate arguments ─────────────────────────────────────────────────────
if [[ -z "$BACKUP_DIR" ]]; then
  echo "Usage: $0 <backup-dir>" >&2
  echo "Example: $0 ./backups/20260504_070000" >&2
  exit 1
fi

if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "ERROR: backup directory not found: $BACKUP_DIR" >&2
  exit 1
fi

PGDUMP="$BACKUP_DIR/belpro.pgdump"
PHOTOS="$BACKUP_DIR/photos.tar.gz"

if [[ ! -f "$PGDUMP" ]]; then
  echo "ERROR: $PGDUMP not found — invalid backup directory?" >&2
  exit 1
fi

# ── Load .env ──────────────────────────────────────────────────────────────
ENV_FILE="$PROJECT_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: .env not found at $ENV_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source <(grep -E '^(POSTGRES_DB|POSTGRES_USER|POSTGRES_PASSWORD)=' "$ENV_FILE")
set +a

: "${POSTGRES_DB:?POSTGRES_DB not set in .env}"
: "${POSTGRES_USER:?POSTGRES_USER not set in .env}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set in .env}"

# ── Confirmation ───────────────────────────────────────────────────────────
echo "BelPro restore"
echo "  Source : $BACKUP_DIR"
echo "  Target : $POSTGRES_DB @ postgres container"
echo ""
echo "WARNING: This will OVERWRITE the current database and photos!"
read -r -p "Type 'da' to continue: " CONFIRM
if [[ "$CONFIRM" != "da" ]]; then
  echo "Restore cancelled."
  exit 0
fi

# ── PostgreSQL restore ─────────────────────────────────────────────────────
echo ""
echo "  [1/3] Dropping and recreating database..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" exec -T postgres \
  psql --username="$POSTGRES_USER" --dbname=postgres \
  -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$POSTGRES_DB' AND pid <> pg_backend_pid();" \
  -c "DROP DATABASE IF EXISTS \"$POSTGRES_DB\";" \
  -c "CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";"
echo "        ✓ database recreated"

echo "  [2/3] Restoring PostgreSQL dump..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" exec -T postgres \
  pg_restore \
    --username="$POSTGRES_USER" \
    --dbname="$POSTGRES_DB" \
    --no-password \
    --exit-on-error \
  < "$PGDUMP"
echo "        ✓ database restored"

# ── Photos restore ─────────────────────────────────────────────────────────
echo "  [3/3] Restoring photos..."
if [[ -s "$PHOTOS" ]]; then
  docker compose -f "$PROJECT_DIR/docker-compose.yml" exec -T api \
    bash -c "rm -rf /app/photos/* 2>/dev/null; tar -xzf - -C /" < "$PHOTOS"
  echo "        ✓ photos restored"
else
  echo "        (photos archive empty — skipping)"
fi

# ── Restart API ────────────────────────────────────────────────────────────
echo ""
echo "Restarting API service..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" restart api
echo "✓ Restore complete."
