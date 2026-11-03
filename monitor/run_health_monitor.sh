#!/bin/bash
# Health-мониторинг: лендинг (HTTP) + чат-бот + ЛК (вход, ФИО, компания)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# shellcheck source=/dev/null
. "$SCRIPT_DIR/rotate_logs.sh"
rotate_monitor_log "$PROJECT_DIR/monitor/health.log"

if [ -f monitor/.env ]; then
  set -a
  # shellcheck disable=SC1091
  source monitor/.env
  set +a
fi

# Слот cron 5 мин: TERM → python пишет bid_lk_run; иначе KILL.
PYTHON="$PROJECT_DIR/.venv/bin/python"
if command -v timeout >/dev/null 2>&1; then
  exec timeout --signal=TERM --kill-after=15 220 "$PYTHON" monitor/run_health_monitor.py
fi
exec "$PYTHON" monitor/run_health_monitor.py
