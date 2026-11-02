# BID monitor digest

- Generated: `2026-11-02T20:50:04.032152+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `829102f chore(monitor): one-shot rewrite of 13:26/13:31 health bars to ok.`

## Influx volume

- `bid_failure`: 27 точек (~1д)
- `bid_lk_pytest`: 50 точек (~1д)
- `bid_lk_run`: 1064 точек (~1д)
- `bid_run`: 5 точек (~1д)

## Failures (bid_failure)

- `2026-11-02 11:28:29.468275+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_icon` | Лендинг: иконка чат-бота | landing_chatbot_icon | landing | https://bid.gazprom-neft.ru/ | Лендинг: иконка чат-бота не отображается
- `2026-11-02 10:51:02.093134+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_icon` | Лендинг: иконка чат-бота | landing_chatbot_icon | landing | https://bid.gazprom-neft.ru/ | Лендинг: иконка чат-бота не отображается
- `2026-11-02 10:31:56.900730+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_icon` | Лендинг: иконка чат-бота | landing_chatbot_icon | landing | https://bid.gazprom-neft.ru/ | Лендинг: иконка чат-бота не отображается
- `2026-11-02 10:26:31.003011+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_icon` | Лендинг: иконка чат-бота | landing_chatbot_icon | landing | https://bid.gazprom-neft.ru/ | Лендинг: иконка чат-бота не отображается
- `2026-11-02 11:28:29.468275+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/service-providers | ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers

## health.log (FAIL/ERROR/WARN/ImportError)

```
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:30:49 GMT', 'Content-Length': '434'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST786485473\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST786485473: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:30:49 GMT', 'Content-Length': '432'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST99846058\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST99846058: no space left on device"}
WARN: InfluxDB write_lk_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:35:55 GMT', 'Content-Length': '436'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST3201908114\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST3201908114: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:35:55 GMT', 'Content-Length': '436'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST2327689636\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST2327689636: no space left on device"}
WARN: InfluxDB write_lk_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:40:50 GMT', 'Content-Length': '434'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST480614714\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST480614714: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:40:50 GMT', 'Content-Length': '436'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST3351751695\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST3351751695: no space left on device"}
WARN: InfluxDB write_lk_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:45:51 GMT', 'Content-Length': '436'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST2731366068\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST2731366068: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:45:51 GMT', 'Content-Length': '436'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST1187396019\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST1187396019: no space left on device"}
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 184.1s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 179.8s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 204.7s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 11:23:29 GMT', 'Content-Length': '161'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/data/9d50e68af0e6d497: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 186.4s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 13:23:10 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/14/_00001.wal: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 177.6s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 15:23:01 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/14/_00001.wal: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 187.5s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 17:23:12 GMT', 'Content-Length': '434'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: manifest write failed for \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST\": failed writing temporary manifest file \"/var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST581542791\": write /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/MANIFEST581542791: no space left on device"}
```

## cron.log (daily) tail markers

```
Metrics sent to InfluxDB (run_status=autotest)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 6.4s
Metrics sent to InfluxDB (run_status=autotest)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.1s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
[FAIL] spa_counter_js 0 26210ms HTTPSConnectionPool(host='spa-back.gazprom-neft.ru', port=443): Read timed out. (read timeout=25)
[FAIL] external_counter.js 0 25137ms HTTPSConnectionPool(host='spa-back.gazprom-neft.ru', port=443): Read timed out. (read timeout=25)
Pytest: 34/39 passed, failed=5, errors=0 in 162.7s
Metrics sent to InfluxDB (run_status=fail)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.6s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 14:01:36 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/14/_00001.wal: no space left on device"}
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

