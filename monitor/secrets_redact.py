"""Маскирование секретов в логах, InfluxDB и Telegram relay."""

from __future__ import annotations

import os
import re

_SECRET_ENV_KEYS = (
    "BID_USERNAME",
    "BID_PASSWORD",
    "BID_TOTP_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "GITHUB_PAT",
    "INFLUXDB_TOKEN",
)


def redact_secrets(text: str, *, limit: int = 200) -> str:
    if not text:
        return ""

    result = text
    for key in _SECRET_ENV_KEYS:
        value = os.getenv(key, "")
        if value and len(value) >= 4:
            result = result.replace(value, f"[{key}]")

    result = re.sub(r"\b\d{6}\b", "[OTP]", result)
    result = re.sub(r"(?i)(password|token|secret|authorization)[=:\s]+\S+", r"\1=[REDACTED]", result)
    return result[:limit]
