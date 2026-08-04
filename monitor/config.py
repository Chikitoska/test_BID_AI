"""Настройки мониторинга из переменных окружения."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://127.0.0.1:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "bid")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "bid_monitor")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_PROXY = os.getenv("TELEGRAM_PROXY", "")

MONITOR_RUN_UI = os.getenv("MONITOR_RUN_UI", "false").lower() in ("1", "true", "yes")
MONITOR_TIMEZONE = os.getenv("MONITOR_TIMEZONE", "Europe/Moscow")
MONITOR_HTTP_TIMEOUT = int(os.getenv("MONITOR_HTTP_TIMEOUT", "10"))
MONITOR_HTTP_CONNECT_TIMEOUT = int(os.getenv("MONITOR_HTTP_CONNECT_TIMEOUT", "5"))
MONITOR_USER_AGENT = os.getenv(
    "MONITOR_USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
)
# Доп. коды «доступен» через WAF, напр. 403 — только если API отдают 200
MONITOR_ACCEPT_CODES = {
    int(code.strip())
    for code in os.getenv("MONITOR_ACCEPT_CODES", "").split(",")
    if code.strip().isdigit()
}

# Prod-алерты: probe без спама, full run — сводка 2 раза в день
TELEGRAM_ALERT_ON_SUCCESS = os.getenv("TELEGRAM_ALERT_ON_SUCCESS", "false").lower() in ("1", "true", "yes")
TELEGRAM_FULL_RUN_SUMMARY = os.getenv("TELEGRAM_FULL_RUN_SUMMARY", "true").lower() in ("1", "true", "yes")
TELEGRAM_ALERT_REPEAT_HOURS = float(os.getenv("TELEGRAM_ALERT_REPEAT_HOURS", "4"))
TELEGRAM_VERBOSE = os.getenv("TELEGRAM_VERBOSE", "false").lower() in ("1", "true", "yes")

ALERT_STATE_FILE = Path(os.getenv("ALERT_STATE_FILE", str(PROJECT_ROOT / "monitor" / ".alert_state.json")))

ALERTS_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
INFLUX_ENABLED = bool(INFLUXDB_TOKEN)
