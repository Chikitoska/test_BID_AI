# BID monitor digest

- Generated: `2026-10-28T20:50:22.684703+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_failure`: 13 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1148 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-28 10:51:35.201703+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/error/500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-10-28 17:24:44.590390+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-28 15:24:28.245119+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-28 13:24:22.719646+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-28 11:25:07.651996+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-28 09:24:26.207247+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-28 07:24:55.642310+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна

## health.log (FAIL/ERROR/WARN/ImportError)

```
Health monitor finished in 116.1s — FAIL_AUTOTEST (run_status=autotest)
[FAIL] lk_auth_login 46872ms Message:
Alert suppressed: health failure classified as autotest (UI flake / Chrome/WebDriver) — Grafana orange; not paging as LK/PROD down
Health monitor finished in 100.6s — FAIL_AUTOTEST (run_status=autotest)
[FAIL] lk_auth_login 46956ms Message:
Alert suppressed: health failure classified as autotest (UI flake / Chrome/WebDriver) — Grafana orange; not paging as LK/PROD down
Health monitor finished in 101.8s — FAIL_AUTOTEST (run_status=autotest)
[FAIL] lk_auth_login 46802ms Message:
Alert suppressed: health failure classified as autotest (UI flake / Chrome/WebDriver) — Grafana orange; not paging as LK/PROD down
Health monitor finished in 100.4s — FAIL_AUTOTEST (run_status=autotest)
[FAIL] lk_auth_login 46882ms Message:
Alert suppressed: health failure classified as autotest (UI flake / Chrome/WebDriver) — Grafana orange; not paging as LK/PROD down
Health monitor finished in 100.8s — FAIL_AUTOTEST (run_status=autotest)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 15296ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 128.3s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 58721ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/service-providers
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 170.2s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 17224ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 127.3s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 24736ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 93.5s — FAIL (run_status=fail)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
E   AssertionError: Кнопка «Написать нам» не видна или недоступна
FAILED tests/lk/test_lk_smoke.py::test_lk_header_action_buttons - AssertionError: Кнопка «Написать нам» не видна или недоступна
======= 1 failed, 16 passed, 3 skipped, 3 warnings in 283.47s (0:04:43) ========
LK pytest: 16/20 passed, failed=1, errors=0, skipped=3 in 284.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
tests/lk/test_lk_smoke.py::test_lk_header_action_buttons FAILED
=================================== FAILURES ===================================
E   AssertionError: Кнопка «Написать нам» не видна или недоступна
FAILED tests/lk/test_lk_smoke.py::test_lk_header_action_buttons - AssertionError: Кнопка «Написать нам» не видна или недоступна
======= 1 failed, 16 passed, 3 skipped, 3 warnings in 260.00s (0:04:20) ========
LK pytest: 16/20 passed, failed=1, errors=0, skipped=3 in 261.2s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
tests/lk/test_lk_smoke.py::test_lk_header_action_buttons FAILED
=================================== FAILURES ===================================
E   AssertionError: Кнопка «Написать нам» не видна или недоступна
FAILED tests/lk/test_lk_smoke.py::test_lk_header_action_buttons - AssertionError: Кнопка «Написать нам» не видна или недоступна
======= 1 failed, 16 passed, 3 skipped, 3 warnings in 262.07s (0:04:22) ========
LK pytest: 16/20 passed, failed=1, errors=0, skipped=3 in 263.1s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
tests/lk/test_lk_smoke.py::test_lk_header_action_buttons FAILED
=================================== FAILURES ===================================
E   AssertionError: Кнопка «Написать нам» не видна или недоступна
FAILED tests/lk/test_lk_smoke.py::test_lk_header_action_buttons - AssertionError: Кнопка «Написать нам» не видна или недоступна
======= 1 failed, 16 passed, 3 skipped, 3 warnings in 260.38s (0:04:20) ========
LK pytest: 16/20 passed, failed=1, errors=0, skipped=3 in 261.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.6s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 9.5s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 12.0s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.2s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.9s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.1s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.1s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

