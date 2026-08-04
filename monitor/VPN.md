# VPN на сервере для доступа к BID

С VPS `78.17.46.33` сайт `bid.gazprom-neft.ru` недоступен (timeout).  
Нужен VPN **на сервере**, чтобы probe ходил в BID через корпоративную сеть.

---

## Быстрый старт

### WireGuard

```bash
# Mac → сервер
scp wg-bid.conf root@78.17.46.33:/root/

# Сервер
bash /opt/test_BID_AI/monitor/setup-vpn-wireguard.sh /root/wg-bid.conf
```

### OpenVPN

```bash
scp bid.ovpn root@78.17.46.33:/root/
bash /opt/test_BID_AI/monitor/setup-vpn-openvpn.sh /root/bid.ovpn
```

---

## Что нужно от IT / админов

Один из вариантов:

| Тип | Что попросить |
|-----|----------------|
| **WireGuard** | файл `wg0.conf` (PrivateKey, Address, Peer, AllowedIPs) |
| **OpenVPN** | файл `.ovpn` + логин/пароль |
| **Корп. VPN** | инструкция для Linux-сервера |

**Split-tunnel** (желательно): маршрут только на `*.gazprom-neft.ru`, не весь трафик.

---

## Вариант A — WireGuard (рекомендуется)

### 1. Установка на сервере

```bash
apt-get update && apt-get install -y wireguard
```

### 2. Конфиг

Сохрани файл от IT как `/etc/wireguard/wg0.conf`:

```ini
[Interface]
PrivateKey = <ваш_ключ>
Address = 10.x.x.x/24
DNS = 8.8.8.8

[Peer]
PublicKey = <ключ_сервера>
Endpoint = vpn.company.ru:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

Для **split-tunnel** только Gazprom:

```ini
AllowedIPs = 10.0.0.0/8, 172.16.0.0/12
```

(уточни подсети у IT)

### 3. Запуск

```bash
chmod 600 /etc/wireguard/wg0.conf
wg-quick up wg0
systemctl enable wg-quick@wg0
```

### 4. Проверка BID

```bash
/opt/test_BID_AI/monitor/vpn-check.sh
```

Ожидание: `bid.gazprom-neft.ru → HTTP 200` (или 403 — но не timeout).

### 5. Probe после VPN

```bash
/opt/test_BID_AI/monitor/run_light.sh
```

Grafana должна стать зелёной, Telegram — короткий OK или коды 403/502 если реальная проблема.

---

## Вариант B — OpenVPN

```bash
apt-get install -y openvpn
openvpn --config /etc/openvpn/bid.ovpn --daemon
/opt/test_BID_AI/monitor/vpn-check.sh
```

---

## Автопроверка VPN перед probe (опционально)

Если VPN иногда падает, добавь в cron **перед** probe:

```cron
*/10 * * * * wg-quick up wg0 2>/dev/null; /opt/test_BID_AI/monitor/run_light.sh >> /opt/test_BID_AI/monitor/probe.log 2>&1
```

---

## Telegram через VPN не нужен

`api.telegram.org` должен идти **мимо** корп. VPN (split-tunnel).  
Иначе Telegram на сервере может перестать работать.

---

## Если VPN нет

Альтернативы:

1. VPS в корп. сети / облаке Gazprom  
2. Мониторинг с рабочей машины (не ideal для prod)  
3. Попросить IT whitelist IP `78.17.46.33` для BID  

---

## Файлы

```
monitor/vpn-check.sh   — проверка доступа к BID
monitor/VPN.md         — эта инструкция
```
