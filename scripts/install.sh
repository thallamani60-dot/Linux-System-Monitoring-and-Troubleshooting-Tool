#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT_DIR/.venv"
if [[ $EUID -eq 0 ]]; then echo 'Run as the project owner, not root.' >&2; exit 1; fi
python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r "$ROOT_DIR/requirements.txt"
printf 'Environment ready at %s\nRun: %s/bin/python %s/monitor.py\n' "$VENV" "$VENV" "$ROOT_DIR"
