# BID monitor digest

- Generated: `2026-11-01T20:50:03.879061+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `ed011a7 fix(monitor): accept WAF 403 on POST /events and stop skipping live BID checks.`

## Influx volume

- `bid_failure`: 105 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `external_counter.js` | Внешний счётчик посещений | HTTPSConnectionPool(host='spa-back.gazprom-neft.ru', port=443): Read timed out. (read timeout=25)
- `2026-11-01 14:50:37.255565+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:45:39.108814+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:40:39.458444+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:35:58.951715+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:30:41.741728+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:25:38.985129+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:20:54.609537+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:15:43.337613+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:10:52.184235+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:05:59.323442+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:00:43.944798+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:55:42.859073+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:50:38.965796+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:45:48.515381+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:40:38.924154+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:35:55.391168+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:30:39.781725+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:25:37.368722+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:15:47.301874+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:10:38.029954+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:05:38.515959+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 13:00:39.596008+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 12:55:39.297777+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 12:50:34.834272+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 12:45:34.086422+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_events` | Лендинг: SPA UUID в events чат-бота | landing_chatbot_events | https://bid.gazprom-neft.ru/ | landing_chatbot: POST /events не обнаружен
- `2026-11-01 14:50:37.255565+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:45:39.108814+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:40:39.458444+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:35:58.951715+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:30:41.741728+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:25:38.985129+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:20:54.609537+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:15:43.337613+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:10:52.184235+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:05:59.323442+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:00:43.944798+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:55:42.859073+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:50:38.965796+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:45:48.515381+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:40:38.924154+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:35:55.391168+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:30:39.781725+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:25:37.368722+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:15:47.301874+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:10:38.029954+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:05:38.515959+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 13:00:39.596008+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 12:55:39.297777+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 12:50:34.834272+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 12:45:34.086422+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_events` | ЛК: SPA UUID в events чат-бота | lk_chatbot_events | https://lk.bid.gazprom-neft.ru/service-providers | lk_chatbot: POST /events не обнаружен
- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `spa_counter_js` | Скрипт веб-аналитики | HTTPSConnectionPool(host='spa-back.gazprom-neft.ru', port=443): Read timed out. (read timeout=25)
- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `test_external_landing_api_methods[spa_counter_js]` | tests/api/test_landing_devtools_api.py::test_external_landing_api_methods[spa_counter_js] | test_external_landing_api_methods[spa_counter_js] | unknown error
- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `test_external_landing_api_methods[spa_events]` | tests/api/test_landing_devtools_api.py::test_external_landing_api_methods[spa_events] | test_external_landing_api_methods[spa_events] | unknown error
- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `test_external_public_assets_return_2xx[https://spa-back.gazprom-neft.ru/static/counter.js]` | tests/api/test_public_api.py::test_external_public_assets_return_2xx[https://spa-back.gazprom-neft.ru/static/counter.js] | test_external_public_assets_return_2xx[https://spa-back.gazprom-neft.ru/static/counter.js] | unknown error
- `2026-11-01 17:23:14.799445+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 15:34:12.777828+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 13:22:57.097384+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 11:22:58.696111+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 09:25:14.476889+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 07:23:00.555020+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 17:23:14.799445+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 15:34:12.777828+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 13:22:57.097384+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 11:22:58.696111+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 09:25:14.476889+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 07:23:00.555020+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 17:23:14.799445+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 15:34:12.777828+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 13:22:57.097384+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 11:22:58.696111+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 09:25:14.476889+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 07:23:00.555020+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 17:23:14.799445+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 15:34:12.777828+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 13:22:57.097384+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 11:22:58.696111+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 09:25:14.476889+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 07:23:00.555020+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `test_no_5xx_on_public_endpoints` | tests/api/test_public_api.py::test_no_5xx_on_public_endpoints | test_no_5xx_on_public_endpoints | reques...
- `2026-11-01 14:03:56.836183+00:00` | Лендинг + сервисы (2×/день) | `test_spa_events_get_returns_405_not_5xx` | tests/api/test_landing_devtools_api.py::test_spa_events_get_returns_405_not_5xx | test_spa_events_get_returns_405_not_5xx | unknown error

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
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 173.12s (0:02:53) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 174.4s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 171.70s (0:02:51) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 172.8s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
======== 10 passed, 2 warnings, 4 errors, 1 rerun in 847.47s (0:14:07) =========
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 848.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
============= 10 passed, 2 warnings, 4 errors in 189.22s (0:03:09) =============
LK pytest: 10/14 passed, failed=0, errors=4, skipped=0 in 190.5s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
```

## cron.log (daily) tail markers

```
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

