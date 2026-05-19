#!/usr/bin/env bash
# List pending_manager entries — ready to paste into the n8n manual trigger.
#
# Usage:
#   ./scripts/list_pending_entries.sh        # entries not yet notified to manager
#   ./scripts/list_pending_entries.sh --all  # include already-notified entries

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

[[ -f "$PROJECT_DIR/.env" ]] || { echo "ERROR: .env not found at $PROJECT_DIR/.env" >&2; exit 1; }

exec python "$SCRIPT_DIR/list_pending_entries.py" "$@"
