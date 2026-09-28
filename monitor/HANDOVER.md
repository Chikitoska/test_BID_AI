# Handover: мониторинг BID (`test_BID_AI`)

Кратко для начальника / преемника. Детали — в соседних файлах `monitor/`.

## Что это и зачем

Python QA/ops-контур вокруг **BID** (лендинг + личный кабинет): регулярные проверки PROD, метрики в Grafana, алерты в Telegram/email при реальных сбоях.

Это **не pet-проект и не игрушка**, но и **не enterprise-платформа**: рабочий Python-стек для наблюдения. Если мониторинг зелёный — он делает своё дело. Переписывать «с нуля» без нужды не стоит.

## Где крутится

| | |
|--|--|
| **VPS** | `157.22.191.247` |
| **Путь** | `/opt/test_BID_AI` |
| **Grafana** | `http://157.22.191.247:3000` (+ InfluxDB рядом) |
| **Секреты** | только `monitor/.env` **на VPS** (в git не класть) |

## Три прогона

1. **Health** (~каждые 5 мин) — «пульс»: лендинг + минимальный вход в ЛК.
2. **Daily** — более полный API/сводный прогон (расписание в crontab на VPS).
3. **lk_pytest** (~каждые 2 ч) — боевые UI-тесты ЛК через Chrome.

Метрики → **InfluxDB → Grafana :3000**. Алерты: сбой → **GitHub relay → Telegram / email** (с VPS напрямую к Telegram часто нельзя).

## Выгрузка ошибок (XLSX)

В Grafana есть кнопка **«Скачать ошибки (XLSX)»** (период = таймпикер дашборда).

- Endpoint под **HTTP Basic Auth**.
- Сервис: systemd **`bid-errors-export`**.
- Снаружи: nginx **`/export/`** → localhost:8765.
- Подробности: `monitor/EXPORT-ERRORS-XLSX.md`.

## Ветка / ожидание — не выкатывать

Ветка **`feature/unified-spa-uuid`**: единый SPA UUID (landing + Keycloak + portal-fe).

**Не мержить в `main` и не деплоить на VPS**, пока на фронте не выйдет cookie `gpn_spa_custom_user_id_cookie` и не будет **явной отмашки**. Иначе мониторинг/логин могут разъехаться с продом. См. `monitor/BRANCH-NOTES.md`.

## Бэклог

Живой чеклист: **`monitor/BACKLOG.md`**.

- **P0 уже в `main`** (Chrome-флаки ≠ «ЛК лежит»; busy Chrome → `skipped`, не ложный «всё ОК»).
- Дальше — P1+ (antiflap daily, lock на alert state, один email-канал и т.д.).

## Как проверить, что живо

1. Grafana `:3000` — свежие точки по health / daily / lk_pytest (нет долгой «тишины»).
2. На VPS: `crontab -l` — три прогона на месте.
3. Логи в `/opt/test_BID_AI/monitor/`:
   - `health.log` — пульс
   - `cron.log` — daily
   - `lk-pytest.log` — UI pytest
4. XLSX-export (если включён): `systemctl status bid-errors-export`; `curl -i http://127.0.0.1:8765/health`.
5. Сводка: `monitor/reports/latest.md` (если digests пишутся).

## Риски без владельца

Стек сам по себе не «самолечится»: crontab, Chrome, `.env`, Influx, nginx, GitHub secrets. Без человека:

- тихие пропуски проверок (Chrome занят, мёртвый write в Influx);
- ложные/пропавшие алерты;
- случайный `git pull` / деплой ветки UUID ломает контур.

**Рекомендация:** назначить **одного владельца** (кто смотрит Grafana/TG и трогает VPS) **либо не трогать стек**, пока мониторинг ок. «Поправить между делом» без контекста — главный риск.

---

*Не деплоить на VPS из этого документа автоматически. Деплой — только по явной команде.*
