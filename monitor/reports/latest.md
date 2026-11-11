# BID monitor digest

- Generated: `2026-11-11T20:50:03.879979+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `54066b4 fix(monitor): restore Influx graphs WRITE-only and stop ENOSPC false alerts.`

## Influx volume

- `bid_failure`: 2 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-11-11 13:11:47.902342+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-11 10:22:07.114287+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500

## health.log (FAIL/ERROR/WARN/ImportError)

```
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 22683ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 85.5s — FAIL (run_status=fail)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 184.0s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 13:23:08 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15/_00001.wal: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 169.6s
WARN: InfluxDB write failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 15:22:53 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15/_00001.wal: no space left on device"}
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 167.9s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 169.8s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 165.6s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 164.2s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 164.5s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 172.3s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 159.6s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 161.0s
plugins: rerunfailures-16.5, allure-pytest-2.16.0, playwright-0.8.0, base-url-2.1.0, xdist-3.8.0
LK pytest: 10/10 passed, failed=0, errors=0, skipped=0 in 164.8s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
WARN: InfluxDB write_pytest_run failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 14:01:24 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15/_00001.wal: no space left on device"}
WARN: InfluxDB write_check_results failed: (500)
Reason: Internal Server Error
HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json; charset=utf-8', 'X-Influxdb-Build': 'OSS', 'X-Influxdb-Version': 'v2.7.12', 'X-Platform-Error-Code': 'internal error', 'Date': 'Tue, 03 Nov 2026 14:01:24 GMT', 'Content-Length': '215'})
HTTP response body: {"code":"internal error","message":"unexpected error writing points to database: engine: error writing WAL entry: write /var/lib/influxdb2/engine/wal/9d50e68af0e6d497/autogen/15/_00001.wal: no space left on device"}
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.5s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

