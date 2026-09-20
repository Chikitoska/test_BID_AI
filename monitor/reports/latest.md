# BID monitor digest

- Generated: `2026-09-20T08:50:03.185582+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `62cc5ed Merge pull request #12 from Chikitoska/fix/lk-pytest-alert-classifier`

## Influx volume

- `bid_failure`: 1 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-20 00:07:17.656268+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500

## health.log (FAIL/ERROR/WARN/ImportError)

```
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15078ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15076ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Alert suppressed: health fail streak 19/2
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15075ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Alert suppressed: health fail streak 20/2
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] lk_auth_login 58081ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 1/2
Health monitor finished in 123.1s — FAIL
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
=================================== FAILURES ===================================
    pytest.fail("Раздел «Аккредитация» не загрузился или нет текущего уровня")
E   Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
======= 1 failed, 17 passed, 2 skipped, 3 warnings in 320.12s (0:05:20) ========
LK pytest: 17/20 passed, failed=1, errors=0, skipped=2 in 321.3s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 358.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 258.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 258.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 259.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 259.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 281.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 290.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 273.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 303.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.2s
```

## cron.log (daily) tail markers

```
Pytest: 38/39 passed, failed=1, errors=0 in 7.8s
Metrics sent to InfluxDB
Alert suppressed: daily fail already reported (anti-flap)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 6.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 8.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 6.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.5s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.3s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.4s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.2s
Metrics sent to InfluxDB
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

