# BID monitor digest

- Generated: `2026-10-19T20:50:07.897220+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_failure`: 9 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-19 12:12:04.856424+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/service-providers | Message: timeout: Timed out receiving message from renderer: -0.001 (Session info: chrome=155.0.8059.79)
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | test_company_in_service_provider | TimeoutException: element not found / wait timed out
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_company_name_in_lk` | tests/lk/test_lk_auth.py::test_company_name_in_lk | test_company_name_in_lk | TimeoutException: element not found / wait timed out
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | test_fio_in_service_provider | TimeoutException: element not found / wait timed out
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_current_level_displayed` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_current_level_displayed | test_lk_accreditation_current_level_displayed | TimeoutException: element not found / wait timed out
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | test_lk_accreditation_level_selection_visible | Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_processor_card_on_vitrina` | tests/lk/test_lk_smoke.py::test_lk_processor_card_on_vitrina | test_lk_processor_card_on_vitrina | AssertionError: На витрине нет карточки Processor
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_user_badge_has_profile_data` | tests/lk/test_lk_smoke.py::test_lk_user_badge_has_profile_data | test_lk_user_badge_has_profile_data | TimeoutException: element not found / wait timed out
- `2026-10-19 11:45:26.275904+00:00` | Боевой прогон ЛК (2 ч) | `test_service_provider_opens` | tests/lk/test_lk_auth.py::test_service_provider_opens | test_service_provider_opens | TimeoutException: element not found / wait timed out

## health.log (FAIL/ERROR/WARN/ImportError)

```
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
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 54232ms Message: timeout: Timed out receiving message from renderer: -0.001
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 120.4s — FAIL (run_status=fail)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 775.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 278.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 776.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 270.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 262.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 269.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.3s
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_current_level_displayed - selenium.common.exceptions.TimeoutException: Message:
ERROR tests/lk/test_lk_auth.py::test_service_provider_opens - selenium.common.exceptions.TimeoutException: Message:
ERROR tests/lk/test_lk_auth.py::test_fio_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
ERROR tests/lk/test_lk_auth.py::test_company_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
= 4 failed, 10 passed, 2 skipped, 3 warnings, 4 errors, 12 rerun in 1512.27s (0:25:12) =
LK pytest: 10/20 passed, failed=4, errors=4, skipped=2 in 1513.4s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 259.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 253.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 332.8s
```

## cron.log (daily) tail markers

```
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

