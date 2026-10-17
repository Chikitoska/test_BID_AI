# BID monitor digest

- Generated: `2026-10-17T20:50:22.676522+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_failure`: 1 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1148 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-17 07:01:47.886554+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/service-providers | Message: stale element reference: stale element not found (Session info: chrome=155.0.8059.39); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubl

## health.log (FAIL/ERROR/WARN/ImportError)

```
[FAIL] lk_auth_login 14556ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 7/1
Health monitor finished in 122.7s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 14736ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 8/1
Health monitor finished in 123.3s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 14045ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 122.5s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 16584ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 2/1
Health monitor finished in 125.4s — FAIL (run_status=fail)
[FAIL] lk_auth_login 16819ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 78.9s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
  (Session info: chrome=155.0.8059.39); For documentation on this error, please visit: https://www.sel. Повтор через 3 с…
[FAIL] lk_auth_login 49999ms Message: stale element reference: stale element not found
  (Session info: chrome=155.0.8059.39); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubl
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 105.5s — FAIL (run_status=fail)
  (Session info: chrome=155.0.8059.39); For documentation on this error, please visit: https://www.sel. Повтор через 3 с…
  (Session info: chrome=155.0.8059.79); For documentation on this error, please visit: https://www.sel. Повтор через 3 с…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 16/20 passed, failed=2, errors=1, skipped=1 in 531.9s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 270.4s
FAILED tests/lk/test_lk_auth.py::test_fio_in_service_provider - selenium.common.exceptions.TimeoutException: Message: Processor: не видно «ФИО» (.User-Name) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
== 1 failed, 16 passed, 3 skipped, 3 warnings, 2 rerun in 1029.98s (0:17:09) ===
LK pytest: 16/20 passed, failed=1, errors=0, skipped=3 in 1031.0s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 258.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 259.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 522.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 248.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 275.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 277.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.8s
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.5s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

