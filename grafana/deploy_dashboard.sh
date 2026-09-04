#!/usr/bin/env bash
# Залить дашборд на VPS и принудительно импортировать в Grafana.
set -euo pipefail

VPS="${VPS:-root@157.22.191.247}"
PROJECT_DIR="${PROJECT_DIR:-/opt/test_BID_AI}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "→ Копирую файлы на $VPS ..."
scp "$REPO_DIR/grafana/dashboards/bid-monitoring.json" \
  "$VPS:$PROJECT_DIR/grafana/dashboards/bid-monitoring.json"
scp "$REPO_DIR/grafana/provisioning/dashboards/default.yml" \
  "$VPS:$PROJECT_DIR/grafana/provisioning/dashboards/default.yml"
scp "$REPO_DIR/grafana/force_import_dashboard.sh" \
  "$VPS:$PROJECT_DIR/grafana/force_import_dashboard.sh"

echo "→ Принудительный import в Grafana ..."
ssh "$VPS" "chmod +x $PROJECT_DIR/grafana/force_import_dashboard.sh && \
  bash $PROJECT_DIR/grafana/force_import_dashboard.sh"

echo "Готово. Ctrl+Shift+R в браузере."
