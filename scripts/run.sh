#!/usr/bin/env bash
# Run the Python health check from any working directory.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT_DIR/monitor.py" "$@"
