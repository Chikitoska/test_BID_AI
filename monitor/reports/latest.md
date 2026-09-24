# BID monitor digest

- Generated: `2026-09-24T08:50:03.878872+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `06f4535 Merge pull request #14 from Chikitoska/feature/http-error-confirm-retry`

## Influx volume

- `bid_failure`: 10 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-23 22:02:14.424560+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-23 21:56:58.870905+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | Message:  Stacktrace: #0 0x5a32d60f986a <unknown> #1 0x5a32d63f2459 <unknown> #2 0x5a32d6445efa <unknown> #3 0x5a32d64461a1 <unknown> #4 0x5a32d64906a4 <unknown> #5 0x5a32d648d886 <unknown> #6 0x5a32d
- `2026-09-23 21:51:44.604666+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | Message:  Stacktrace: #0 0x6021e80ca86a <unknown> #1 0x6021e83c3459 <unknown> #2 0x6021e8416efa <unknown> #3 0x6021e84171a1 <unknown> #4 0x6021e84616a4 <unknown> #5 0x6021e845e886 <unknown> #6 0x6021e
- `2026-09-23 21:46:44.688080+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | Message:  Stacktrace: #0 0x58b8fe8aa86a <unknown> #1 0x58b8feba3459 <unknown> #2 0x58b8febf6efa <unknown> #3 0x58b8febf71a1 <unknown> #4 0x58b8fec416a4 <unknown> #5 0x58b8fec3e886 <unknown> #6 0x58b8f

## health.log (FAIL/ERROR/WARN/ImportError)

```
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
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 337.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 258.3s
    raise LkPageError("Не отображается текущий уровень аккредитации")
E   pages.lk_page.LkPageError: Не отображается текущий уровень аккредитации
    pytest.fail("Раздел «Аккредитация» не загрузился или нет текущего уровня")
E   Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
    pytest.fail("Раздел «Аккредитация» не загрузился или нет текущего уровня")
E   Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_current_level_displayed - pages.lk_page.LkPageError: Не отображается текущий уровень аккредитации
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - Failed: Раздел «Аккредитация» не загрузился или нет текущего уровня
ERROR tests/lk/test_lk_auth.py::test_service_provider_opens - selenium.common.exceptions.TimeoutException: Message:
ERROR tests/lk/test_lk_auth.py::test_fio_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
ERROR tests/lk/test_lk_auth.py::test_company_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
= 3 failed, 13 passed, 1 skipped, 3 warnings, 3 errors, 6 rerun in 897.13s (0:14:57) =
LK pytest: 13/20 passed, failed=3, errors=3, skipped=1 in 898.4s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 265.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 261.9s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 256.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 255.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 261.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 262.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 249.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 249.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 250.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 254.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.3s
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.4s
Metrics sent to InfluxDB
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

