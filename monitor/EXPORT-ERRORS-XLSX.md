# Выгрузка ошибок в XLSX (Grafana → Basic Auth)

Влито в **`main`** (merge `6c0aa5b`). Выкат на VPS — по чеклисту ниже.

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
→ http://157.22.191.247/export/errors.xlsx?from=${__from}&to=${__to}
```

Прод-шаблон в JSON (через nginx `/export/`). Локально для отладки сервиса: `http://127.0.0.1:8765/...`. Переменные Grafana:

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

Ссылка в Grafana уже на прод:

```text
http://157.22.191.247/export/errors.xlsx?from=${__from}&to=${__to}
```

Браузер спросит логин/пароль (Basic Auth).

## VPS после merge (copy-paste)

На `root@157.22.191.247`, репо `/opt/test_BID_AI`:

1. `cd /opt/test_BID_AI && git pull origin main`
2. `.venv/bin/pip install -r requirements.txt` (нужен `openpyxl`)
3. В `monitor/.env` добавить `EXPORT_BASIC_*` / `EXPORT_BIND` / `EXPORT_PORT` (см. выше)
4. Создать unit из секции systemd выше → `daemon-reload` → `enable --now bid-errors-export`
5. Добавить nginx `location /export/` → `nginx -t && reload`
6. `bash grafana/force_import_dashboard.sh` (или с Mac: `bash grafana/deploy_dashboard.sh`) — проверить link URL
7. Smoke: `curl -i http://127.0.0.1:8765/health` и `curl -u USER:PASS -OJ 'http://127.0.0.1:8765/export/errors.xlsx?from=…&to=…'` (снаружи — через `http://157.22.191.247/export/...`)
