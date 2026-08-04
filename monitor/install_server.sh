#!/bin/bash
# Установка мониторинга BID на чистый VPS (Ubuntu/Debian)
# Запуск на сервере: bash monitor/install_server.sh
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/opt/test_BID_AI}"
SERVER_IP="${SERVER_IP:-78.17.46.33}"

echo "=== BID Monitor: установка на $SERVER_IP ==="
echo "Каталог проекта: $PROJECT_DIR"

# --- 1. Docker ---
if ! command -v docker &>/dev/null; then
  echo "[1/6] Установка Docker..."
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER" 2>/dev/null || true
  echo "Docker установлен. Если нужен docker без sudo — перелогиньтесь и запустите скрипт снова."
else
  echo "[1/6] Docker уже установлен: $(docker --version)"
fi

COMPOSE_CMD="docker compose"
if ! docker compose version &>/dev/null 2>&1; then
  echo "[1/6] Установка Docker Compose..."
  if command -v apt-get &>/dev/null; then
    apt-get update -qq
    apt-get install -y -qq docker-compose-v2 2>/dev/null \
      || apt-get install -y -qq docker-compose-plugin 2>/dev/null \
      || true
  fi
fi

if ! docker compose version &>/dev/null 2>&1; then
  if command -v docker-compose &>/dev/null; then
    COMPOSE_CMD="docker-compose"
    echo "[1/6] Используем docker-compose (v1)"
  else
    echo "ERROR: docker compose не найден. Выполните: apt-get install -y docker-compose-v2"
    exit 1
  fi
else
  echo "[1/6] Docker Compose: $(docker compose version)"
fi

# --- 2. Зависимости системы ---
echo "[2/6] Системные пакеты..."
if command -v apt-get &>/dev/null; then
  apt-get update -qq
  apt-get install -y -qq python3 python3-venv python3-pip curl git openssl
fi

# --- 3. Проверка проекта ---
if [ ! -f "$PROJECT_DIR/monitor/run_daily.py" ]; then
  echo ""
  echo "ERROR: Проект не найден в $PROJECT_DIR"
  echo "Скопируйте test_BID_AI на сервер, например:"
  echo "  scp -r test_BID_AI user@${SERVER_IP}:/opt/"
  echo "или git clone в $PROJECT_DIR"
  exit 1
fi

cd "$PROJECT_DIR"

# --- 4. Python venv ---
echo "[3/6] Python окружение..."
if [ -d .venv ] && ! .venv/bin/python -c "import sys; sys.exit(0)" &>/dev/null; then
  echo "WARN: .venv с Mac/другой ОС — пересоздаём"
  rm -rf .venv
fi
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt

# --- 5. Конфиг ---
echo "[4/6] Конфигурация .env..."
if [ ! -f .env ]; then
  cp .env.example .env
  TOKEN=$(openssl rand -hex 32)
  sed -i "s/your-long-random-token-here/$TOKEN/" .env
  sed -i "s/strong_influx_password/$(openssl rand -hex 16)/" .env
  sed -i "s/strong_grafana_password/$(openssl rand -hex 16)/" .env
  echo "Создан .env с случайными паролями. Сохраните их:"
  grep -E "^(INFLUXDB_TOKEN|GRAFANA_ADMIN_PASSWORD|INFLUXDB_ADMIN_PASSWORD)=" .env
fi

if [ ! -f monitor/.env ]; then
  cp monitor/.env.example monitor/.env
  INFLUX_TOKEN=$(grep ^INFLUXDB_TOKEN= .env | cut -d= -f2-)
  sed -i "s/CHANGE_ME_GENERATE_ON_SERVER/$INFLUX_TOKEN/" monitor/.env
fi

# --- 6. Проверка доступа к BID ---
echo "[5/6] Проверка bid.gazprom-neft.ru с сервера..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 https://bid.gazprom-neft.ru/ 2>/dev/null || true)
HTTP_CODE=${HTTP_CODE:-000}
echo "HTTP код главной: $HTTP_CODE"
if [ "$HTTP_CODE" = "000" ] || [ "$HTTP_CODE" -ge 500 ]; then
  echo "WARN: Сайт недоступен или 5xx. Мониторинг может постоянно падать."
elif [ "$HTTP_CODE" = "403" ]; then
  echo "WARN: 403 — возможно нужен VPN/корп. сеть на этом VPS."
fi

# --- 7. Docker Compose ---
echo "[6/6] Запуск InfluxDB + Grafana..."
set -a
# shellcheck disable=SC1091
source .env
set +a
$COMPOSE_CMD up -d

chmod +x monitor/run_daily.sh

echo ""
echo "=== Готово ==="
echo "Grafana:  http://${SERVER_IP}:3000"
echo "Логин:    admin"
echo "Пароль:   см. GRAFANA_ADMIN_PASSWORD в $PROJECT_DIR/.env"
echo ""
echo "InfluxDB token: см. INFLUXDB_TOKEN в $PROJECT_DIR/.env"
echo ""
echo "Проверка мониторинга:"
echo "  cd $PROJECT_DIR && ./monitor/run_daily.sh"
echo ""
echo "Cron (ежедневно 08:00):"
echo "  (crontab -l 2>/dev/null; echo '0 8 * * * $PROJECT_DIR/monitor/run_daily.sh >> $PROJECT_DIR/monitor/cron.log 2>&1') | crontab -"
echo ""
echo "Grafana → Connections → Data sources → InfluxDB-BID:"
echo "  вставьте INFLUXDB_TOKEN если datasource не подключился автоматически"
