# BID monitor digest

- Generated: `2026-09-13T08:50:03.888624+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `d97bcc8 chore(monitor): digest report 2026-09-06 14:21 UTC+03:00`

## Influx volume

- `bid_failure`: 26 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-13 05:45:45.609990+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
- `2026-09-12 20:46:04.633522+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
- `2026-09-13 05:25:34.253944+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-13 03:24:47.763050+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-13 01:25:43.820443+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-12 23:25:10.019402+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-12 21:24:49.587568+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-12 19:24:49.253157+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-13 05:25:34.253944+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-13 03:24:47.763050+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-13 01:25:43.820443+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-12 23:25:10.019402+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-12 21:24:49.587568+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-12 19:24:49.253157+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)

## health.log (FAIL/ERROR/WARN/ImportError)

```
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
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 304.65s (0:05:04) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 305.7s
Failure events sent to InfluxDB (таблица Grafana)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 341.32s (0:05:41) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 342.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 282.32s (0:04:42) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 283.4s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
=== 2 failed, 17 passed, 1 skipped, 3 warnings, 1 rerun in 313.25s (0:05:13) ===
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 314.5s
Failure events sent to InfluxDB (таблица Grafana)
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 17.1s
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

