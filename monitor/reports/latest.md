# BID monitor digest

- Generated: `2026-11-16T20:50:16.396600+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `54066b4 fix(monitor): restore Influx graphs WRITE-only and stop ENOSPC false alerts.`

## Influx volume

- `bid_failure`: 11 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-11-16 12:36:11.193939+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 12:01:15.890505+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:56:09.085363+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:51:08.511723+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:46:16.502606+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:41:47.403278+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:16:27.559136+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:11:24.417871+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 11:06:31.565125+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-11-16 09:17:47.768881+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/service-providers | ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
- `2026-11-16 11:40:42.164053+00:00` | Боевой прогон ЛК (2 ч) | `pytest` | Pytest: ошибка окружения | Pytest не запустился: |     self._report_item(container) |   File "/opt/test_BID_AI/.venv/lib/python3.12/site-packages/allure_commons/logger.py", line 25, in _report_item |     with io.open(self._report_dir / filename, "w", encoding="utf8") as json_file: |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | FileNotFoundError: [Errno 2] No such file or directory: '/opt/test_B

## health.log (FAIL/ERROR/WARN/ImportError)

```
Health monitor finished in 84.8s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 14947ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 2/1
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 79.9s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 17501ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 3/1
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 83.0s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 14975ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 5/1
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 72.0s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 13610ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 6/1
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 63.9s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 10895ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 7/1
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 64.5s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 10 с (слот 5xx не greening)…
[FAIL] lk_auth_login 12546ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 66.3s — FAIL (run_status=fail)
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

