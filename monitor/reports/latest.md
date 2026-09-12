# BID monitor digest

- Generated: `2026-09-12T08:50:03.880095+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `d97bcc8 chore(monitor): digest report 2026-09-06 14:21 UTC+03:00`

## Influx volume

- `bid_failure`: 31 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 864 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-11 18:52:11.873912+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-11 18:47:29.009544+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-09-12 05:24:49.269505+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-12 03:24:44.514780+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-12 01:24:49.206976+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 23:25:02.627145+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 21:24:48.729595+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-11 19:24:50.415480+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_apply_button_without_submit` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit | tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit: AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
- `2026-09-12 05:24:49.269505+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-12 03:24:44.514780+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-12 01:24:49.206976+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 23:25:02.627145+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 21:24:48.729595+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
- `2026-09-11 19:24:50.415480+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_level_selection_visible` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible | tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible: AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)

## health.log (FAIL/ERROR/WARN/ImportError)

```
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
[FAIL] lk_auth_login 58177ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Health monitor finished in 125.7s — FAIL
[FAIL] lk_auth_login 59753ms ЛК не загрузился после входа (нет бейджа пользователя), URL: https://lk.bid.gazprom-neft.ru/error/500
Alert suppressed: health fail streak 13/2
Health monitor finished in 127.2s — FAIL
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 297.15s (0:04:57) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 298.3s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 283.68s (0:04:43) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 284.9s
Failure events sent to InfluxDB (таблица Grafana)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 281.67s (0:04:41) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 282.9s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: daily fail already reported (anti-flap)
ssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
E   AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_level_selection_visible - AssertionError: Не отображается UI выбора уровня аккредитации (карточки «ДОСТУПНО» или опросник «Выбрать уровень»)
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_apply_button_without_submit - AssertionError: Не отображается элемент начала выбора уровня («Заполнить анкету», «Выбрать уровень» или «Далее»)
======= 2 failed, 17 passed, 1 skipped, 3 warnings in 283.85s (0:04:43) ========
LK pytest: 17/20 passed, failed=2, errors=0, skipped=1 in 284.9s
Failure events sent to InfluxDB (таблица Grafana)
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

