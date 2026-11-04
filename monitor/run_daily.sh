#!/bin/bash
# Запуск ежедневного мониторинга (для cron)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# shellcheck source=/dev/null
. "$SCRIPT_DIR/rotate_logs.sh"
rotate_monitor_log "$PROJECT_DIR/monitor/cron.log"

if [ -f monitor/.env ]; then
  set -a
  # shellcheck disable=SC1091
  source monitor/.env
  set +a
fi

# Минцифр не должен висеть часами: TERM после 10 мин (bid_run уже записан раньше UI).
PYTHON="$PROJECT_DIR/.venv/bin/python"
if command -v timeout >/dev/null 2>&1; then
  exec timeout --signal=TERM --kill-after=15 600 "$PYTHON" monitor/run_daily.py
fi
exec "$PYTHON" monitor/run_daily.py
