# BID monitor digest

- Generated: `2026-09-18T08:50:03.865466+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `b125238 Merge pull request #11 from Chikitoska/harden-lk-processor-antiflap`

## Influx volume

- `bid_failure`: 2 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-18 01:27:51.282530+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | tests/lk/test_lk_auth.py::test_company_in_service_provider: selenium.common.exceptions.TimeoutException: Message
- `2026-09-18 01:27:51.282530+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | tests/lk/test_lk_auth.py::test_fio_in_service_provider: selenium.common.exceptions.TimeoutException: Message

## health.log (FAIL/ERROR/WARN/ImportError)

```
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
[FAIL] main_page 0 15078ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
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
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 147.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 149.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 164.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 152.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 166.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 149.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 149.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 148.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 149.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 145.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 180.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 163.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 146.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 171.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 190.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 186.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 191.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 154.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 149.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 185.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 189.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 147.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 180.3s
FAILED tests/lk/test_lk_auth.py::test_fio_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
FAILED tests/lk/test_lk_auth.py::test_company_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
=== 2 failed, 15 passed, 3 skipped, 3 warnings, 4 rerun in 465.85s (0:07:45) ===
LK pytest: 15/20 passed, failed=2, errors=0, skipped=3 in 467.0s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 147.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 189.0s
```

## cron.log (daily) tail markers

```
Pytest: 39/39 passed, failed=0, errors=0 in 10.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.3s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

