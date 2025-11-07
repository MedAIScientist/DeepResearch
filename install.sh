#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
VENV_PATH="$PROJECT_ROOT/.venv"

info() {
  printf "\033[1;34m[INFO]\033[0m %s\n" "$1"
}

warn() {
  printf "\033[1;33m[WARN]\033[0m %s\n" "$1"
}

error() {
  printf "\033[1;31m[ERROR]\033[0m %s\n" "$1" >&2
  exit 1
}

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  error "Python executable '$PYTHON_BIN' not found. Set PYTHON_BIN or install Python 3.10+."
fi

info "Creating virtual environment at $VENV_PATH"
"$PYTHON_BIN" -m venv "$VENV_PATH"

source "$VENV_PATH/bin/activate"

info "Upgrading pip"
pip install --upgrade pip

if [ ! -f "$PROJECT_ROOT/requirements.txt" ]; then
  error "requirements.txt not found in project root."
fi

info "Installing Python dependencies"
pip install -r "$PROJECT_ROOT/requirements.txt"

ENV_FILE="$PROJECT_ROOT/.env"

if [ -f "$ENV_FILE" ]; then
  warn ".env already exists. Skipping credential prompts."
else
  info "Collecting API credentials for Tongyi DeepResearch workflow"
  read -r -p "OpenRouter API key (sk-or-...): " OPENROUTER_API_KEY
  read -r -p "Serper API key: " SERPER_API_KEY
  read -r -p "Jina API key: " JINA_API_KEY

  cat >"$ENV_FILE" <<EOF
OPENROUTER_API_KEY="$OPENROUTER_API_KEY"
SERPER_API_KEY="$SERPER_API_KEY"
JINA_API_KEY="$JINA_API_KEY"

# Optional overrides
MODEL_PATH=""
OUTPUT_PATH=""
TEMPERATURE="0.85"
PRESENCE_PENALTY="1.1"
MAX_WORKERS="1"
ROLLOUT_COUNT="1"
EOF

  info "Credential file written to $ENV_FILE"
fi

cat <<'EOM'

==============================================================
Eye of Prometheus setup complete!

Next steps:
1. source .venv/bin/activate
2. Run the CLI from project root, e.g.
   python -m eye_of_prometheus.ask "What are the latest AI safety milestones?"

Refer to README.md for detailed usage instructions.
==============================================================
EOM

