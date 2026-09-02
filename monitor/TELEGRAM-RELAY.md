# Telegram без блокировок РКН (схема для VPS)

## Проблема

С RU VPS **api.telegram.org** часто недоступен.  
**TELEGRAM_PROXY** на VPS — риск блокировки (похоже на обход ограничений).

## Решение: GitHub relay

```
VPS (157.22.191.247)
  run_light.sh / run_daily.sh
       │ только при FAIL
       ▼
  api.github.com  (repository_dispatch)
       │
       ▼
  GitHub Actions (облако)
       │
       ▼
  api.telegram.org  →  ваш Telegram
```

VPS **не** обращается к Telegram. РКN блокировал старый сервер из‑за **VPN**, не из‑за Telegram.

---

## Настройка (один раз)

### 1. GitHub Secrets

Репо `Chikitoska/test_BID_AI` → **Settings → Secrets → Actions**:

| Secret | Значение |
|--------|----------|
| `TELEGRAM_BOT_TOKEN` | от @BotFather |
| `TELEGRAM_CHAT_ID` | ваш chat id (или id группы) |
| `SMTP_HOST` | напр. `smtp.yandex.ru` |
| `SMTP_PORT` | `465` (SSL) или `587` (TLS) |
| `SMTP_USER` | ваш email |
| `SMTP_PASSWORD` | пароль приложения / SMTP |
| `ALERT_EMAIL_TO` | получатели через **запятую**: `you@co.ru, colleague@co.ru` |
| `SMTP_FROM` | опционально, по умолчанию = SMTP_USER |
| `SMTP_USE_TLS` | `true` для порта 587, иначе можно не задавать |

**Email:** при каждой ошибке письмо уходит **с VPS** (если SMTP в `monitor/.env`).  
GitHub Actions + Yandex часто даёт `454 Try again later` — это блокировка IP датацентра, не ваш пароль.

| Где | Telegram | Email |
|-----|----------|-------|
| GitHub Secrets | `TELEGRAM_*` | не нужно (можно удалить `SMTP_*`) |
| VPS `monitor/.env` | пусто | `SMTP_*`, `ALERT_EMAIL_TO` |

### 2. GitHub PAT

https://github.com/settings/tokens → **classic** → scope **`repo`**

### 3. monitor/.env на VPS

```env
GITHUB_PAT=ghp_...
GITHUB_REPO=Chikitoska/test_BID_AI

# Telegram на VPS — ПУСТО:
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_PROXY=
```

### 4. Проверка на VPS

```bash
cd /opt/test_BID_AI
./monitor/verify_github_relay.sh
```

### 5. Тест сообщения

GitHub → **Actions** → **BID Telegram Relay** → **Run workflow** → status: **fail**

Должно прийти: сообщение в Telegram **и** письмо на все адреса из `ALERT_EMAIL_TO`.

---

## Поведение алертов

| Событие | Когда шлётся |
|---------|----------------|
| Быстрая проверка FAIL | **сразу** при первом FAIL (после retry ~30 с) |
| Повтор FAIL | раз в **4 ч**, если всё ещё падает |
| OK каждые 5 мин | **не** шлётся |
| Полный прогон FAIL | сразу + повтор раз в 4 ч |
| Полный прогон | **каждый час** (HTTP + pytest) |

---

## Чего не делать на VPS

- ❌ `TELEGRAM_BOT_TOKEN` в monitor/.env  
- ❌ `TELEGRAM_PROXY=socks5://...`  
- ❌ WireGuard / OpenVPN  

---

## Если dispatch не работает

```bash
grep GITHUB /opt/test_BID_AI/monitor/.env
./monitor/verify_github_relay.sh
```

Лог probe при FAIL: `GitHub dispatch sent`  
GitHub → Actions — запуск **BID Telegram Relay**

---

## Email: пошаговая настройка

Письма уходят **только при ошибках** (health FAIL, pytest упал, ЛК не прошёл).  
Успешные прогоны — без писем.

### Шаг 1 — пароль приложения SMTP

Пример для **Yandex**:

1. [id.yandex.ru](https://id.yandex.ru) → Безопасность → **Пароли приложений**
2. Создать пароль для «Почта» / «Другое»
3. Сохранить пароль (показывается один раз)

Для **Gmail**: App Password в Google Account → Security.

### Шаг 2 — SMTP в monitor/.env на VPS

На VPS (не в GitHub Secrets):

```env
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=465
SMTP_USER=ваш@yandex.ru
SMTP_PASSWORD=пароль-приложения
ALERT_EMAIL_TO=вы@mail.ru, коллега@mail.ru
```

**Добавить коллегу:** допишите email в `ALERT_EMAIL_TO` через запятую.

### Шаг 3 — проверка с VPS

```bash
cd /opt/test_BID_AI
./monitor/verify_smtp.sh
```

Должно быть: `Email sent to: ...` и письмо во входящих.

### Шаг 4 — git pull на VPS

```bash
cd /opt/test_BID_AI && git pull
```

### Шаг 5 — тест при ошибке

GitHub → **BID Telegram Relay → fail** — проверяет только Telegram.  
Email при реальных падениях шлёт VPS вместе с `GitHub dispatch sent`.
