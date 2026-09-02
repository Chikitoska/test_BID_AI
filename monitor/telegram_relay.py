#!/usr/bin/env python3
"""
Relay: repository_dispatch при неуспехе → Telegram + email (GitHub Actions).
Письмо уходит при каждой ошибке, если настроен SMTP (не только fallback).
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
from monitor.email_relay import email_config_status, email_configured, send_alert_email
from monitor.run_labels import get_run_label

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


def _alert_subject(run_type: str) -> str:
    return f"BID — {get_run_label(run_type)}"


def _send_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=20,
    )
    response.raise_for_status()


def _deliver_alert(*, subject: str, message: str, run_type: str) -> int:
    telegram_ok = False
    email_ok = False

    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            _send_telegram(message)
            print(f"Sent Telegram: fail ({run_type})")
            telegram_ok = True
        except requests.RequestException as exc:
            print(f"WARN: Telegram failed: {exc}")
    else:
        print("WARN: TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set")

    if email_configured():
        if send_alert_email(subject, message):
            email_ok = True
        else:
            print("ERROR: email send failed")
    else:
        print(f"INFO: SMTP not configured — email skipped ({email_config_status()})")

    if telegram_ok or email_ok:
        return 0

    print("ERROR: no alert channel succeeded (Telegram and email failed or not configured)")
    return 1


def main() -> int:
    status = _probe_status()
    if status is None:
        print("ERROR: PROBE_STATUS must be ok or fail")
        return 1

    if status == "ok":
        print("Skipped: all checks ok")
        return 0

    run_type = os.getenv("RUN_TYPE", "probe")
    pytest_failed = int(os.getenv("PYTEST_FAILED", "0") or "0")
    pytest_total = int(os.getenv("PYTEST_TOTAL", "0") or "0")

    message = format_relay_failure_message(
        _load_failures(),
        run_type=run_type,
        pytest_failed=pytest_failed,
        pytest_total=pytest_total,
        pytest_error=os.getenv("PYTEST_ERROR", ""),
    )
    return _deliver_alert(subject=_alert_subject(run_type), message=message, run_type=run_type)


if __name__ == "__main__":
    raise SystemExit(main())
