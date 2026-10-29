"""Единый SPA UUID мониторинга для cookie и POST spa-back/events."""

from __future__ import annotations

import json
import os
from typing import Any

DEFAULT_MONITOR_ANALYTICS_UID = "b1d00000-0000-4000-a000-000000000001"
DEFAULT_SPA_USER_ID_COOKIE_KEY = "gpn_spa_custom_user_id_cookie"
SPA_EVENTS_COUNTER_ID = 1212
_UID_KEYS = ("uid", "customUserId", "custom_user_id", "userId")


def spa_events_uid() -> str:
    return os.getenv("MONITOR_ANALYTICS_UID", DEFAULT_MONITOR_ANALYTICS_UID).strip()


def spa_user_id_cookie_key() -> str:
    return os.getenv("SPA_USER_ID_COOKIE_KEY", DEFAULT_SPA_USER_ID_COOKIE_KEY).strip()


def spa_events_cookie_header() -> str:
    return f"{spa_user_id_cookie_key()}={spa_events_uid()}"


def spa_events_payload(
    *,
    event: str = "page_view",
    counter_id: int = SPA_EVENTS_COUNTER_ID,
) -> list[dict[str, Any]]:
    """Тело POST /events: всегда один и тот же MONITOR_ANALYTICS_UID."""
    return [
        {
            "event": event,
            "counterId": counter_id,
            "uid": spa_events_uid(),
        }
    ]


def extract_uids_from_events_payload(payload: Any) -> list[str]:
    found: list[str] = []

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            for key in _UID_KEYS:
                value = obj.get(key)
                if value:
                    found.append(str(value))
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(payload)
    return found


def extract_uids_from_events_body(post_data: str) -> list[str]:
    if not post_data:
        return []
    try:
        payload = json.loads(post_data)
    except json.JSONDecodeError:
        return []
    return extract_uids_from_events_payload(payload)
