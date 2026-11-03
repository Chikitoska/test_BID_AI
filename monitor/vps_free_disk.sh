#!/bin/bash
# Освободить место на VPS 15 ГБ. Grafana/Influx volumes не удаляем.
# Запуск: bash /opt/test_BID_AI/monitor/vps_free_disk.sh
set -u
PROJECT_DIR="${PROJECT_DIR:-/opt/test_BID_AI}"

echo "=== до ==="
df -h /

journalctl --vacuum-size=50M >/dev/null 2>&1 || true
apt-get clean >/dev/null 2>&1 || true

for f in health.log cron.log lk-pytest.log digest.log probe.log; do
  log="$PROJECT_DIR/monitor/$f"
  if [ -f "$log" ]; then
    tail -n 3000 "$log" > "${log}.tmp" && mv "${log}.tmp" "$log"
  fi
done

rm -rf \
  "$PROJECT_DIR/artifacts"/* \
  "$PROJECT_DIR/.selenium_cache" \
  /tmp/chrome-* /tmp/.com.google.Chrome* /tmp/chromedriver* \
  2>/dev/null || true

find /var/lib/docker/containers -name '*-json.log' -size +5M -exec truncate -s 0 {} \; 2>/dev/null || true
docker builder prune -af >/dev/null 2>&1 || true
docker image prune -af >/dev/null 2>&1 || true

echo "=== после ==="
df -h /
echo
echo "Крупные каталоги:"
du -xh --max-depth=1 /opt /var/lib /var/log 2>/dev/null | sort -h | tail -15
echo
docker system df 2>/dev/null || true
echo
echo "Нужно свободно ≥1 ГБ на /. Потом:"
echo "  docker restart bid-influxdb"
echo "  cd $PROJECT_DIR && git checkout -- monitor/reports/latest.md && git pull"
echo "  .venv/bin/python monitor/rewrite_health_ok.py --apply"
echo "  .venv/bin/python monitor/rewrite_missing_daily.py --apply"
