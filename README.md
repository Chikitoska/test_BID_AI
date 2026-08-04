# Автотесты BID (Газпром Бизнес ID)

Проект **test_BID_AI** — автотесты для https://bid.gazprom-neft.ru/

**Scope:** публичный лендинг + backend (2xx), **без авторизации** (кнопка «Войти» / Keycloak / OIDC исключены).

## Структура

```
test_BID_AI/
├── config/settings.py      # URL, API, паттерны auth
├── pages/landing_page.py   # Page Object лендинга
├── utils/                  # HTTP, network log, auth filter
├── tests/
│   ├── api/                # Backend (requests)
│   └── ui/                 # Frontend (Selenium)
├── pytest.ini
└── requirements.txt
```

## Запуск

```bash
cd ~/Projects/test_BID_AI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Все тесты
pytest

# Только API (быстро, без браузера)
pytest -m api

# Только Selenium-сценарии
pytest -m selenium tests/ui/selenium_ui/

# Только Playwright-сценарии
pytest -m playwright tests/ui/playwright_ui/

# После первой установки Playwright
playwright install chromium

# Smoke
pytest -m smoke
```

## PyCharm

**File → Open** → `~/Projects/test_BID_AI`  
Интерпретатор: `.venv/bin/python`

## Что покрыто

### Backend (API) — DevTools Network
- `GET /config.json` — конфиг лендинга
- `GET /api/gateway/public/api/public/service-provider` — сервисы
- `GET /api/gateway/global/legal-documents/v1` — юр. документы (bulk + по каждому)
- `GET /version` и `/version?k=...` — версия фронта
- `GET spa-back/static/counter.js` — скрипт аналитики
- `POST spa-back/events` — analytics-события
- Фильтрация service-provider по 6 тегам вкладок
- `GET lk.bid.gazprom-neft.ru/help-section` — раздел помощи

### Frontend (Selenium)
- Заголовок, URL, контент страницы
- Кнопка «Войти» видна, но **не нажимается**
- «Получить ID», блок ИНН, чекбоксы
- Навигационные вкладки (6 шт.)
- Форма обратной связи
- Console errors (SEVERE)
- Network log: все non-auth запросы 2xx/3xx
- Статические ресурсы и время загрузки

## Мониторинг (Grafana + InfluxDB)

Ежедневный мониторинг BID с дашбордом и Telegram-алертами.

**Инструкция и чек-лист:** [monitor/DEPLOY.md](monitor/DEPLOY.md)

```bash
docker compose up -d          # Grafana :3000, InfluxDB :8086
./monitor/run_daily.sh        # ручной прогон
```
