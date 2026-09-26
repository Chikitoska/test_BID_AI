# BID monitor digest

- Generated: `2026-09-26T20:50:02.695848+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `06f4535 Merge pull request #14 from Chikitoska/feature/http-error-confirm-retry`

## Influx volume

- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

(ошибок bid_failure за период нет)

## health.log (FAIL/ERROR/WARN/ImportError)

```
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 19920ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 4/1
Health monitor finished in 136.5s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] lk_auth_login 46675ms Message:
Alert suppressed: health fail streak 1/2
Health monitor finished in 100.2s — FAIL
[FAIL] lk_auth_login 46674ms Message:
Health monitor finished in 100.1s — FAIL
[FAIL] lk_auth_login 46546ms Message:
Alert suppressed: health fail streak 3/2
Health monitor finished in 99.8s — FAIL
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 18506ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 4/1
Health monitor finished in 129.9s — FAIL
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 19613ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Health monitor finished in 160.8s — FAIL
[FAIL] lk_company_badge 45083ms Message:
Alert suppressed: health fail streak 2/2
Health monitor finished in 62.8s — FAIL
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 19841ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Health monitor finished in 133.8s — FAIL
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 22351ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 2/1
Health monitor finished in 135.6s — FAIL
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 264.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 287.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 263.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 265.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 266.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 523.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 255.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 254.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 260.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 252.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 281.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 248.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 255.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 250.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 279.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 261.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 258.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 258.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 253.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 256.1s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 11.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.5s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.4s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

