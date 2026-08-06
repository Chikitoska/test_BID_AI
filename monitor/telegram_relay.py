#!/usr/bin/env python3
"""
Relay: получает статус probe (repository_dispatch) → шлёт Telegram из GitHub Actions.
FirstVDS не достучится до api.telegram.org — relay запускается в облаке GitHub.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

STATE_FILE = os.getenv("RELAY_STATE_FILE", "relay-state.txt")


def _probe_status() -> str | None:
    status = os.getenv("PROBE_STATUS", "").strip().lower()
    if status in ("ok", "fail"):
        return status
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
    response = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
        timeout=20,
    )
    response.raise_for_status()
    return True


def main() -> int:
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print("ERROR: задайте TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        return 1

    current = _probe_status()
    if current is None:
        print("ERROR: PROBE_STATUS must be ok or fail")
        return 1

    previous = _load_state()
    failed_count = os.getenv("PROBE_FAILED_COUNT", "0")
    duration_sec = os.getenv("PROBE_DURATION_SEC", "")

    if previous is None:
        _save_state(current)
        print(f"Init state: {current}")
        return 0

    if current == previous:
        print(f"No change: {current}")
        return 0

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    extra = ""
    if duration_sec:
        extra = f"\nДлительность: {duration_sec}s"
    if failed_count != "0":
        extra += f"\nУпало проверок: {failed_count}"

    if current == "fail":
        msg = (
            f"<b>🔴 BID Probe — FAIL</b>\n\n"
            f"Сервер: FirstVDS\n"
            f"Время: {now}{extra}\n\n"
            f"Проверьте Grafana."
        )
    else:
        msg = f"<b>🟢 BID Probe — восстановлено</b>\n\nВремя: {now}{extra}"

    _send_telegram(msg)
    _save_state(current)
    print(f"Alert sent: {previous} → {current}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
