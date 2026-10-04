# LK tests

Автотесты личного кабинета (`lk.bid.gazprom-neft.ru`): Keycloak + TOTP.

## BE API smoke (`lk_be`)

После одного FE-логина (`LkFlow` + TOTP) извлекаем auth (cookie / localStorage /
sessionStorage) и дергаем BE endpoints через `requests` (ожидаем **HTTP 200**).

```bash
# только BE smoke
.venv/bin/pytest -m lk_be tests/lk/test_lk_be_api.py -v

# весь ЛК (включая BE) — как combat run_lk_pytest
.venv/bin/pytest tests/lk/ -v
```

Каталог: `config/lk_be_api_catalog.py` (из capture Заявки 2026-10-04).

| Группа | Поведение |
| --- | --- |
| Active GET (22) | assert status **200** |
| `gost-lk…` | `pytest.skip` — **GOST/CA later** |
| `requests/archived` | `pytest.skip` — 403 ACL, permissions TBD |
| `spa-back…/events` POST | `pytest.skip` — analytics, daily GET-only |

Токен: один логин на сессию/модуль; при **401** — один refresh (re-extract, затем re-login).

### Daily / monitor

- Уже подхватывается **`monitor/run_lk_pytest.py`** (весь `tests/lk/`).
- В **`run_daily`** (`tests/api/`) **не** включено: нужен Chrome + credentials,
  иначе удлинит/сломает VPS daily без ЛК-секретов.
- Подключить в daily позже: добавить путь/`-m lk_be` когда credentials+Chrome
  стабильны на хосте daily.

Credentials: `BID_USERNAME` / `BID_PASSWORD` / `BID_TOTP_SECRET` в `monitor/.env`.
