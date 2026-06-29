#!/bin/bash
# Wrapper for gcalcli using credentials from .env

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing .env file. Copy .env.example to .env and fill in your credentials."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

PYTHONWARNINGS=ignore /Users/mayumikato/Library/Python/3.9/bin/gcalcli \
  --client-id="$GCAL_CLIENT_ID" \
  --client-secret="$GCAL_CLIENT_SECRET" \
  "$@"
