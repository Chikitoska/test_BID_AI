# BID monitor digest

- Generated: `2026-09-06T14:21:04.902140+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `a8e493b Add VPS monitor digest report for scheduled Cursor agent (option B)`

## Influx volume

- `bid_failure`: 1 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 828 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-06 01:45:17.013677+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)

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
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
ImportError: cannot import name 'failures_from_checks' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
[FAIL] main_page 0 16140ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 16.1s — FAIL
[FAIL] main_page 0 16144ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 16.1s — FAIL
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
    from monitor.metrics import FailureEvent, write_failure_events, write_lk_pytest_run
ImportError: cannot import name 'FailureEvent' from 'monitor.metrics' (/opt/test_BID_AI/monitor/metrics.py)
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 176.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 185.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 151.2s
FAILED tests/lk/test_lk_auth.py::test_fio_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
FAILED tests/lk/test_lk_auth.py::test_company_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
=== 2 failed, 17 passed, 1 skipped, 3 warnings, 4 rerun in 454.77s (0:07:34) ===
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 455.9s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 147.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 146.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 195.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 190.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 146.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 146.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 145.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 147.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 148.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 151.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 149.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 184.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 152.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 153.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 149.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 151.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 145.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 174.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 151.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 155.3s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.4s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
Metrics sent to InfluxDB
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

