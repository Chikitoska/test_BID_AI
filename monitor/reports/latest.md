# BID monitor digest

- Generated: `2026-10-15T20:50:22.689290+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1148 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

(ошибок bid_failure за период нет)

## health.log (FAIL/ERROR/WARN/ImportError)

```
Health monitor finished in 80.6s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 17301ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 126.2s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 30005ms Message: timeout: Timed out receiving message from renderer: 26.752
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 70.8s — FAIL (run_status=fail)
[FAIL] lk_auth_login 16795ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 79.8s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 77406ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 147.2s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 15846ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 132.7s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<HTTPSConnection(host='bid.gazprom-neft.ru', port=443) at 0x7f837c5441a0>, 'Connection to bid.gazprom-neft.ru timed out. (connect timeout=15)'))), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<HTTPSConnection(host='bid.gazprom-neft.ru', port=443) at 0x7428f031fad0>, 'Connection to bid.gazprom-neft.ru timed out. (connect timeout=15)'))), повтор через 10 с (ещё 1 раз)…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 351.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 273.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 514.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 263.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 272.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 277.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 272.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 260.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.7s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.2s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 9.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.6s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

