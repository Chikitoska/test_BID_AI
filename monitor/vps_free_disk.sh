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
  "$PROJECT_DIR/allure-results"/* \
  /tmp/chrome-* /tmp/.com.google.Chrome* /tmp/chromedriver* \
  /tmp/bid-chrome-* \
  /tmp/snap-private-tmp/snap.chromium/tmp/bid-chrome-* \
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
echo "Нужно свободно ≥1 ГБ на /. Grafana/Influx volumes не трогать."
echo "Influx не рестартить, пока Avail=0 — сгорит WAL."
