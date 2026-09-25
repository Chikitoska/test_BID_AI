#!/usr/bin/env bash
# HTTP export bid_failure → XLSX (Basic Auth). См. monitor/EXPORT-ERRORS-XLSX.md
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"
# shellcheck disable=SC1091
source "$PROJECT_DIR/.venv/bin/activate" 2>/dev/null || true
exec "$PROJECT_DIR/.venv/bin/python" monitor/export_errors_server.py
