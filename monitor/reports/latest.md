# BID monitor digest

- Generated: `2026-09-15T20:50:03.880821+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `5de4b64 chore(monitor): digest report 2026-09-14 20:50 UTC+03:00`

## Influx volume

- `bid_failure`: 18 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-15 11:23:19.250366+00:00` | Боевой прогон ЛК (2 ч) | `test_auth_redirects_to_lk` | tests/lk/test_lk_auth.py::test_auth_redirects_to_lk | tests/lk/test_lk_auth.py::test_auth_redirects_to_lk: pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-15 11:23:19.250366+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | tests/lk/test_lk_auth.py::test_company_in_service_provider: pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-15 11:23:19.250366+00:00` | Боевой прогон ЛК (2 ч) | `test_company_name_in_lk` | tests/lk/test_lk_auth.py::test_company_name_in_lk | tests/lk/test_lk_auth.py::test_company_name_in_lk: pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-15 11:23:19.250366+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | tests/lk/test_lk_auth.py::test_fio_in_service_provider: pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-15 11:23:19.250366+00:00` | Боевой прогон ЛК (2 ч) | `test_service_provider_opens` | tests/lk/test_lk_auth.py::test_service_provider_opens | tests/lk/test_lk_auth.py::test_service_provider_opens: pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-15 14:00:16.130045+00:00` | Лендинг + API autotests | `test_service_provider_tags_match_landing_tabs` | tests/api/test_landing_devtools_api.py::test_service_provider_tags_match_landing_tabs | tests/api/test_landing_devtools_api.py::test_service_provider_tags_match_landing_tabs

## health.log (FAIL/ERROR/WARN/ImportError)

```
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] lk_auth_login 58177ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Health monitor finished in 125.7s — FAIL
[FAIL] lk_auth_login 59753ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 13/2
Health monitor finished in 127.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15083ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15073ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15071ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Health monitor finished in 41.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 283.20s (0:04:43) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 284.3s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
=== 2 failed, 17 passed, 1 skipped, 3 warnings, 1 rerun in 357.47s (0:05:57) ===
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 358.8s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 152.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 159.8s
    raise LkAuthError(
E   pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
______________ ERROR at setup of test_company_in_service_provider ______________
    raise LkAuthError(
E   pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_auth.py::test_auth_redirects_to_lk - pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_auth.py::test_company_name_in_lk - pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_auth.py::test_service_provider_opens - pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_auth.py::test_fio_in_service_provider - pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
ERROR tests/lk/test_lk_auth.py::test_company_in_service_provider - pages.lk_flow.LkAuthError: ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
======= 12 passed, 3 skipped, 3 warnings, 5 errors in 193.47s (0:03:13) ========
LK pytest: 12/20 passed, failed=0, errors=5, skipped=3 in 194.9s
Failure events sent to InfluxDB (таблица Grafana)
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 181.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 148.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 150.2s
```

## cron.log (daily) tail markers

```
Pytest: 39/39 passed, failed=0, errors=0 in 5.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 17.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

