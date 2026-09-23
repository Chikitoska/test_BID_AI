# BID monitor digest

- Generated: `2026-09-23T08:50:03.883962+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `06f4535 Merge pull request #14 from Chikitoska/feature/http-error-confirm-retry`

## Influx volume

- `bid_failure`: 19 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

(ошибок bid_failure за период нет)

## health.log (FAIL/ERROR/WARN/ImportError)

```
[FAIL] main_page 0 20020ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))
Alert suppressed: health fail streak 8/2
Health monitor finished in 50.0s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 20023ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))
Alert suppressed: health fail streak 9/2
Health monitor finished in 50.0s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 20019ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))
Alert suppressed: health fail streak 10/2
Health monitor finished in 50.0s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 20008ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='bid.gazprom-neft.ru', port=443): Failed to resolve 'bid.gazprom-neft.ru' ([Errno -3] Temporary failure in name resolution)"))
Alert suppressed: health fail streak 11/2
Health monitor finished in 50.0s — FAIL
main_page FAIL (HTTP 503: Service Unavailable), повтор через 10 с (ещё 1 раз)…
[FAIL] lk_auth_login 46765ms Message:
Alert suppressed: health fail streak 1/2
Health monitor finished in 111.0s — FAIL
[FAIL] lk_auth_login 17942ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Health monitor finished in 72.0s — FAIL
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 21551ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 3/1
Health monitor finished in 135.9s — FAIL
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 19920ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 4/1
Health monitor finished in 136.5s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 270.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 262.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 525.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 257.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.0s
    raise HttpStatusError(
E   pages.lk_flow.HttpStatusError: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
_____ ERROR at setup of test_lk_accreditation_apply_button_without_submit ______
    raise last_error
    raise HttpStatusError(
E   pages.lk_flow.HttpStatusError: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_navigation - pages.lk_flow.HttpStatusError: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_current_level_displayed - pages.lk_flow.HttpStatusError: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - pages.lk_flow.HttpStatusError: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - pages.lk_flow.HttpStatusError: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
== 15 passed, 1 skipped, 3 warnings, 4 errors, 9 rerun in 1242.30s (0:20:42) ===
LK pytest: 15/20 passed, failed=0, errors=4, skipped=1 in 1244.2s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 337.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 258.3s
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 11.2s
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

