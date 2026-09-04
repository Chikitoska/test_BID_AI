#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"
# .env грузит Python (load_project_env) — не source, иначе () в UA ломают bash
exec "$PROJECT_DIR/.venv/bin/python" monitor/verify_analytics_uid.py
