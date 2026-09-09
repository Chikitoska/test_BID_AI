# BID monitor digest

- Generated: `2026-09-09T08:50:03.872752+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `d97bcc8 chore(monitor): digest report 2026-09-06 14:21 UTC+03:00`

## Influx volume

- `bid_failure`: 4 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

(ошибок bid_failure за период нет)

## health.log (FAIL/ERROR/WARN/ImportError)

```
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
[FAIL] main_page 0 16140ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 16.1s — FAIL
[FAIL] main_page 0 16144ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 16.1s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 185.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 247.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 185.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 150.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 192.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 156.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 145.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 184.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 252.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 181.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 165.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 169.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 173.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 189.6s
  (Session info: chrome=152.0.7977.64); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#staleelementreferenceexception
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
  (Session info: chrome=152.0.7977.64); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#staleelementreferenceexception
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
  (Session info: chrome=152.0.7977.64); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#staleelementreferenceexception
======= 15 passed, 1 skipped, 3 warnings, 4 errors in 147.02s (0:02:27) ========
LK pytest: 15/20 passed, failed=0, errors=4, skipped=1 in 148.4s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 149.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 183.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 171.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 212.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 179.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 148.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 168.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 189.2s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 14.9s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.5s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.9s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.5s
Metrics sent to InfluxDB
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

