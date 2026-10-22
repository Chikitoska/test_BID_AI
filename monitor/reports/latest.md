# BID monitor digest

- Generated: `2026-10-22T08:50:01.311170+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_failure`: 5 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

(ошибок bid_failure за период нет)

## health.log (FAIL/ERROR/WARN/ImportError)

```
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 54232ms Message: timeout: Timed out receiving message from renderer: -0.001
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 120.4s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 19495ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 130.6s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 59247ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 2/2
Health monitor finished in 178.4s — FAIL (run_status=fail)
[FAIL] lk_auth_login 71761ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 3/2
Health monitor finished in 150.6s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 14491ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 123.4s — FAIL (run_status=fail)
[FAIL] lk_auth_login 78888ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 162.2s — FAIL (run_status=fail)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 260.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 262.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 259.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 268.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 263.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 283.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 259.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 260.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 507.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 260.4s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.2s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.5s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 14.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 9.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

