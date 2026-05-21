#!/bin/bash
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/${DATE}"
RETENTION_DAYS="${1:-${BACKUP_RETENTION_DAYS:-30}}"
EMSO_KEY_FINGERPRINT="${EMSO_ENCRYPTION_KEY:0:8}..."

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
PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
    -h "${POSTGRES_HOST}" \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    --format=custom \
    -f "${BACKUP_DIR}/belpro.pgdump" || PG_RC=$?
if [ "${PG_RC:-0}" -ne 0 ]; then
  report_error "pg_dump failed" "exit code ${PG_RC}"
  rm -rf "${BACKUP_DIR}"
  exit 1
fi

# Photos archive
echo "[backup] Archiving photos..."
if ! tar -czf "${BACKUP_DIR}/photos.tar.gz" -C /app photos 2>/dev/null; then
  echo "[backup] Warning: photos archive failed (directory may be empty)"
  report_error "photos archive failed" "tar returned non-zero; directory may be empty"
fi

# PDFs archive
echo "[backup] Archiving PDFs..."
if ! tar -czf "${BACKUP_DIR}/pdfs.tar.gz" -C /app pdfs 2>/dev/null; then
  echo "[backup] Warning: PDFs archive failed (directory may be empty)"
  report_error "PDFs archive failed" "tar returned non-zero; directory may be empty"
fi

# Manifest
cat > "${BACKUP_DIR}/manifest.txt" <<EOF
BelPro backup
Timestamp         : ${DATE}
Date              : $(date)
DB                : ${POSTGRES_DB}
Files             : belpro.pgdump  photos.tar.gz  pdfs.tar.gz
EMSO key prefix   : ${EMSO_KEY_FINGERPRINT}
EOF

echo "[backup] Backup complete: ${BACKUP_DIR}"

# Prune old backups
echo "[backup] Pruning backups older than ${RETENTION_DAYS} days..."
find /backups -maxdepth 1 -type d -mtime "+${RETENTION_DAYS}" -exec rm -rf {} + || {
  echo "[backup] Warning: pruning old backups failed"
  report_error "backup pruning failed" "find/rm returned non-zero"
}

echo "[backup] Done."
