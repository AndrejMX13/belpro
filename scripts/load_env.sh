#!/usr/bin/env bash
# Loads variables from .env in the project root into the current shell session.
# Must be sourced, not executed: source ./scripts/load_env.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: .env file not found at $ENV_FILE" >&2
    return 1
fi

count=0
while IFS= read -r line || [[ -n "$line" ]]; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line//[[:space:]]/}" ]] && continue
    if [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]%$'\r'}"
        # Strip surrounding single or double quotes
        if [[ "$value" =~ ^\"(.*)\"$ ]] || [[ "$value" =~ ^\'(.*)\'$ ]]; then
            value="${BASH_REMATCH[1]}"
        fi
        printf -v "$key" '%s' "$value"
        export "$key"
        count=$(( count + 1 ))
    fi
done < "$ENV_FILE"

echo "Loaded $count variables from .env"
