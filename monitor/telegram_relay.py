#!/usr/bin/env python3
"""
Relay: repository_dispatch при неуспехе probe/autotests → Telegram (GitHub Actions).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.alerts import format_relay_failure_message

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def _probe_status() -> str | None:
    status = os.getenv("PROBE_STATUS", "").strip().lower()
    if status in ("ok", "fail"):
        return status
    return None


def _load_failures() -> list[dict]:
    raw = os.getenv("PROBE_FAILURES_JSON", "[]").strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        print(f"WARN: invalid PROBE_FAILURES_JSON: {raw[:120]}")
        return []


def _send_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=20,
    )
    response.raise_for_status()
    return True


def main() -> int:
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print("ERROR: задайте TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        return 1

    status = _probe_status()
    if status is None:
        print("ERROR: PROBE_STATUS must be ok or fail")
        return 1

    if status == "ok":
        print("Skipped Telegram: all checks ok")
        return 0

    run_type = os.getenv("RUN_TYPE", "probe")
    pytest_failed = int(os.getenv("PYTEST_FAILED", "0") or "0")
    pytest_total = int(os.getenv("PYTEST_TOTAL", "0") or "0")

    message = format_relay_failure_message(
        _load_failures(),
        run_type=run_type,
        pytest_failed=pytest_failed,
        pytest_total=pytest_total,
    )
    _send_telegram(message)
    print(f"Sent Telegram: fail ({run_type})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
