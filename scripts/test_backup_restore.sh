#!/usr/bin/env bash
# Smoke test: backup → drop → init.sql → restore → verify.
# Run from the repo root.  Requires the belpro stack to be up.
# Requires: scripts/backup.sh and scripts/restore.sh
set -euo pipefail

API="http://localhost:8100"
MANAGER_USER="admin"
MANAGER_PASS="${MANAGER_PASSWORD:-changeme}"  # read from env or .env
AUTH="-u ${MANAGER_USER}:${MANAGER_PASS}"

echo "=== BelPro backup/restore smoke test ==="

# 1. Confirm stack is running
echo "[1] Checking stack health..."
curl -sf "${API}/api/health" | grep -q '"status":"ok"' \
  || { echo "FAIL: stack not healthy"; exit 1; }

# 2. Seed known data via API
echo "[2] Seeding test data..."
VOLUNTEER_RESP=$(curl -sf -X POST "${API}/api/volunteers" \
  ${AUTH} \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Backup",
    "last_name": "Test",
    "street": "Testna 99",
    "postal_code": "1000",
    "city": "Ljubljana",
    "emso": "9999999999999",
    "phone": "+38641999888"
  }')

VOLUNTEER_ID=$(echo "${VOLUNTEER_RESP}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "    Seeded volunteer: ${VOLUNTEER_ID}"

# 3. Run backup
echo "[3] Running backup..."
SNAPSHOT=$(bash scripts/backup.sh | tail -1)
echo "    Snapshot: ${SNAPSHOT}"
[ -f "${SNAPSHOT}" ] || { echo "FAIL: snapshot file not created at ${SNAPSHOT}"; exit 1; }

# 4. Drop the belpro database
echo "[4] Dropping belpro database..."
docker compose exec -T postgres psql -U belpro -d postgres -c "DROP DATABASE IF EXISTS belpro;"

# 5. Recreate schema via init.sql
echo "[5] Recreating schema via init.sql..."
docker compose exec -T postgres psql -U belpro -d postgres -c "CREATE DATABASE belpro;"
docker compose exec -T postgres psql -U belpro -d belpro < db/init.sql

# 6. Restore from snapshot
echo "[6] Restoring from snapshot..."
bash scripts/restore.sh "${SNAPSHOT}"

# 7. Verify the seeded volunteer is present
echo "[7] Verifying restore..."
ITEMS=$(curl -sf "${API}/api/volunteers" ${AUTH} | python3 -c "import sys,json; print(json.load(sys.stdin)['total'])")
echo "    Volunteers after restore: ${ITEMS}"

curl -sf "${API}/api/volunteers/${VOLUNTEER_ID}" ${AUTH} > /dev/null \
  || { echo "FAIL: seeded volunteer not found after restore"; exit 1; }

# 8. Cleanup test data
echo "[8] Cleaning up seeded test volunteer..."
curl -sf -X DELETE "${API}/api/volunteers/${VOLUNTEER_ID}" ${AUTH} || true
rm -f "${SNAPSHOT}"

echo ""
echo "=== PASS: backup/restore smoke test completed successfully ==="
