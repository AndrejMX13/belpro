#!/bin/bash
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/${DATE}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"

report_error() {
  local message="$1"
  local detail="$2"
  curl -sf -X POST "${API_URL}/api/errors" \
    -H "Content-Type: application/json" \
    -H "X-Internal-Key: ${API_SECRET_KEY}" \
    -d "{\"service\":\"ops\",\"operation\":\"backup\",\"message\":\"${message}\",\"detail\":\"${detail}\"}" \
    || true
}

echo "[backup] Starting backup: ${DATE}"

mkdir -p "${BACKUP_DIR}"

# PostgreSQL dump
echo "[backup] Dumping database..."
if ! PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
    -h "${POSTGRES_HOST}" \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    -f "${BACKUP_DIR}/db.sql"; then
  report_error "pg_dump failed" "exit code $?"
  rm -rf "${BACKUP_DIR}"
  exit 1
fi

# Photos archive
echo "[backup] Archiving photos..."
if ! tar -czf "${BACKUP_DIR}/photos.tar.gz" -C /app photos 2>/dev/null; then
  echo "[backup] Warning: photos archive failed (directory may be empty)"
fi

# PDFs archive
echo "[backup] Archiving PDFs..."
if ! tar -czf "${BACKUP_DIR}/pdfs.tar.gz" -C /app pdfs 2>/dev/null; then
  echo "[backup] Warning: PDFs archive failed (directory may be empty)"
fi

# Compress DB dump
gzip "${BACKUP_DIR}/db.sql"

echo "[backup] Backup complete: ${BACKUP_DIR}"

# Prune old backups
echo "[backup] Pruning backups older than ${RETENTION_DAYS} days..."
find /backups -maxdepth 1 -type d -mtime "+${RETENTION_DAYS}" -exec rm -rf {} + || true

echo "[backup] Done."
