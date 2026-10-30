# BID monitor digest

- Generated: `2026-10-30T08:50:03.881616+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `754858e feat(monitor): include chatbot/mincifry in 2h pytest and drop obsolete «Написать нам» check.`

## Influx volume

- `bid_failure`: 92 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-30 03:47:44.300872+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | test_company_in_service_provider | https://processor.gazprom-neft.ru/ | TimeoutException: Processor: не видно «компания» (.User-Info) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
- `2026-10-30 01:48:05.318356+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | test_company_in_service_provider | https://processor.gazprom-neft.ru/ | TimeoutException: Processor: не видно «компания» (.User-Info) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
- `2026-10-29 23:47:32.890323+00:00` | Боевой прогон ЛК (2 ч) | `test_company_in_service_provider` | tests/lk/test_lk_auth.py::test_company_in_service_provider | test_company_in_service_provider | https://processor.gazprom-neft.ru/ | TimeoutException: Processor: не видно «компания» (.User-Info) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
- `2026-10-30 02:01:23.017648+00:00` | Лендинг + API autotests | `test_external_landing_api_methods[spa_events]` | tests/api/test_landing_devtools_api.py::test_external_landing_api_methods[spa_events] | test_external_landing_api_methods[spa_events] | unknown error
- `2026-10-30 03:47:44.300872+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | test_fio_in_service_provider | https://processor.gazprom-neft.ru/ | TimeoutException: Processor: не видно «ФИО» (.User-Name) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
- `2026-10-30 01:48:05.318356+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | test_fio_in_service_provider | https://processor.gazprom-neft.ru/ | TimeoutException: Processor: не видно «ФИО» (.User-Name) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
- `2026-10-29 23:47:32.890323+00:00` | Боевой прогон ЛК (2 ч) | `test_fio_in_service_provider` | tests/lk/test_lk_auth.py::test_fio_in_service_provider | test_fio_in_service_provider | https://processor.gazprom-neft.ru/ | TimeoutException: Processor: не видно «ФИО» (.User-Name) после 2 попыток по 45s. URL=https://processor.gazprom-neft.ru/. Message:
- `2026-10-30 05:25:45.179003+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 03:47:44.300872+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 01:48:05.318356+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 23:47:32.890323+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 21:28:23.267699+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 19:26:08.528301+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 05:25:45.179003+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 03:47:44.300872+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 01:48:05.318356+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 23:47:32.890323+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 21:28:23.267699+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 19:26:08.528301+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 05:25:45.179003+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 03:47:44.300872+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 01:48:05.318356+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 23:47:32.890323+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 21:28:23.267699+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 19:26:08.528301+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 05:25:45.179003+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 03:47:44.300872+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-30 01:48:05.318356+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 23:47:32.890323+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 21:28:23.267699+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 19:26:08.528301+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception

## health.log (FAIL/ERROR/WARN/ImportError)

```
Alert suppressed: health fail streak 26/2
Health monitor finished in 59.0s — FAIL (run_status=fail)
[FAIL] lk_chatbot_topics 21273ms ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 27/2
Health monitor finished in 58.6s — FAIL (run_status=fail)
[FAIL] lk_chatbot_nav 577ms ЛК: нет кнопки «Назад» или «Вернуться в начало»
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 28/2
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
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
= 2 failed, 6 passed, 2 skipped, 2 warnings, 4 errors, 4 rerun in 1650.52s (0:27:30) =
LK pytest: 6/14 passed, failed=2, errors=4, skipped=2 in 1651.7s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
= 2 failed, 6 passed, 2 skipped, 2 warnings, 4 errors, 4 rerun in 1661.18s (0:27:41) =
LK pytest: 6/14 passed, failed=2, errors=4, skipped=2 in 1662.2s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
= 2 failed, 6 passed, 2 skipped, 2 warnings, 4 errors, 4 rerun in 1657.93s (0:27:37) =
LK pytest: 6/14 passed, failed=2, errors=4, skipped=2 in 1659.0s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
======== 8 passed, 2 skipped, 2 warnings, 4 errors in 335.45s (0:05:35) ========
LK pytest: 8/14 passed, failed=0, errors=4, skipped=2 in 336.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 7.1s
Metrics sent to InfluxDB (run_status=autotest)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 6.4s
Metrics sent to InfluxDB (run_status=autotest)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

