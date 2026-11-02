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


class SpaEventsHarnessError(SpaEventsUidError):
    """Страница жива, сниффер пуст — промах автотеста, не сеть."""


class SpaEventsNetworkError(SpaEventsUidError):
    """spa-back ответил 5xx или timeout — красный network."""


@dataclass
class SpaEventsNetworkHints:
    statuses: list[int] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    page_status: int = 0


def enable_performance_log(options) -> None:
    """goog:loggingPrefs для Network.requestWillBeSent. Не включать по умолчанию."""
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})


def drain_performance_log(driver) -> None:
    try:
        driver.get_log("performance")
    except Exception:
        pass


def collect_hooked_event_bodies(driver) -> list[str]:
    """Тела POST /events, которые патч fetch/XHR/sendBeacon сложил в window."""
    try:
        raw = driver.execute_script(
            "return Array.isArray(window.__BID_MONITOR_EVENTS) "
            "? window.__BID_MONITOR_EVENTS.slice() : [];"
        )
    except Exception:
        return []
    bodies: list[str] = []
    for item in raw or []:
        if item is None:
            continue
        text = item if isinstance(item, str) else str(item)
        bodies.append(text)
    return bodies


def _post_from_body(body: str) -> SpaEventPost:
    text = body or ""
    return SpaEventPost(
        body=text,
        uids=extract_uids_from_events_body(text),
        event_names=extract_event_names_from_events_body(text),
    )


def collect_events_capture(driver) -> tuple[list[SpaEventPost], SpaEventsNetworkHints]:
    """Один drain performance log: тела POST /events + статусы/ошибки spa-back."""
    posts: list[SpaEventPost] = []
    seen: set[str] = set()
    hints = SpaEventsNetworkHints(page_status=page_http_status(driver))

    def add(body: str) -> None:
        text = body or ""
        key = text or f"empty:{len(posts)}"
        if key in seen:
            return
        seen.add(key)
        posts.append(_post_from_body(text))

    for body in collect_hooked_event_bodies(driver):
        add(body)

    try:
        entries = driver.get_log("performance")
    except Exception:
        entries = []

    request_ids: set[str] = set()
    for entry in entries:
        try:
            message = json.loads(entry["message"])["message"]
        except (KeyError, json.JSONDecodeError, TypeError):
            continue
        method = message.get("method")
        params = message.get("params", {})
        if method == "Network.requestWillBeSent":
            request = params.get("request", {})
            url = request.get("url", "")
            if SPA_EVENTS_HOST not in url or request.get("method") != "POST":
                continue
            request_id = params.get("requestId")
            if request_id:
                request_ids.add(request_id)
            body = request.get("postData") or ""
            if not body and request_id:
                try:
                    data = driver.execute_cdp_cmd(
                        "Network.getRequestPostData", {"requestId": request_id}
                    )
                    body = data.get("postData") or ""
                except Exception:
                    body = ""
            add(body)
            continue
        url = (params.get("response") or {}).get("url") or params.get("url") or ""
        if SPA_EVENTS_HOST not in str(url):
            continue
        if method == "Network.responseReceived":
            try:
                hints.statuses.append(int((params.get("response") or {}).get("status") or 0))
            except (TypeError, ValueError):
                continue
        elif method == "Network.loadingFailed":
            error_text = str(params.get("errorText") or params.get("blockedReason") or "")
            if error_text:
                hints.errors.append(error_text)
    return posts, hints


def collect_events_posts(driver) -> list[SpaEventPost]:
    posts, _ = collect_events_capture(driver)
    return posts


def collect_events_post_bodies(driver) -> list[str]:
    return [item.body for item in collect_events_posts(driver)]


def page_http_status(driver) -> int:
    """HTTP-статус текущей навигации (0 если браузер не отдал)."""
    try:
        code = driver.execute_script(
            "var n = (window.performance && window.performance.getEntriesByType)"
            " ? window.performance.getEntriesByType('navigation')[0] : null;"
            "return (n && n.responseStatus) ? n.responseStatus : 0;"
        )
        return int(code or 0)
    except Exception:
        return 0


def collect_events_network_hints(driver) -> SpaEventsNetworkHints:
    """Статусы/ошибки POST spa-back/events (тот же drain, что и collect_events_posts)."""
    _, hints = collect_events_capture(driver)
    return hints


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


def _spa_back_network_fail(statuses: list[int], errors: list[str]) -> str:
    if any(code >= 500 for code in statuses):
        code = next(code for code in statuses if code >= 500)
        return f"spa-back HTTP {code}"
    joined = " ".join(errors).lower()
    if any(
        token in joined
        for token in ("timed_out", "timed out", "timeout", "net::err_", "err_connection")
    ):
        return f"spa-back timeout ({errors[0]})" if errors else "spa-back timeout"
    return ""


def assert_only_monitor_uid(
    posts: list[SpaEventPost] | list[str],
    *,
    expected: str | None = None,
    require_posts: bool = True,
    context: str = "SPA /events",
    page_status: int | None = None,
    spa_statuses: list[int] | None = None,
    spa_errors: list[str] | None = None,
) -> None:
    """Ожидаемый uid есть, чужих нет. Пустой лог классифицируем: harness vs spa-back."""
    target = (expected or spa_events_uid()).strip()
    bodies = [item.body if isinstance(item, SpaEventPost) else item for item in posts]
    uids = uids_from_posts(posts)

    if require_posts and not bodies:
        network = _spa_back_network_fail(spa_statuses or [], spa_errors or [])
        if network:
            raise SpaEventsNetworkError(f"{context}: {network} — POST /events")
        page_ok = page_status is None or page_status == 0 or 200 <= page_status < 400
        if page_ok:
            shown = page_status if page_status else 200
            raise SpaEventsHarnessError(
                f"{context}: POST /events не обнаружен "
                f"(harness: страница {shown}, сниффер пуст)"
            )
        raise SpaEventsUidError(
            f"{context}: POST /events не обнаружен (страница HTTP {page_status})"
        )
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
