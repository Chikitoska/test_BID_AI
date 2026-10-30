# BID monitor digest

- Generated: `2026-10-30T20:50:03.867490+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `ed011a7 fix(monitor): accept WAF 403 on POST /events and stop skipping live BID checks.`

## Influx volume

- `bid_failure`: 57 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-30 12:46:03.611833+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_icon` | Лендинг: иконка чат-бота | landing_chatbot_icon | https://bid.gazprom-neft.ru/ | Лендинг: иконка чат-бота не отображается
- `2026-10-30 08:51:57.058584+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://id.bid.gazprom-neft.ru/realms/ecoportal/login-actions/authenticate?execution=3ae89bde-8c38-42b7-a53b-feea88b3fe6d&client_id=self-authentication&tab_id=nbNiueQf0OE&cl | Нет поля OTP за 45 с (URL: https://id.bid.gazprom-neft.ru/realms/ecoportal/login-actions/authenticate?execution=3ae89bde-8c38-42b7-a53b-feea88b3fe6d&client_id=self-authentication&tab_id=nbNiueQf0OE&cl
- `2026-10-30 17:22:56.937455+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 15:23:34.208792+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 13:23:03.229920+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 11:23:22.511876+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 09:23:31.038320+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 07:25:31.284385+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 17:22:56.937455+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 15:23:34.208792+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 13:23:03.229920+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 11:23:22.511876+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 09:23:31.038320+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 07:25:31.284385+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 17:22:56.937455+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 15:23:34.208792+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 13:23:03.229920+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 11:23:22.511876+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 09:23:31.038320+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 07:25:31.284385+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 17:22:56.937455+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 15:23:34.208792+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 13:23:03.229920+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 11:23:22.511876+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 09:23:31.038320+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 07:25:31.284385+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception

## health.log (FAIL/ERROR/WARN/ImportError)

```
Health monitor finished in 41.7s — FAIL (run_status=fail)
[FAIL] lk_chatbot_topics 20728ms ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 29/2
Health monitor finished in 64.8s — FAIL (run_status=fail)
[FAIL] lk_chatbot_topics 20387ms ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 30/2
Health monitor finished in 57.8s — FAIL (run_status=fail)
[FAIL] lk_chatbot_topics 20895ms ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 31/2
Health monitor finished in 57.1s — FAIL (run_status=fail)
[FAIL] lk_chatbot_topics 21104ms ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 32/2
Health monitor finished in 57.4s — FAIL (run_status=fail)
[FAIL] lk_chatbot_topics 20879ms ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 33/2
Health monitor finished in 70.8s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 46957ms Нет поля OTP за 45 с (URL: https://id.bid.gazprom-neft.ru/realms/ecoportal/login-actions/authenticate?execution=3ae89bde-8c38-42b7-a53b-feea88b3fe6d&client_id=self-authentication&tab_id=nbNiueQf0OE&cl
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 111.2s — FAIL (run_status=fail)
[FAIL] landing_chatbot_icon 20131ms Лендинг: иконка чат-бота не отображается
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 59.0s — FAIL (run_status=fail)
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 191.74s (0:03:11) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 192.8s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 178.58s (0:02:58) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 179.7s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 190.00s (0:03:09) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 191.1s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 171.53s (0:02:51) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 172.7s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
```

## cron.log (daily) tail markers

```
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

