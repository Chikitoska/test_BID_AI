#!/bin/bash
# Проверка доступа к BID с сервера (после настройки VPN)
set -euo pipefail

echo "=== VPN / BID check ==="

if command -v wg &>/dev/null && wg show 2>/dev/null | grep -q interface; then
  echo "WireGuard: UP ($(wg show interfaces))"
else
  echo "WireGuard: not running"
fi

for url in \
  "https://bid.gazprom-neft.ru/" \
  "https://bid.gazprom-neft.ru/config.json" \
  "https://spa-back.gazprom-neft.ru/static/counter.js"
do
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "$url" || echo "000")
  echo "$url → HTTP $code"
done

echo ""
echo "200/301/302 = OK | 403 = доступ есть, WAF | 000/timeout = VPN не помог"
