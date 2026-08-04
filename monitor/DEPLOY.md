# Мониторинг BID: Grafana + InfluxDB + Cron

## Что нужно от вас (чек-лист)

### 1. Сервер (VPS)

| Параметр | Пример | Зачем |
|----------|--------|-------|
| **IP / hostname** | `203.0.113.10` | SSH и доступ к Grafana |
| **SSH-доступ** | user + ключ или пароль | Установка и cron |
| **ОС** | Ubuntu 22.04 / Debian 12 | Docker + Python |
| **RAM** | минимум 2 GB | InfluxDB + Grafana + Chrome (если UI) |
| **Диск** | 10+ GB | История метрик |

### 2. Сеть

| Вопрос | Нужно |
|--------|-------|
| Сервер **видит** `https://bid.gazprom-neft.ru/`? | Да — иначе мониторинг бессмысленен |
| Нужен VPN / корп. сеть? | Уточните — с вашего Mac сайт открывается |
| Открытые порты | `3000` Grafana, `8086` InfluxDB (лучше только localhost + nginx) |

### 3. Секреты (вы создаёте)

```bash
# Сгенерировать токен InfluxDB (на сервере):
openssl rand -hex 32
```

| Переменная | Кто создаёт | Где хранится |
|------------|-------------|--------------|
| `INFLUXDB_TOKEN` | вы | `monitor/.env` + `.env` для docker |
| `GRAFANA_ADMIN_PASSWORD` | вы | `.env` для docker |
| `INFLUXDB_ADMIN_PASSWORD` | вы | `.env` для docker |
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) | `monitor/.env` |
| `TELEGRAM_CHAT_ID` | [@userinfobot](https://t.me/userinfobot) | `monitor/.env` |

### 4. Расписание

| Параметр | По умолчанию | Можно изменить |
|----------|--------------|----------------|
| Время прогона | **08:00** ежедневно | crontab |
| Часовой пояс | `Europe/Moscow` | `monitor/.env` |
| UI-тесты в cron | **выключены** | `MONITOR_RUN_UI=true` |

### 5. Доступ к дашборду

- Как заходить: `http://IP:3000` или домен через nginx
- Логин Grafana: `admin` + ваш пароль
- Кто должен видеть дашборд: только вы / команда

---

## Быстрая установка на сервере `78.17.46.33`

> Docker на сервере **нет** — скрипт установит его автоматически.

### Шаг A — скопировать проект на сервер (с вашего Mac)

```bash
scp -r ~/Projects/test_BID_AI user@78.17.46.33:/opt/
```

Замените `user` на ваш SSH-логин (например `root` или `ubuntu`).

### Шаг B — на сервере

```bash
ssh user@78.17.46.33
cd /opt/test_BID_AI
bash monitor/install_server.sh
```

Скрипт: установит Docker → Python venv → создаст `.env` → поднимет Grafana + InfluxDB.

### Шаг C — после установки

```bash
./monitor/run_daily.sh          # тестовый прогон
```

Grafana: **http://78.17.46.33:3000** (логин/пароль — в файле `/opt/test_BID_AI/.env`)

---

## Быстрая установка на сервере (ручная)

```bash
# 1. Клонировать / скопировать проект
sudo mkdir -p /opt/test_BID_AI
sudo chown $USER:$USER /opt/test_BID_AI
# scp или git clone вашего test_BID_AI в /opt/test_BID_AI

# 2. Python окружение
cd /opt/test_BID_AI
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
playwright install chromium   # только если MONITOR_RUN_UI=true

# 3. Docker (если нет)
# curl -fsSL https://get.docker.com | sh

# 4. Настроить секреты
cp .env.example .env
cp monitor/.env.example monitor/.env
# отредактировать оба файла — одинаковый INFLUXDB_TOKEN

# 5. Поднять Grafana + InfluxDB
docker compose up -d

# 6. Grafana: Connections → Data sources → InfluxDB-BID
#    вставить INFLUXDB_TOKEN если datasource не подхватился

# 7. Проверка мониторинга вручную
chmod +x monitor/run_daily.sh
./monitor/run_daily.sh

# 8. Cron (ежедневно в 08:00 MSK)
crontab -e
# добавить:
0 8 * * * /opt/test_BID_AI/monitor/run_daily.sh >> /opt/test_BID_AI/monitor/cron.log 2>&1
```

---

## Prod-мониторинг (рекомендуется)

Два уровня проверок:

| Режим | Скрипт | Частота | Что делает | Telegram |
|-------|--------|---------|------------|----------|
| **Probe** | `run_light.sh` | каждые 10 мин | только HTTP | падение / восстановление |
| **Full** | `run_daily.sh` | 2 раза в день | HTTP + pytest API | сводка OK или алерт FAIL |

### Настройки в `monitor/.env`

```env
TELEGRAM_ALERT_ON_SUCCESS=false
TELEGRAM_FULL_RUN_SUMMARY=true
TELEGRAM_ALERT_REPEAT_HOURS=4
```

- **Probe** не шлёт «всё OK» каждые 10 минут
- При длительном падении — повторный алерт раз в 4 часа
- **Full** — краткая сводка 2 раза в день (08:00 и 20:00)

### Cron на сервере

```bash
crontab -e
```

```cron
# HTTP-probe каждые 10 минут
*/10 * * * * /opt/test_BID_AI/monitor/run_light.sh >> /opt/test_BID_AI/monitor/probe.log 2>&1

# Полный прогон pytest — 08:00 и 20:00 МСК (сервер в UTC: 05:00 и 17:00)
0 5,17 * * * /opt/test_BID_AI/monitor/run_daily.sh >> /opt/test_BID_AI/monitor/cron.log 2>&1
```

Проверка:

```bash
chmod +x /opt/test_BID_AI/monitor/run_light.sh
/opt/test_BID_AI/monitor/run_light.sh
/opt/test_BID_AI/monitor/run_daily.sh
crontab -l
```

---

## Что записывается в InfluxDB

| Measurement | Поля | Смысл |
|-------------|------|-------|
| `bid_check` | success, http_code, duration_ms, error | Каждый URL/API |
| `bid_probe` | success, failed_checks, duration_sec | Итог HTTP-probe |
| `bid_run` | total, passed, failed, success | Итог pytest |

---

## Telegram алерты

| Событие | Когда |
|---------|-------|
| 🔴 Probe FAIL | первое падение HTTP |
| 🔴 Probe FAIL (повтор) | всё ещё падает через 4 ч |
| 🟢 Восстановлено | HTTP снова OK |
| 🟢 Full OK | сводка после pytest (2×/день) |
| 🔴 Full FAIL | pytest или HTTP упали |

Без `TELEGRAM_*` мониторинг работает, но алерты только в логах.

---

## Файлы мониторинга

```
monitor/
├── run_light.py      # HTTP-probe (prod, каждые 10 мин)
├── run_light.sh
├── run_daily.py      # полный прогон + pytest
├── run_daily.sh
├── alert_policy.py   # логика алертов без спама
├── state.py
├── checks.py
├── metrics.py
├── alerts.py
└── DEPLOY.md
```

---

## Что прислать мне для финальной настройки

1. IP сервера и OS  
2. Есть ли Docker (`docker --version`)  
3. Открывается ли BID **с сервера**: `curl -I https://bid.gazprom-neft.ru/`  
4. Нужен ли Telegram (да/нет)  
5. Время cron (оставить 08:00?)  
6. Домен для Grafana или только IP:3000  

После этого можно донастроить nginx, firewall и datasource Grafana под ваш сервер.
