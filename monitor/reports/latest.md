# BID monitor digest

- Generated: `2026-09-14T08:50:03.863341+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `d97bcc8 chore(monitor): digest report 2026-09-06 14:21 UTC+03:00`

## Influx volume

- `bid_failure`: 27 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-14 03:55:45.734180+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
- `2026-09-14 01:30:08.495860+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | tests/lk/test_lk_auth.py::test_company_in_service_provider: selenium.common.exceptions.TimeoutException: Message
- `2026-09-14 01:30:08.495860+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | tests/lk/test_lk_auth.py::test_fio_in_service_provider: selenium.common.exceptions.TimeoutException: Message
- `2026-09-14 05:25:41.666959+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-14 03:25:01.881795+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-14 01:30:08.495860+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-13 23:25:17.670424+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-13 21:24:54.684763+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-13 19:25:13.471619+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-14 05:25:41.666959+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-14 03:25:01.881795+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-14 01:30:08.495860+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-13 23:25:17.670424+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-13 21:24:54.684763+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-13 19:25:13.471619+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)

## health.log (FAIL/ERROR/WARN/ImportError)

```
Alert suppressed: health fail streak 10/2
Health monitor finished in 123.5s — FAIL
[FAIL] lk_auth_login 58156ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 11/2
Health monitor finished in 124.0s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
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
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 293.54s (0:04:53) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 294.6s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_auth.py::test_fio_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
FAILED tests/lk/test_lk_auth.py::test_company_in_service_provider - selenium.common.exceptions.TimeoutException: Message:
=== 4 failed, 15 passed, 1 skipped, 3 warnings, 4 rerun in 601.33s (0:10:01) ===
LK pytest: 15/20 passed, failed=4, errors=0, skipped=1 in 602.3s
Failure events sent to InfluxDB (таблица Grafana)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 285.22s (0:04:45) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 286.4s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
=== 2 failed, 17 passed, 1 skipped, 3 warnings, 1 rerun in 317.28s (0:05:17) ===
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 318.6s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
```

## cron.log (daily) tail markers

```
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

