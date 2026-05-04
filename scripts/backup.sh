#!/usr/bin/env bash
# BelPro backup — PostgreSQL dump + photos archive.
# Run from the project root: ./scripts/backup.sh [backup-dir]
# Requires: docker compose stack is running.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_ROOT="${1:-$PROJECT_DIR/backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

# ── Load .env ──────────────────────────────────────────────────────────────
ENV_FILE="$PROJECT_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: .env not found at $ENV_FILE" >&2
  exit 1
fi

# Export only the DB variables we need
set -a
# shellcheck disable=SC1090
source <(grep -E '^(POSTGRES_DB|POSTGRES_USER|POSTGRES_PASSWORD)=' "$ENV_FILE")
set +a

: "${POSTGRES_DB:?POSTGRES_DB not set in .env}"
: "${POSTGRES_USER:?POSTGRES_USER not set in .env}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set in .env}"

# ── Prepare backup directory ───────────────────────────────────────────────
mkdir -p "$BACKUP_DIR"
echo "BelPro backup → $BACKUP_DIR"

# ── PostgreSQL dump ────────────────────────────────────────────────────────
echo "  [1/3] Dumping PostgreSQL..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" exec -T postgres \
  pg_dump \
    --username="$POSTGRES_USER" \
    --dbname="$POSTGRES_DB" \
    --format=custom \
    --no-password \
  > "$BACKUP_DIR/belpro.pgdump"
echo "        ✓ belpro.pgdump ($(du -sh "$BACKUP_DIR/belpro.pgdump" | cut -f1))"

# ── Photos archive ─────────────────────────────────────────────────────────
echo "  [2/3] Archiving photos..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" exec -T api \
  tar -czf - /app/photos 2>/dev/null \
  > "$BACKUP_DIR/photos.tar.gz" || {
    echo "        (no photos directory yet — skipping)"
    touch "$BACKUP_DIR/photos.tar.gz"
  }
echo "        ✓ photos.tar.gz ($(du -sh "$BACKUP_DIR/photos.tar.gz" | cut -f1))"

# ── Manifest ───────────────────────────────────────────────────────────────
echo "  [3/3] Writing manifest..."
cat > "$BACKUP_DIR/manifest.txt" <<EOF
BelPro backup
Timestamp : $TIMESTAMP
Date      : $(date)
DB        : $POSTGRES_DB
Files     : belpro.pgdump  photos.tar.gz
EOF
echo "        ✓ manifest.txt"

# ── Done ───────────────────────────────────────────────────────────────────
echo ""
echo "Backup complete: $BACKUP_DIR"
echo "To restore: ./scripts/restore.sh $BACKUP_DIR"
