# BID monitor digest

- Generated: `2026-10-29T20:50:01.376443+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `754858e feat(monitor): include chatbot/mincifry in 2h pytest and drop obsolete «Написать нам» check.`

## Influx volume

- `bid_failure`: 67 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-10-29 08:50:34.578133+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_close` | Лендинг: закрытие окна чат-бота | landing_chatbot_close | https://bid.gazprom-neft.ru/ | Лендинг: после закрытия окно чат-бота всё ещё открыто (темы на экране)
- `2026-10-29 08:45:16.925350+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_close` | Лендинг: закрытие окна чат-бота | landing_chatbot_close | https://bid.gazprom-neft.ru/ | Лендинг: после закрытия окно чат-бота всё ещё открыто (темы на экране)
- `2026-10-29 08:38:48.505889+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_close` | Лендинг: закрытие окна чат-бота | landing_chatbot_close | https://bid.gazprom-neft.ru/ | Лендинг: после закрытия окно чат-бота всё ещё открыто (темы на экране)
- `2026-10-29 10:23:35.808869+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_topics` | Лендинг: темы чат-бота | landing_chatbot_topics | https://bid.gazprom-neft.ru/ | Лендинг: после открытия чата темы не отображаются. Текст: 'Войти\nПолучить ID\nПолучить ID\nАссистент\nНеизвестная ошибка\n\nСейчас ассистент недоступен — попробуйте вернуться позже или обратитесь в п
- `2026-10-29 10:17:16.226460+00:00` | Лендинг + мин ЛК (5 мин) | `landing_chatbot_topics` | Лендинг: темы чат-бота | landing_chatbot_topics | https://bid.gazprom-neft.ru/ | Лендинг: после открытия чата темы не отображаются. Текст: 'Войти\nПолучить ID\nПолучить ID\nАссистент\nНеизвестная ошибка\n\nСейчас ассистент недоступен — попробуйте вернуться позже или обратитесь в п
- `2026-10-29 09:01:23.442713+00:00` | mincifry | `landing_mincifry_click` | Минцифр: блок кликабелен, открылась страница | landing_mincifry_click | https://bid.gazprom-neft.ru/ | Блок Минцифр на лендинге некликабелен
- `2026-10-29 08:55:37.273565+00:00` | mincifry | `landing_mincifry_yandex` | Минцифр: установка Яндекс Браузера | landing_mincifry_yandex | https://lk.bid.gazprom-neft.ru/registration | На странице нет указания по установке Яндекс Браузера: url='https://lk.bid.gazprom-neft.ru/registration' текст='регистрация шаг 1 из 4 резидент нерезидент инн далее о компании о вас пароль подтвержден
- `2026-10-29 08:52:17.470743+00:00` | mincifry | `landing_mincifry_yandex` | Минцифр: установка Яндекс Браузера | landing_mincifry_yandex | https://id.bid.gazprom-neft.ru/realms/ecoportal/protocol/openid-connect/auth?client_id=self-authentication&redirect_uri=https%3A%2F%2Flk.bid | На странице нет указания по установке Яндекс Браузера: url='https://id.bid.gazprom-neft.ru/realms/ecoportal/protocol/openid-connect/auth?client_id=self-authentication&redirect_uri=https%3A%2F%2Flk.bid
- `2026-10-29 08:39:18.710856+00:00` | mincifry | `landing_mincifry_yandex` | Минцифр: установка Яндекс Браузера | landing_mincifry_yandex | https://id.bid.gazprom-neft.ru/realms/ecoportal/protocol/openid-connect/auth?client_id=self-authentication&redirect_uri=https%3A%2F%2Flk.bid.gazprom-neft.ru&response_type=code | На странице нет указания по установке Яндекс Браузера
- `2026-10-29 10:17:16.226460+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/error/500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-10-29 08:50:34.578133+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://sts.gazprom-neft.ru/adfs/oauth2/authorize/?scope=openid+profile+email&state=5NyEN6ZbzK3mCN87FUNW5oG2D-4ts94LAEc-7pLMVNw.oBRnSpsB-c8.fsejIHxxQWaTyqd9QDSxsg.eyJydSI6Imh0dHB | Нет поля логина (URL: https://sts.gazprom-neft.ru/adfs/oauth2/authorize/?scope=openid+profile+email&state=5NyEN6ZbzK3mCN87FUNW5oG2D-4ts94LAEc-7pLMVNw.oBRnSpsB-c8.fsejIHxxQWaTyqd9QDSxsg.eyJydSI6Imh0dHB
- `2026-10-29 08:45:16.925350+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://sts.gazprom-neft.ru/adfs/oauth2/authorize/?scope=openid+profile+email&state=gS9ts86vckx8Pc6VbE_m4eIz8lMwYdhOA624O49zbBQ.sDwRkPnYmYY.fsejIHxxQWaTyqd9QDSxsg.eyJydSI6Imh0dHB | Нет поля логина (URL: https://sts.gazprom-neft.ru/adfs/oauth2/authorize/?scope=openid+profile+email&state=gS9ts86vckx8Pc6VbE_m4eIz8lMwYdhOA624O49zbBQ.sDwRkPnYmYY.fsejIHxxQWaTyqd9QDSxsg.eyJydSI6Imh0dHB
- `2026-10-29 08:38:48.505889+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://sts.gazprom-neft.ru/adfs/oauth2/authorize/?scope=openid+profile+email&state=FAEZ47MS5n_RT2tgRZcgIepySVavk73mhs8_CtBA1sc.7bg_nzNT3Gg.fsejIHxxQWaTyqd9QDSxsg.eyJydSI6Imh0dHB | Нет поля логина (URL: https://sts.gazprom-neft.ru/adfs/oauth2/authorize/?scope=openid+profile+email&state=FAEZ47MS5n_RT2tgRZcgIepySVavk73mhs8_CtBA1sc.7bg_nzNT3Gg.fsejIHxxQWaTyqd9QDSxsg.eyJydSI6Imh0dHB
- `2026-10-29 06:07:12.547151+00:00` | Лендинг + мин ЛК (5 мин) | `lk_auth_login` | ЛК: вход (логин + 2FA) | lk_auth_login | https://lk.bid.gazprom-neft.ru/error/500 | ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
- `2026-10-29 10:55:46.229182+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 10:30:57.822395+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 09:51:08.011805+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 09:45:46.624552+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 09:35:50.811900+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 09:15:47.648787+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 08:56:30.999912+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_nav` | ЛК: Назад / в начало чат-бота | lk_chatbot_nav | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: нет кнопки «Назад» или «Вернуться в начало»
- `2026-10-29 11:26:11.561727+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 11:15:58.219826+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 11:11:01.762801+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 11:06:02.349568+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 11:01:28.094712+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:51:03.166730+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:46:03.545402+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:41:03.405117+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:36:01.114719+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:26:01.836132+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:23:35.808869+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:11:03.392541+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:06:02.948286+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 10:01:01.184603+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:56:02.310113+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:41:02.802671+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:31:04.416100+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:25:57.644143+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:11:00.427352+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:05:59.629857+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 09:00:59.053578+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 08:51:33.416196+00:00` | Лендинг + мин ЛК (5 мин) | `lk_chatbot_topics` | ЛК: темы чат-бота | lk_chatbot_topics | https://lk.bid.gazprom-neft.ru/service-providers | ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документ
- `2026-10-29 14:01:21.182025+00:00` | Лендинг + API autotests | `test_external_landing_api_methods[spa_events]` | tests/api/test_landing_devtools_api.py::test_external_landing_api_methods[spa_events] | test_external_landing_api_methods[spa_events] | unknown error
- `2026-10-29 17:23:30.254862+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 15:26:04.331711+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 13:24:11.489513+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_full_flow` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow | test_landing_chatbot_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 17:23:30.254862+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 15:26:04.331711+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 13:24:11.489513+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_chatbot_skips_login_and_registration` | tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_skips_login_and_registration | test_landing_chatbot_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 17:23:30.254862+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 15:26:04.331711+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 13:24:11.489513+00:00` | Боевой прогон ЛК (2 ч) | `test_landing_mincifry_full_flow` | tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow | test_landing_mincifry_full_flow | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 11:25:05.535838+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_chatbot_full_flow` | tests/lk/test_lk_chatbot.py::test_lk_chatbot_full_flow | test_lk_chatbot_full_flow | ChatbotError: ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документы в профиль пользователя, чтобы подтвердить роль\nДобавить документы\nВсе\nОтраслевые сервисы\nПоддержка б'
- `2026-10-29 09:24:52.024562+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_chatbot_full_flow` | tests/lk/test_lk_chatbot.py::test_lk_chatbot_full_flow | test_lk_chatbot_full_flow | ChatbotError: ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документы в профиль пользователя, чтобы подтвердить роль\nДобавить документы\nВсе\nОтраслевые сервисы\nПоддержка б'
- `2026-10-29 11:25:05.535838+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-29 09:24:52.024562+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-29 07:24:30.313625+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_header_action_buttons` | tests/lk/test_lk_smoke.py::test_lk_header_action_buttons | test_lk_header_action_buttons | AssertionError: Кнопка «Написать нам» не видна или недоступна
- `2026-10-29 17:23:30.254862+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 15:26:04.331711+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
- `2026-10-29 13:24:11.489513+00:00` | Боевой прогон ЛК (2 ч) | `test_mincifry_card_click_skips_login_and_registration` | tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration | test_mincifry_card_click_skips_login_and_registration | SessionNotCreatedException: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception

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
    raise ChatbotError(
E   pages.chatbot_widget.ChatbotError: ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документы в профиль пользователя, чтобы подтвердить роль\nДобавить документы\nВсе\nОтраслевые сервисы\nПоддержка б'
E   AssertionError: Кнопка «Написать нам» не видна или недоступна
FAILED tests/lk/test_lk_chatbot.py::test_lk_chatbot_full_flow - pages.chatbot_widget.ChatbotError: ЛК: после открытия чата темы не отображаются. Текст: 'Витрина\nПрофиль компании\nАккредитация\nЗаявки\nНС\nНикита Смирнов\nООО "ЭКОСИСТЕМА"\nПодтвердите роль куратора\nВам необходимо добавить документы в профиль пользователя, чтобы подтвердить роль\nДобавить документы\nВсе\nОтраслевые сервисы\nПоддержка б'
FAILED tests/lk/test_lk_smoke.py::test_lk_header_action_buttons - AssertionError: Кнопка «Написать нам» не видна или недоступна
======= 2 failed, 16 passed, 3 skipped, 3 warnings in 300.11s (0:05:00) ========
LK pytest: 16/21 passed, failed=2, errors=0, skipped=3 in 301.2s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
======== 8 passed, 2 skipped, 2 warnings, 4 errors in 227.36s (0:03:47) ========
LK pytest: 8/14 passed, failed=0, errors=4, skipped=2 in 228.4s
Pytest metrics sent to InfluxDB (run_status=fail)
Failure events sent to InfluxDB (таблица Grafana)
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
======== 8 passed, 2 skipped, 2 warnings, 4 errors in 341.07s (0:05:41) ========
LK pytest: 8/14 passed, failed=0, errors=4, skipped=2 in 342.3s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
ERROR tests/ui/selenium_ui/test_landing_chatbot.py::test_landing_chatbot_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_mincifry_card_click_skips_login_and_registration - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
ERROR tests/ui/selenium_ui/test_mincifry.py::test_landing_mincifry_full_flow - selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome instance exited. Examine ChromeDriver verbose log to determine the cause.; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#sessionnotcreatedexception
======== 8 passed, 2 skipped, 2 warnings, 4 errors in 186.00s (0:03:06) ========
LK pytest: 8/14 passed, failed=0, errors=4, skipped=2 in 187.2s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
```

## cron.log (daily) tail markers

```
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
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 38/39 passed, failed=1, errors=0 in 7.1s
Metrics sent to InfluxDB (run_status=autotest)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

