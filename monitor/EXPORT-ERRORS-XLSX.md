# Выгрузка ошибок в XLSX (Grafana → Basic Auth)

Ветка: **`feature/grafana-errors-xlsx-export`**.  
**Не мержить в `main` и не выкатывать на VPS без явной отмашки.**

HTTP endpoint отдаёт Excel с колонками **дата | ошибка | прогон** (`health` / `daily` / `lk_pytest`) по measurement `bid_failure` из Influx. Период берётся из таймпикера Grafana (`${__from}` / `${__to}`).

## Env (не в git)

В `monitor/.env` (или systemd `EnvironmentFile`):

```bash
# Обязательно для export-сервиса
EXPORT_BASIC_USER=export_user
EXPORT_BASIC_PASSWORD=change_me_long_random
EXPORT_BIND=127.0.0.1
EXPORT_PORT=8765

# Уже нужны для чтения Influx (как у monitor)
INFLUXDB_URL=http://127.0.0.1:8086
INFLUXDB_TOKEN=...
INFLUXDB_ORG=bid
INFLUXDB_BUCKET=bid_monitor
```

Пароль сгенерировать, например: `openssl rand -hex 24`.

## Локально

```bash
cd /path/to/test_BID_AI
.venv/bin/pip install -r requirements.txt   # нужен openpyxl
export EXPORT_BASIC_USER=u EXPORT_BASIC_PASSWORD=p
# Influx опционален для unit-тестов; для живого ответа — токен как у monitor
./monitor/export_errors_server.sh
```

Проверка:

```bash
# без auth → 401
curl -i 'http://127.0.0.1:8765/export/errors.xlsx?from=1718452800000&to=1718539200000'

# с auth → файл .xlsx
curl -u u:p -OJ 'http://127.0.0.1:8765/export/errors.xlsx?from=${__from}&to=${__to}'
# подставьте реальные ms из Grafana (URL дашборда: from=…&to=…)

# unit без Influx
.venv/bin/pytest tests/unit/test_export_errors_xlsx.py -q
```

Путь: **`GET /export/errors.xlsx?from=…&to=…`**  
Health: **`GET /health`** (без Basic Auth).

## Grafana: кнопка с таймпикером

В дашборде `grafana/dashboards/bid-monitoring.json` добавлена **dashboard link** (верхняя панель ссылок), без изменения timeseries 🟢🔴🟠:

```text
Скачать ошибки (XLSX)
→ http://127.0.0.1:8765/export/errors.xlsx?from=${__from}&to=${__to}
```

На VPS замените host/port на публичный URL (или nginx path). Переменные Grafana:

| Переменная | Смысл |
|------------|--------|
| `${__from}` | начало диапазона таймпикера (epoch **ms**) |
| `${__to}` | конец диапазона (epoch **ms**) |

После правки JSON — импорт дашборда (`grafana/deploy_dashboard.sh` / UI Import), как обычно.

Маппинг Influx → колонка «прогон»: `health`→`health`, `full`→`daily`, `lk_pytest`→`lk_pytest`.

## VPS: systemd (минимально)

`/etc/systemd/system/bid-errors-export.service`:

```ini
[Unit]
Description=BID Grafana errors XLSX export
After=network.target docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/test_BID_AI
EnvironmentFile=/opt/test_BID_AI/monitor/.env
ExecStart=/opt/test_BID_AI/.venv/bin/python /opt/test_BID_AI/monitor/export_errors_server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# после выката ветки (когда дадут отмашку):
sudo systemctl daemon-reload
sudo systemctl enable --now bid-errors-export
sudo systemctl status bid-errors-export
```

Сервис слушает **только localhost** (`EXPORT_BIND=127.0.0.1`) — наружу через nginx.

## VPS: nginx (минимально)

```nginx
# внутри server { ... } рядом с Grafana, либо отдельный location
location /export/ {
    proxy_pass http://127.0.0.1:8765;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    # Basic Auth проверяет Python-сервис; nginx auth не обязателен
}
```

Тогда ссылка в Grafana:

```text
http://YOUR_HOST/export/errors.xlsx?from=${__from}&to=${__to}
```

Браузер спросит логин/пароль (Basic Auth).

## Что ещё не сделано на VPS

Эта ветка **только в git**. Пока нет отмашки:

- не merge в `main`
- не `systemctl enable` на сервере
- не менять nginx на проде

После merge: `pip install openpyxl`, env vars, systemd, обновить dashboard link на реальный URL, `systemctl start bid-errors-export`.
