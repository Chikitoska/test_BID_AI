#!/bin/bash
# Освободить место на VPS 15 ГБ. Grafana/Influx volumes не удаляем.
# Запуск: bash /opt/test_BID_AI/monitor/vps_free_disk.sh
#
# Cron каждые 20 мин (после git pull на VPS):
#   */20 * * * * /bin/bash /opt/test_BID_AI/monitor/vps_free_disk.sh >> /opt/test_BID_AI/monitor/disk.log 2>&1
#
# НИКОГДА: docker volume prune, docker restart influx, удаление grafana/influx data.
set -u
PROJECT_DIR="${PROJECT_DIR:-/opt/test_BID_AI}"

echo "=== до ==="
df -h /

journalctl --vacuum-size=50M >/dev/null 2>&1 || true
apt-get clean >/dev/null 2>&1 || true

for f in health.log cron.log lk-pytest.log digest.log probe.log disk.log; do
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
  2>/dev/null || true

# leftover bid-chrome-* кроме живого профиля (health/combat может идти прямо сейчас)
swept=0
if [ -x "$PROJECT_DIR/.venv/bin/python" ]; then
  if (
    cd "$PROJECT_DIR" &&
    PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}" \
      "$PROJECT_DIR/.venv/bin/python" -c \
      "from utils.selenium_factory import sweep_stale_bid_chrome_profiles; sweep_stale_bid_chrome_profiles()"
  ); then
    swept=1
  fi
fi
if [ "$swept" -eq 0 ]; then
  live=$(ps -ax -o args= 2>/dev/null | tr ' ' '\n' | sed -n 's|^--user-data-dir=.*/\(bid-chrome-[^/]*\)$|\1|p' | sort -u)
  for d in /tmp/bid-chrome-* /tmp/snap-private-tmp/snap.chromium/tmp/bid-chrome-*; do
    [ -e "$d" ] || continue
    base=$(basename "$d")
    if [ -n "$live" ] && printf '%s\n' "$live" | grep -qx "$base"; then
      echo "skip live $d"
      continue
    fi
    rm -rf "$d" 2>/dev/null || true
  done
fi

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
