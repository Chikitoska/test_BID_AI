"""Отправка алертов по SMTP (GitHub Actions relay)."""

from __future__ import annotations

import os
import re
import smtplib
import ssl
from email.mime.text import MIMEText


def parse_alert_emails(raw: str | None = None) -> list[str]:
    """Список адресов из ALERT_EMAIL_TO: через запятую, точку с запятой или пробел."""
    value = (raw if raw is not None else os.getenv("ALERT_EMAIL_TO", "")).strip()
    if not value:
        return []
    parts = re.split(r"[,;\s]+", value)
    seen: set[str] = set()
    recipients: list[str] = []
    for part in parts:
        email = part.strip()
        if not email or email in seen:
            continue
        seen.add(email)
        recipients.append(email)
    return recipients


def email_config_status() -> str:
    """Для лога GitHub Actions — без паролей."""
    host = bool(os.getenv("SMTP_HOST", "").strip())
    user = bool(os.getenv("SMTP_USER", "").strip())
    password = bool(os.getenv("SMTP_PASSWORD", "").strip())
    recipients = parse_alert_emails()
    port_raw = os.getenv("SMTP_PORT", "").strip()
    parts = [
        f"SMTP_HOST={'yes' if host else 'NO'}",
        f"SMTP_USER={'yes' if user else 'NO'}",
        f"SMTP_PASSWORD={'yes' if password else 'NO'}",
        f"ALERT_EMAIL_TO={len(recipients)} addr(s)",
        f"SMTP_PORT={port_raw or '465 (default)'}",
    ]
    return ", ".join(parts)


def email_configured() -> bool:
    return bool(
        os.getenv("SMTP_HOST")
        and os.getenv("SMTP_USER")
        and os.getenv("SMTP_PASSWORD")
        and parse_alert_emails()
    )


def send_alert_email(subject: str, body: str) -> bool:
    host = os.getenv("SMTP_HOST", "").strip()
    user = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    recipients = parse_alert_emails()
    port_raw = os.getenv("SMTP_PORT", "465").strip()
    try:
        port = int(port_raw or "465")
    except ValueError:
        print(f"ERROR: SMTP_PORT invalid: {port_raw!r}")
        return False
    use_tls = os.getenv("SMTP_USE_TLS", "").lower() in ("1", "true", "yes")
    mail_from = os.getenv("SMTP_FROM", user).strip()

    if not all([host, user, password, recipients]):
        print("ERROR: SMTP не настроен (SMTP_HOST, SMTP_USER, SMTP_PASSWORD, ALERT_EMAIL_TO)")
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = ", ".join(recipients)

    try:
        if use_tls or port == 587:
            with smtplib.SMTP(host, port, timeout=30) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(user, password)
                server.send_message(msg, to_addrs=recipients)
        else:
            with smtplib.SMTP_SSL(host, port, timeout=30, context=ssl.create_default_context()) as server:
                server.login(user, password)
                server.send_message(msg, to_addrs=recipients)
        print(f"Email sent to: {', '.join(recipients)}")
        return True
    except smtplib.SMTPException as exc:
        print(f"ERROR: SMTP send failed: {exc}")
        return False
    except OSError as exc:
        print(f"ERROR: SMTP connection failed: {exc}")
        return False
