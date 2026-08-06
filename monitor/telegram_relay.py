#!/usr/bin/env python3
"""
Relay: читает статус probe из InfluxDB (FirstVDS) → шлёт Telegram (из GitHub Actions).
FirstVDS не достучится до api.telegram.org — relay запускается в облаке GitHub.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

import requests
from influxdb_client import InfluxDBClient

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://62.109.31.244:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "bid")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "bid_monitor")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

STATE_FILE = os.getenv("RELAY_STATE_FILE", "relay-state.txt")


def _last_probe_ok() -> bool | None:
    query = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -30m)
  |> filter(fn: (r) => r._measurement == "bid_probe" and r._field == "success")
  |> last()
'''
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        tables = client.query_api().query(query, org=INFLUXDB_ORG)
        for table in tables:
            for record in table.records:
                return int(record.get_value()) == 1
    return None


def _load_state() -> str | None:
    try:
        return open(STATE_FILE, encoding="utf-8").read().strip() or None
    except OSError:
        return None


def _save_state(state: str) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(state)


def _send_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    r = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
        timeout=20,
    )
    r.raise_for_status()
    return True


def main() -> int:
    if not all([INFLUXDB_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print("ERROR: задайте INFLUXDB_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        return 1

    ok = _last_probe_ok()
    if ok is None:
        print("WARN: нет данных bid_probe за 30 мин — InfluxDB недоступен или probe не запускался")
        return 0

    current = "ok" if ok else "fail"
    previous = _load_state()

    if previous is None:
        _save_state(current)
        print(f"Init state: {current}")
        return 0

    if current == previous:
        print(f"No change: {current}")
        return 0

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if current == "fail":
        msg = f"<b>🔴 BID Probe — FAIL</b>\n\nСервер: FirstVDS\nВремя: {now}\n\nПроверьте Grafana."
    else:
        msg = f"<b>🟢 BID Probe — восстановлено</b>\n\nВремя: {now}"

    _send_telegram(msg)
    _save_state(current)
    print(f"Alert sent: {previous} → {current}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
