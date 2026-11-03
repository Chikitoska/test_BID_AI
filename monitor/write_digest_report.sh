#!/bin/bash
# Digest мониторинга → monitor/reports/latest.md и (по умолчанию) push в GitHub.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"
# shellcheck source=/dev/null
. "$SCRIPT_DIR/rotate_logs.sh"
rotate_monitor_log "$PROJECT_DIR/monitor/digest.log"
HOURS="${1:-12}"
exec "$PROJECT_DIR/.venv/bin/python" monitor/write_digest_report.py "$HOURS" --push
