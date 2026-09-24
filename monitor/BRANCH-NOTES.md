# Ветки — не забыть

## ⛔ `feature/unified-spa-uuid`

**НЕ мержить в `main`. НЕ выкатывать на VPS** — пока пользователь явно не скажет.

Смысл ветки: единый хардкодный SPA UUID на лендинг + Keycloak + portal-fe (ЛК); адаптация логики фронта (`getOrCreateCustomUserId` / shared cookie), без `crypto.randomUUID()`.

### Сделано

- Inject в `utils/selenium_factory.py`: CDP `Network.setCookie` на `MONITOR_SPA_ROOT_DOMAIN` (`bid.gazprom-neft.ru`) + `Page.addScriptToEvaluateOnNewDocument` (cookie как `setSharedCookie` + `localStorage.gpnSpaUid` для `counter.js`).
- Значение всегда `MONITOR_ANALYTICS_UID` (`b1d00000-0000-4000-a000-000000000001`).
- Cookie key: `SPA_USER_ID_COOKIE_KEY` (placeholder `spa_user_id` — **уточнить у фронта** имя `SPA_USER_ID_KEY`).
- `monitor/verify_analytics_uid.py` проверяет cookie + localStorage + POST `/events` (лендинг, cookie на Keycloak, ЛК).

### Ждёт отмашки

- Подтверждение имени cookie (`SPA_USER_ID_KEY`) и `root_domain` из конфига фронта.
- Merge в `main` и деплой на VPS — только по явной команде.
