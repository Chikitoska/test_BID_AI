# BID monitor digest

- Generated: `2026-11-03T08:50:01.600893+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `652f0a8 fix(monitor): restore overnight combat bars that Influx dropped on full disk.`

## Influx volume

- `bid_failure`: 1 точек (~1д)
- `bid_lk_pytest`: 55 точек (~1д)
- `bid_lk_run`: 1064 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-11-03 05:26:31.330429+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_topics` | Лендинг: темы чат-бота | landing_chatbot_topics | landing | https://bid.gazprom-neft.ru/ | Лендинг: после открытия чата темы не отображаются. Текст: 'Ассистент\nНеизвестная ошибка\n\nСейчас ассистент недоступен — попробуйте вернуться позже или обратитесь в поддержку'

## health.log (FAIL/ERROR/WARN/ImportError)

```
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:21:36 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
WARN: InfluxDB write_lk_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:25:49 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:25:49 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
WARN: InfluxDB write_lk_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:30:42 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:30:42 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
WARN: InfluxDB write_lk_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:35:50 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
WARN: InfluxDB write checks failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:35:50 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
[FAIL] landing_chatbot_topics 30078ms Лендинг: после открытия чата темы не отображаются. Текст: 'Ассистент\nНеизвестная ошибка\n\nСейчас ассистент недоступен — попробуйте вернуться позже или обратитесь в поддержку'
Alert suppressed: health failure classified as autotest (UI flake / Chrome/WebDriver) — Grafana orange; not paging as LK/PROD down
Health monitor finished in 89.1s — FAIL_AUTOTEST (run_status=autotest)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 19:23:05 GMT', 'Content-Length': '195'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: open /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/L0-00000100.tsl: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 171.2s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 21:22:55 GMT', 'Content-Length': '195'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: open /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/L0-00000151.tsl: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 179.4s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Mon, 02 Nov 2026 23:23:03 GMT', 'Content-Length': '195'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: open /var/lib/influxdb2/engine/data/9d50e68af0e6d497/autogen/14/index/7/L0-00000202.tsl: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 165.3s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 01:22:49 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 170.5s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 03:22:54 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 193.0s
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 02:01:16 GMT', 'Content-Length': '171'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: mkdir /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15: no space left on device"}
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

