# Мониторинг BID с MacBook (когда VPS заблокирован WAF)

С Mac: `403` — сайт **доступен**, WAF режет.  
С VPS: `timeout` — IP датацентра **заблокирован**. Whitelist невозможен.

**Схема:** probe с Mac → InfluxDB на VPS → Grafana на VPS.

```
MacBook (cron probe)  ──HTTP──►  bid.gazprom-neft.ru  ✅
MacBook               ──write──►  78.17.46.33:8086     InfluxDB
Browser               ──view───►  78.17.46.33:3000     Grafana
```

---

## 1. Проверь API с Mac (без VPN)

```bash
curl -s -o /dev/null -w "main: %{http_code}\n" https://bid.gazprom-neft.ru/
curl -s -o /dev/null -w "config: %{http_code}\n" https://bid.gazprom-neft.ru/config.json
curl -s -o /dev/null -w "version: %{http_code}\n" https://bid.gazprom-neft.ru/version
```

| Код | Смысл |
|-----|-------|
| 200 | OK для мониторинга |
| 403 | WAF — см. `MONITOR_ACCEPT_CODES` ниже |
| 000 / timeout | сеть недоступна |

---

## 2. `monitor/.env` на Mac

```env
INFLUXDB_URL=http://78.17.46.33:8086
INFLUXDB_TOKEN=<тот же что на сервере>
INFLUXDB_ORG=bid
INFLUXDB_BUCKET=bid_monitor

TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

TELEGRAM_ALERT_ON_SUCCESS=false
TELEGRAM_FULL_RUN_SUMMARY=true
TELEGRAM_ALERT_REPEAT_HOURS=4
```

Токен InfluxDB — с сервера:

```bash
ssh root@78.17.46.33 "grep INFLUXDB_TOKEN /opt/test_BID_AI/.env"
```

Если главная 403, а API 200 — **не** добавляй `MONITOR_ACCEPT_CODES`.  
Если всё 403, но сайт в браузере открывается:

```env
MONITOR_ACCEPT_CODES=403
```

---

## 3. Открыть InfluxDB на VPS (только для твоего IP)

На сервере — узнай свой домашний IP: https://ifconfig.me (с Mac)

```bash
MY_IP=<твой_IP_с_Mac>
ufw allow from $MY_IP to any port 8086 proto tcp
ufw status
```

Проверка с Mac:

```bash
curl -s -o /dev/null -w "%{http_code}" http://78.17.46.33:8086/health
```

---

## 4. Probe с Mac

```bash
cd ~/Projects/test_BID_AI
./monitor/run_light.sh
```

---

## 5. Cron на Mac

```bash
crontab -e
```

```cron
*/10 * * * * /Users/nikitasmirnov/Projects/test_BID_AI/monitor/run_light.sh >> /Users/nikitasmirnov/Projects/test_BID_AI/monitor/probe.log 2>&1
0 8,20 * * * /Users/nikitasmirnov/Projects/test_BID_AI/monitor/run_daily.sh >> /Users/nikitasmirnov/Projects/test_BID_AI/monitor/cron.log 2>&1
```

**Mac должен быть включён** в эти моменты.

Telegram с Mac: если `api.telegram.org` не открывается — включай VPN **только для probe** или используй `TELEGRAM_PROXY`.

---

## 6. Отключить probe на VPS (чтобы не спамил FAIL)

На сервере:

```bash
crontab -e
```

Удали или закомментируй строку `run_light.sh`.  
Grafana + InfluxDB + `run_daily` на VPS можно оставить или тоже перенести на Mac.

---

## Ограничения

| | Mac | VPS |
|--|-----|-----|
| Доступ к BID | ✅ 403/200 | ❌ timeout |
| 24/7 без Mac | ❌ | ✅ инфра |
| Prod как у больших команд | ⚠️ компромисс | ✅ если бы IP пускали |

Идеал для prod без whitelist: **VPS в другой сети**, откуда BID отвечает не timeout.
