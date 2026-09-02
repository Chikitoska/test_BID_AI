#!/usr/bin/env python3
"""Проверка SMTP с VPS (monitor/.env)."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from monitor.email_relay import email_config_status, email_configured, send_alert_email


def main() -> int:
    print("=== SMTP (VPS) ===")
    print(email_config_status())
    if not email_configured():
        print("\nERROR: добавьте SMTP_* и ALERT_EMAIL_TO в monitor/.env")
        return 1

    ok = send_alert_email(
        subject="BID — тест SMTP",
        body="Тестовое письмо с VPS. Если видите это — email-алерты работают.",
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
