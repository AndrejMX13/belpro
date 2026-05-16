#!/usr/bin/env bash
# Switch the manager's WhatsApp phone between real (manager) and test (volunteer) mode.
# Usage: ./scripts/switch_manager_phone.sh [volunteer|manager]
# Reads TEST_MANAGER_PHONE, TEST_VOLUNTEER_PHONE, and MANAGER_PASSWORD from environment or .env.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck disable=SC1090
source "$SCRIPT_DIR/load_env.sh"

MODE="${1:-}"
if [[ "$MODE" != "volunteer" && "$MODE" != "manager" ]]; then
    echo "Usage: $0 [volunteer|manager]" >&2
    exit 1
fi

FAKE_PHONE="${TEST_VOLUNTEER_PHONE:-38600000000}"
REAL_PHONE="${TEST_MANAGER_PHONE:-}"
PASSWORD="${MANAGER_PASSWORD:-}"

if [[ -z "$REAL_PHONE" ]]; then
    echo "ERROR: TEST_MANAGER_PHONE not set in environment or .env" >&2
    exit 1
fi

if [[ -z "$PASSWORD" ]]; then
    echo "ERROR: MANAGER_PASSWORD not set in environment or .env" >&2
    exit 1
fi

API_URL="http://localhost:8100/api/managers/me"

if [[ "$MODE" == "volunteer" ]]; then
    PHONE="$FAKE_PHONE"
    echo "Switching to TEST phone ($PHONE) — your phone is VOLUNTEER"
else
    PHONE="$REAL_PHONE"
    echo "Switching to REAL phone ($PHONE) — your phone is MANAGER"
fi

RESULT=$(curl -sf -X PATCH "$API_URL" \
    -u "manager:$PASSWORD" \
    -H "Content-Type: application/json" \
    -d "{\"phone\":\"$PHONE\"}")

echo "Done. Manager phone: $(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['phone'])")"
