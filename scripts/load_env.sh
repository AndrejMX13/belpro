#!/usr/bin/env bash
# Loads variables from .env in the project root into the current shell session.
# Must be sourced, not executed: source ./scripts/load_env.sh
# Skips blank lines and comments. Handles quoted values.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: .env file not found at $ENV_FILE" >&2
    return 1
fi

set -a
# shellcheck disable=SC1090
source <(grep -v '^\s*#' "$ENV_FILE" | grep -v '^\s*$')
set +a

COUNT=$(grep -v '^\s*#' "$ENV_FILE" | grep -c '^\s*[^=]*=')
echo "Loaded $COUNT variables from .env"
