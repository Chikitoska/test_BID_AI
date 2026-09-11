# BID monitor digest

- Generated: `2026-09-11T20:50:00.677482+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `d97bcc8 chore(monitor): digest report 2026-09-06 14:21 UTC+03:00`

## Influx volume

- `bid_failure`: 32 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_auth_redirects_to_lk` | tests/lk/test_lk_auth.py::test_auth_redirects_to_lk | tests/lk/test_lk_auth.py::test_auth_redirects_to_lk: selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | tests/lk/test_lk_auth.py::test_company_in_service_provider: selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_company_name_in_lk` | tests/lk/test_lk_auth.py::test_company_name_in_lk | tests/lk/test_lk_auth.py::test_company_name_in_lk: selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | tests/lk/test_lk_auth.py::test_fio_in_service_provider: selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
- `2026-09-11 17:25:34.753898+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 15:25:41.481949+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 13:24:50.940925+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 11:24:53.288852+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 07:25:09.644960+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 17:25:34.753898+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 15:25:41.481949+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 13:24:50.940925+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 11:24:53.288852+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 07:25:09.644960+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 09:25:09.916987+00:00` | Боевой прогон ЛК (2 ч) | `test_service_provider_opens` | tests/lk/test_lk_auth.py::test_service_provider_opens | tests/lk/test_lk_auth.py::test_service_provider_opens: selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found

## health.log (FAIL/ERROR/WARN/ImportError)

```
Health monitor finished in 126.0s — FAIL
[FAIL] lk_auth_login 58635ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 5/2
Health monitor finished in 125.1s — FAIL
[FAIL] lk_auth_login 64664ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 6/2
Health monitor finished in 129.8s — FAIL
[FAIL] lk_auth_login 58795ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 7/2
Health monitor finished in 125.8s — FAIL
[FAIL] lk_auth_login 58396ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 8/2
Health monitor finished in 123.6s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[FAIL] lk_auth_login 59758ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Health monitor finished in 127.0s — FAIL
[FAIL] lk_auth_login 58388ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 10/2
Health monitor finished in 123.5s — FAIL
[FAIL] lk_auth_login 58156ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 11/2
Health monitor finished in 124.0s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 290.60s (0:04:50) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 292.0s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 285.59s (0:04:45) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 286.7s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
=== 2 failed, 17 passed, 1 skipped, 3 warnings, 1 rerun in 338.46s (0:05:38) ===
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 339.7s
Failure events sent to InfluxDB (таблица Grafana)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
=== 2 failed, 17 passed, 1 skipped, 3 warnings, 1 rerun in 329.20s (0:05:29) ===
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 330.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 5.7s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 5.6s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

