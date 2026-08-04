#!/bin/bash
# Быстрый HTTP-probe для cron (каждые 5–10 мин)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

if [ -f monitor/.env ]; then
  set -a
  # shellcheck disable=SC1091
  source monitor/.env
  set +a
fi

exec "$PROJECT_DIR/.venv/bin/python" monitor/run_light.py
