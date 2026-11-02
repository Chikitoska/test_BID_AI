# BID monitor digest

- Generated: `2026-11-02T08:50:03.866046+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `82a09f8 fix(monitor): stop combat Chrome mismatch and health /events sniffer misses.`

## Influx volume

- `bid_failure`: 103 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-11-02 03:22:57.295608+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 01:22:58.203219+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 23:25:05.612162+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 21:25:08.047450+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 19:27:50.938339+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 05:23:55.000803+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | ChatbotError: Лендинг: иконка чат-бота не отображается
- `2026-11-02 03:22:57.295608+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 01:22:58.203219+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 23:25:05.612162+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 21:25:08.047450+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 19:27:50.938339+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 03:22:57.295608+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 01:22:58.203219+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 23:25:05.612162+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 21:25:08.047450+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 19:27:50.938339+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 05:23:55.000803+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | MincifryError: На лендинге не отображается блок «Установите российские сертификаты, чтобы не терять доступ к сервисам»
- `2026-11-02 03:22:57.295608+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-02 01:22:58.203219+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 23:25:05.612162+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 21:25:08.047450+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 19:27:50.938339+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception

## health.log (FAIL/ERROR/WARN/ImportError)

```
[FAIL] landing_chatbot_events 2998ms landing_chatbot: POST /events не обнаружен
[FAIL] lk_chatbot_events 2504ms lk_chatbot: POST /events не обнаружен
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 20/2
Health monitor finished in 34.5s — FAIL (run_status=fail)
[FAIL] landing_chatbot_events 2996ms landing_chatbot: POST /events не обнаружен
[FAIL] lk_chatbot_events 2504ms lk_chatbot: POST /events не обнаружен
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 21/2
Health monitor finished in 37.2s — FAIL (run_status=fail)
[FAIL] landing_chatbot_events 2985ms landing_chatbot: POST /events не обнаружен
[FAIL] lk_chatbot_events 2505ms lk_chatbot: POST /events не обнаружен
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 22/2
Health monitor finished in 35.7s — FAIL (run_status=fail)
[FAIL] landing_chatbot_events 3007ms landing_chatbot: POST /events не обнаружен
[FAIL] lk_chatbot_events 2503ms lk_chatbot: POST /events не обнаружен
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 23/2
Health monitor finished in 34.9s — FAIL (run_status=fail)
[FAIL] landing_chatbot_events 3003ms landing_chatbot: POST /events не обнаружен
[FAIL] lk_chatbot_events 2503ms lk_chatbot: POST /events не обнаружен
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 24/2
Health monitor finished in 34.6s — FAIL (run_status=fail)
[FAIL] landing_chatbot_events 2993ms landing_chatbot: POST /events не обнаружен
[FAIL] lk_chatbot_events 2507ms lk_chatbot: POST /events не обнаружен
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 25/2
Health monitor finished in 32.8s — FAIL (run_status=fail)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 304.6s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 172.80s (0:02:52) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 173.9s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 172.03s (0:02:52) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 173.1s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration FAILED
tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration FAILED
=================================== FAILURES ===================================
    raise ChatbotError(f"{context}: иконка чат-бота не отображается")
E   pages.chatbot_widget.ChatbotError: Лендинг: иконка чат-бота не отображается
    raise MincifryError(
E   pages.mincifry_page.MincifryError: На лендинге не отображается блок «Установите российские сертификаты, чтобы не терять доступ к сервисам»
FAILED tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration - pages.chatbot_widget.ChatbotError: Лендинг: иконка чат-бота не отображается
FAILED tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - pages.mincifry_page.MincifryError: На лендинге не отображается блок «Установите российские сертификаты, чтобы не терять доступ к сервисам»
============= 2 failed, 12 passed, 2 warnings in 229.45s (0:03:49) =============
LK pytest: 12/14 passed, failed=2, errors=0, skipped=0 in 230.7s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
```

## cron.log (daily) tail markers

```
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 7.1s
Metrics sent to InfluxDB (run_status=autotest)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 6.4s
Metrics sent to InfluxDB (run_status=autotest)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.1s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
[FAIL] spa_counter_js 0 26210ms HTTPSConnectionPool(host='spa-back.gazprom-neft.ru', port=443): Read timed out. (read timeout=25)
[FAIL] external_counter.js 0 25137ms HTTPSConnectionPool(host='spa-back.gazprom-neft.ru', port=443): Read timed out. (read timeout=25)
Pytest: 34/39 passed, failed=5, errors=0 in 162.7s
Metrics sent to InfluxDB (run_status=fail)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.1s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

