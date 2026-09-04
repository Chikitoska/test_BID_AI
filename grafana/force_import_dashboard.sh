#!/usr/bin/env bash
# Перечитать bid-monitoring.json из provisioning (после git pull / scp).
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ ! -f grafana/dashboards/bid-monitoring.json ]]; then
  echo "Нет grafana/dashboards/bid-monitoring.json" >&2
  exit 1
fi

echo "Перезапуск Grafana (подхватит JSON с диска за ~30 с)..."
docker compose restart grafana

echo "Дашборд: http://157.22.191.247:3000/d/bid-monitoring/bid-monitoring"
echo "Обновите страницу: Ctrl+Shift+R"
