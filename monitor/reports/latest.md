# BID monitor digest

- Generated: `2026-10-26T20:50:03.873049+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_failure`: 3 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-26 11:01:48.804098+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/error/500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-10-26 10:57:48.253745+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/service-providers | ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
- `2026-10-26 06:46:07.335188+00:00` | Лендинг + мин ЛК (5 мин) | `lk_company_badge` | ЛК: компания в шапке | lk_company_badge | https://lk.bid.gazprom-neft.ru/service-providers | Message:

## health.log (FAIL/ERROR/WARN/ImportError)

```
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 14491ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 123.4s — FAIL (run_status=fail)
[FAIL] lk_auth_login 78888ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 162.2s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NewConnectionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to establish a new connection: [Errno 111] Connection refused"))), повтор через 10 с (ещё 1 раз)…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 15916ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 126.3s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 23509ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 135.6s — FAIL (run_status=fail)
[FAIL] lk_company_badge 45067ms Message:
Alert suppressed: health failure classified as autotest (UI flake / Chrome/WebDriver) — Grafana orange; not paging as LK/PROD down
Health monitor finished in 62.8s — FAIL_AUTOTEST (run_status=autotest)
[FAIL] lk_auth_login 83259ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 163.6s — FAIL (run_status=fail)
[FAIL] lk_auth_login 20892ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 104.2s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 248.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 260.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 282.4s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 12.0s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 9.2s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 9.5s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 12.0s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

