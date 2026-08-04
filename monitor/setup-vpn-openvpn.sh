#!/bin/bash
# OpenVPN для доступа к BID с VPS
# Использование: bash monitor/setup-vpn-openvpn.sh /path/to/bid.ovpn
set -euo pipefail

OVPN_SRC="${1:-}"

echo "=== OpenVPN setup для BID ==="

apt-get update -qq
apt-get install -y -qq openvpn curl

if [ -z "$OVPN_SRC" ] || [ ! -f "$OVPN_SRC" ]; then
  echo ""
  echo "Нужен файл .ovpn от IT."
  echo ""
  echo "Пример:"
  echo "  scp bid.ovpn root@78.17.46.33:/root/"
  echo "  bash /opt/test_BID_AI/monitor/setup-vpn-openvpn.sh /root/bid.ovpn"
  exit 1
fi

install -m 600 "$OVPN_SRC" /etc/openvpn/client/bid.conf

# auth-user-pass если нужен логин/пароль — создайте /etc/openvpn/client/bid.auth
if grep -q "auth-user-pass" /etc/openvpn/client/bid.conf; then
  if [ ! -f /etc/openvpn/client/bid.auth ]; then
    echo "Создайте /etc/openvpn/client/bid.auth (2 строки: login, password)"
    echo "  nano /etc/openvpn/client/bid.auth && chmod 600 /etc/openvpn/client/bid.auth"
    echo "  sed -i 's|auth-user-pass|auth-user-pass /etc/openvpn/client/bid.auth|' /etc/openvpn/client/bid.conf"
  fi
fi

systemctl enable openvpn-client@bid
systemctl restart openvpn-client@bid
sleep 3
systemctl status openvpn-client@bid --no-pager || true

echo ""
/opt/test_BID_AI/monitor/vpn-check.sh || true
