"""Сбор POST spa-back/events из Chrome performance log и проверка uid."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from utils.spa_analytics import (
    SPA_EVENTS_HOST,
    extract_event_names_from_events_body,
    extract_uids_from_events_body,
    spa_events_uid,
)


@dataclass
class SpaEventPost:
    body: str
    uids: list[str] = field(default_factory=list)
    event_names: list[str] = field(default_factory=list)


class SpaEventsUidError(AssertionError):
    """POST /events без MONITOR_ANALYTICS_UID или с чужим uid."""


def enable_performance_log(options) -> None:
    """goog:loggingPrefs для Network.requestWillBeSent. Не включать по умолчанию."""
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})


def drain_performance_log(driver) -> None:
    try:
        driver.get_log("performance")
    except Exception:
        pass


def collect_events_posts(driver) -> list[SpaEventPost]:
    posts: list[SpaEventPost] = []
    try:
        entries = driver.get_log("performance")
    except Exception:
        return posts

    for entry in entries:
        try:
            message = json.loads(entry["message"])["message"]
        except (KeyError, json.JSONDecodeError, TypeError):
            continue
        if message.get("method") != "Network.requestWillBeSent":
            continue
        params = message.get("params", {})
        request = params.get("request", {})
        url = request.get("url", "")
        if SPA_EVENTS_HOST not in url or request.get("method") != "POST":
            continue
        body = request.get("postData") or ""
        if not body:
            request_id = params.get("requestId")
            if request_id:
                try:
                    data = driver.execute_cdp_cmd(
                        "Network.getRequestPostData", {"requestId": request_id}
                    )
                    body = data.get("postData") or ""
                except Exception:
                    body = ""
        posts.append(
            SpaEventPost(
                body=body,
                uids=extract_uids_from_events_body(body),
                event_names=extract_event_names_from_events_body(body),
            )
        )
    return posts


def collect_events_post_bodies(driver) -> list[str]:
    return [item.body for item in collect_events_posts(driver)]


def uids_from_posts(posts: list[SpaEventPost] | list[str]) -> list[str]:
    found: list[str] = []
    for item in posts:
        if isinstance(item, SpaEventPost):
            found.extend(item.uids)
        else:
            found.extend(extract_uids_from_events_body(item))
    return found


def event_names_from_posts(posts: list[SpaEventPost] | list[str]) -> list[str]:
    names: list[str] = []
    for item in posts:
        if isinstance(item, SpaEventPost):
            names.extend(item.event_names)
        else:
            names.extend(extract_event_names_from_events_body(item))
    return names


def assert_only_monitor_uid(
    posts: list[SpaEventPost] | list[str],
    *,
    expected: str | None = None,
    require_posts: bool = True,
    context: str = "SPA /events",
) -> None:
    """Ожидаемый uid есть, чужих нет. Пустой лог / тело без uid — ошибка при require_posts."""
    target = (expected or spa_events_uid()).strip()
    bodies = [item.body if isinstance(item, SpaEventPost) else item for item in posts]
    uids = uids_from_posts(posts)

    if require_posts and not bodies:
        raise SpaEventsUidError(f"{context}: POST /events не обнаружен")
    if require_posts and bodies and not uids:
        raise SpaEventsUidError(
            f"{context}: POST /events без uid в теле (ожидали {target})"
        )
    foreign = [uid for uid in uids if uid != target]
    if foreign:
        raise SpaEventsUidError(f"{context}: чужие uid (не {target}): {foreign}")
    if uids and target not in uids:
        raise SpaEventsUidError(
            f"{context}: ожидаемый uid {target} не найден, факты={uids}"
        )
