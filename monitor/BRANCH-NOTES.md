# Заметки по веткам monitor

бэклог: `monitor/BACKLOG.md`

- **`feature/grafana-errors-xlsx-export`** — HTTP Basic Auth выгрузка `bid_failure` → XLSX + ссылка Grafana `${__from}`/`${__to}`. См. `monitor/EXPORT-ERRORS-XLSX.md`.
- **`feature/unified-spa-uuid`** — единый SPA UUID через cookie `gpn_spa_custom_user_id_cookie`. Фронт уже на PROD; ветка сливается в `main`.

## `feature/unified-spa-uuid`

Смысл: единый хардкодный SPA UUID на лендинг + Keycloak + portal-fe (ЛК); адаптация логики фронта (`getOrCreateCustomUserId` / shared cookie), без `crypto.randomUUID()`.

### Сделано

- Inject в `utils/selenium_factory.py`: CDP `Network.setCookie` на `MONITOR_SPA_ROOT_DOMAIN` (`bid.gazprom-neft.ru`) + `Page.addScriptToEvaluateOnNewDocument` (cookie как `setSharedCookie`; опционально `localStorage.gpnSpaUid` для `counter.js`, не SoT).
- Значение всегда `MONITOR_ANALYTICS_UID` (`b1d00000-0000-4000-a000-000000000001`).
- Cookie key: `SPA_USER_ID_COOKIE_KEY` = `gpn_spa_custom_user_id_cookie` (фронтовая `SPA_USER_ID_KEY`). **Источник истины — только cookie**, не localStorage.
- Domain cookie: `bid.gazprom-neft.ru` (видны на bid / id.bid / lk.bid).
- Атрибуты cookie (как у фронта `setSharedCookie`): `path=/`, `Secure` (на https / CDP), `SameSite=Lax`, `max-age` = `SPA_USER_ID_COOKIE_MAX_AGE_SEC` (дефолт `365*24*60*60`).
- `monitor/verify_analytics_uid.py`: основной check = cookie + POST `/events`; localStorage — информативно/warn.
- HTTP POST `/events` в автотестах тоже шлёт этот же UUID.

### Ответы фронта (2026-09-25)

| # | Вопрос | Ответ |
|---|--------|-------|
| 1 | `root_domain` prod = `bid.gazprom-neft.ru`? | ✅ ДА |
| 2 | Если cookie уже есть — `getOrCreateCustomUserId` не создаёт новый, только продлевает? | ✅ ДА |
| 3 | Лендинг / Keycloak / portal-fe читают только `gpn_spa_custom_user_id_cookie`? | ✅ ДА |
| 4 | В `/events` уходит то же значение из этой cookie? | ✅ ДА |
| 5 | На error 4xx/5xx аналитика тоже читает эту cookie? | ✅ ДА (с оговоркой «вроде как») |
| 6 | `max-age` = фронтовый `DEFAULT_COOKIE_AGE_SECONDS`? | ✅ ДА ставить как у них, **но число не назвали** |
| — | Cookie key `gpn_spa_custom_user_id_cookie` | ✅ уже в коде |
| — | `Secure` + `SameSite=Lax` | ⚠️ **не подтверждено явно**; в коде как у фронта (`setSharedCookie`) |
