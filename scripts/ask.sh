#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR%/scripts}"
VENV_PATH="$PROJECT_ROOT/.venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "❌ Virtual environment not found at $VENV_PATH"
  echo "Run ./install.sh first to set up dependencies."
  exit 1
fi

source "$VENV_PATH/bin/activate"

ENV_FILE="$PROJECT_ROOT/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

# Ensure src/ is on PYTHONPATH so `python -m gazzali.ask` resolves
export PYTHONPATH="$PROJECT_ROOT/src:${PYTHONPATH:-}"

python -m gazzali.ask "$@"

