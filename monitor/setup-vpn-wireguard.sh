#!/bin/bash
# WireGuard VPN для доступа к BID с VPS
# Использование: bash monitor/setup-vpn-wireguard.sh /path/to/wg0.conf
set -euo pipefail

CONF_SRC="${1:-}"

echo "=== WireGuard setup для BID ==="

if ! command -v apt-get &>/dev/null; then
  echo "ERROR: поддерживается Ubuntu/Debian"
  exit 1
fi

apt-get update -qq
apt-get install -y -qq wireguard curl

if [ -z "$CONF_SRC" ] || [ ! -f "$CONF_SRC" ]; then
  echo ""
  echo "Нужен конфиг WireGuard от IT (.conf файл)."
  echo ""
  echo "Пример использования:"
  echo "  scp wg-bid.conf root@78.17.46.33:/root/"
  echo "  bash /opt/test_BID_AI/monitor/setup-vpn-wireguard.sh /root/wg-bid.conf"
  echo ""
  echo "Шаблон /etc/wireguard/wg0.conf:"
  cat << 'EOF'

[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 10.x.x.x/24
DNS = 8.8.8.8

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

EOF
  exit 1
fi

install -m 600 "$CONF_SRC" /etc/wireguard/wg0.conf

# Поднять VPN
wg-quick down wg0 2>/dev/null || true
wg-quick up wg0
systemctl enable wg-quick@wg0

echo ""
echo "WireGuard: UP"
wg show

echo ""
echo "=== Проверка BID ==="
/opt/test_BID_AI/monitor/vpn-check.sh || true

echo ""
echo "Если BID отвечает 200/403 — запустите probe:"
echo "  /opt/test_BID_AI/monitor/run_light.sh"
