# Мониторинг BID 24/7 без MacBook

VPS AdminVPS **не видит** BID (timeout). Mac **видит** (200), но выключен.

**Решение:** GitHub Actions по расписанию → probe в облаке → InfluxDB на VPS → Grafana.

```
GitHub Actions (cron)  ──►  bid.gazprom-neft.ru  ✅
                       ──►  78.17.46.33:8086     InfluxDB
                       ──►  Telegram
Browser                ──►  78.17.46.33:3000     Grafana
```

Mac **не нужен**.

---

## 1. Репозиторий на GitHub

```bash
cd ~/Projects/test_BID_AI
git init
git add .
git commit -m "BID monitoring"
```

Создай репозиторий на GitHub (можно **private**).

```bash
git remote add origin git@github.com:USER/test_BID_AI.git
git push -u origin main
```

> **Private repo:** ~2000 мин/мес бесплатно → probe **каждый час**.  
> **Public repo:** минуты без лимита → probe **каждые 10 мин**.

---

## 2. Secrets в GitHub

Repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Значение |
|--------|----------|
| `INFLUXDB_TOKEN` | из `/opt/test_BID_AI/.env` на VPS |
| `TELEGRAM_BOT_TOKEN` | токен бота |
| `TELEGRAM_CHAT_ID` | `318498795` |

---

## 3. InfluxDB на VPS

Порт 8086 уже открыт (`ufw inactive`). Доступ защищён **токеном**, не IP.

Проверка с любой машины:

```bash
curl -s -o /dev/null -w "%{http_code}" http://78.17.46.33:8086/health
```

---

## 4. Отключить probe на VPS и Mac

**VPS:**

```bash
crontab -e   # удалить run_light.sh
```

**Mac:** cron не ставить.

---

## 5. Проверка GitHub Actions

Repo → **Actions** → workflow **BID Monitor** → **Run workflow**.

Лог: `Probe finished — OK`, Grafana зелёная.

---

## Альтернативы (если GitHub не видит BID)

| Вариант | Плюсы |
|---------|--------|
| **Public repo** + probe каждые 10 мин | бесплатно, без Mac |
| **Raspberry Pi** дома (~3 000 ₽) | всегда в вашей сети |
| **Другой VPS** (Selectel, Timeweb) | проверить `curl` + browser UA |
| **Рабочий ПК** в офисе | cron + probe |

Тест с VPS-кандидата:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" \
  https://bid.gazprom-neft.ru/config.json
```

`200` = подходит для probe.

---

## Расписание в workflow

Файл `.github/workflows/bid-monitor.yml`:

- **probe** — каждый час (private) или каждые 10 мин (public)
- **full** — 08:00 и 20:00 МСК
