# Ветки — не забыть

## ⛔ `feature/unified-spa-uuid`

**НЕ мержить в `main`. НЕ выкатывать на VPS** — пока пользователь явно не скажет.

Смысл ветки: единый хардкодный SPA UUID на лендинг + Keycloak + portal-fe (ЛК); адаптация логики фронта (`getOrCreateCustomUserId` / shared cookie), без `crypto.randomUUID()`.

### Сделано

- Inject в `utils/selenium_factory.py`: CDP `Network.setCookie` на `MONITOR_SPA_ROOT_DOMAIN` (`bid.gazprom-neft.ru`) + `Page.addScriptToEvaluateOnNewDocument` (cookie как `setSharedCookie`; опционально `localStorage.gpnSpaUid` для `counter.js`, не SoT).
- Значение всегда `MONITOR_ANALYTICS_UID` (`b1d00000-0000-4000-a000-000000000001`).
- Cookie key: `SPA_USER_ID_COOKIE_KEY` = `gpn_spa_custom_user_id_cookie` (фронтовая `SPA_USER_ID_KEY`). **Источник истины — только cookie**, не localStorage.
- Domain cookie: `bid.gazprom-neft.ru` (видны на bid / id.bid / lk.bid).
- `monitor/verify_analytics_uid.py`: основной check = cookie + POST `/events`; localStorage — информативно/warn.

### Ждёт отмашки

- Merge в `main` и деплой на VPS — только по явной команде.
