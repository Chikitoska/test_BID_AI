"""Единый SPA UUID мониторинга для cookie и POST spa-back/events."""

from __future__ import annotations

import json
import os
from typing import Any

DEFAULT_MONITOR_ANALYTICS_UID = "b1d00000-0000-4000-a000-000000000001"
DEFAULT_SPA_USER_ID_COOKIE_KEY = "gpn_spa_custom_user_id_cookie"
SPA_EVENTS_COUNTER_ID = 1212
SPA_EVENTS_HOST = "spa-back.gazprom-neft.ru/events"
UID_KEYS = ("uid", "customUserId", "custom_user_id", "userId")
_UID_KEYS = UID_KEYS


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
            if obj.get("as_user_id"):
                extra = obj.get("value")
                if extra:
                    found.append(str(extra))
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(payload)
    return found


def extract_uids_from_events_body(post_data: str) -> list[str]:
    payload = _parse_events_body(post_data)
    if payload is None:
        return []
    return extract_uids_from_events_payload(payload)


def extract_event_names_from_events_payload(payload: Any) -> list[str]:
    names: list[str] = []

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            event = obj.get("event")
            component_id = obj.get("componentid")
            consta_type = obj.get("constaeventtype")
            event_type = obj.get("eventType")
            if event not in (None, ""):
                names.append(str(event))
            elif component_id not in (None, ""):
                label = str(component_id)
                if consta_type not in (None, "", "undefined"):
                    label = f"{label}:{consta_type}"
                names.append(label)
            elif consta_type not in (None, "", "undefined"):
                names.append(str(consta_type))
            elif event_type not in (None, ""):
                names.append(f"eventType:{event_type}")
            for child in obj.values():
                walk(child)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(payload)
    return names


def extract_event_names_from_events_body(post_data: str) -> list[str]:
    payload = _parse_events_body(post_data)
    if payload is None:
        return []
    return extract_event_names_from_events_payload(payload)


def stamp_events_uid_in_payload(payload: Any, uid: str | None = None) -> Any:
    """Подставить MONITOR_ANALYTICS_UID во все uid-поля (и добавить uid, если его нет)."""
    target = (uid or spa_events_uid()).strip()

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            event_like = "event" in obj or "counterId" in obj
            touched = False
            for key in _UID_KEYS:
                value = obj.get(key)
                if value not in (None, ""):
                    obj[key] = target
                    touched = True
            if event_like or touched:
                obj["uid"] = target
            if obj.get("as_user_id") and obj.get("value") not in (None, ""):
                obj["value"] = target
            for child in obj.values():
                walk(child)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(payload)
    return payload


def stamp_events_uid_in_body(post_data: str, uid: str | None = None) -> str:
    payload = _parse_events_body(post_data)
    if payload is None:
        return post_data
    stamp_events_uid_in_payload(payload, uid)
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def events_uid_rewrite_js(uid: str | None = None) -> str:
    """Патч fetch/XHR/sendBeacon: uid в POST /events всегда MONITOR_ANALYTICS_UID."""
    target = (uid or spa_events_uid()).strip()
    return (
        "(function () {\n"
        f"  var uid = {json.dumps(target)};\n"
        f"  var host = {json.dumps(SPA_EVENTS_HOST)};\n"
        f"  var keys = {json.dumps(list(_UID_KEYS))};\n"
        "  function isEventsUrl(url) {\n"
        "    return String(url || '').indexOf(host) !== -1;\n"
        "  }\n"
        "  function stamp(obj) {\n"
        "    if (Array.isArray(obj)) {\n"
        "      for (var i = 0; i < obj.length; i++) stamp(obj[i]);\n"
        "      return obj;\n"
        "    }\n"
        "    if (obj && typeof obj === 'object') {\n"
        "      var eventLike = Object.prototype.hasOwnProperty.call(obj, 'event')\n"
        "        || Object.prototype.hasOwnProperty.call(obj, 'counterId');\n"
        "      var touched = false;\n"
        "      for (var k = 0; k < keys.length; k++) {\n"
        "        var key = keys[k];\n"
        "        if (obj[key] !== undefined && obj[key] !== null && obj[key] !== '') {\n"
        "          obj[key] = uid;\n"
        "          touched = true;\n"
        "        }\n"
        "      }\n"
        "      if (eventLike || touched) obj.uid = uid;\n"
        "      if (obj.as_user_id && obj.value !== undefined && obj.value !== null && obj.value !== '') {\n"
        "        obj.value = uid;\n"
        "      }\n"
        "      var names = Object.keys(obj);\n"
        "      for (var j = 0; j < names.length; j++) stamp(obj[names[j]]);\n"
        "    }\n"
        "    return obj;\n"
        "  }\n"
        "  function rewriteBody(body) {\n"
        "    if (body == null) return body;\n"
        "    try {\n"
        "      if (typeof body === 'string') {\n"
        "        var parsed = JSON.parse(body);\n"
        "        stamp(parsed);\n"
        "        return JSON.stringify(parsed);\n"
        "      }\n"
        "    } catch (e) {}\n"
        "    return body;\n"
        "  }\n"
        "  try {\n"
        "    var origFetch = window.fetch;\n"
        "    if (origFetch) {\n"
        "      window.fetch = function (input, init) {\n"
        "        try {\n"
        "          var url = (typeof input === 'string') ? input : (input && input.url);\n"
        "          if (isEventsUrl(url) && init && init.body != null) {\n"
        "            var copy = Object.assign({}, init);\n"
        "            copy.body = rewriteBody(init.body);\n"
        "            return origFetch.call(this, input, copy);\n"
        "          }\n"
        "        } catch (e) {}\n"
        "        return origFetch.apply(this, arguments);\n"
        "      };\n"
        "    }\n"
        "  } catch (e) {}\n"
        "  try {\n"
        "    var origOpen = XMLHttpRequest.prototype.open;\n"
        "    var origSend = XMLHttpRequest.prototype.send;\n"
        "    XMLHttpRequest.prototype.open = function (method, url) {\n"
        "      try { this.__gpnSpaEvents = isEventsUrl(url); } catch (e) {}\n"
        "      return origOpen.apply(this, arguments);\n"
        "    };\n"
        "    XMLHttpRequest.prototype.send = function (body) {\n"
        "      try { if (this.__gpnSpaEvents) body = rewriteBody(body); } catch (e) {}\n"
        "      return origSend.call(this, body);\n"
        "    };\n"
        "  } catch (e) {}\n"
        "  try {\n"
        "    if (navigator.sendBeacon) {\n"
        "      var origBeacon = navigator.sendBeacon.bind(navigator);\n"
        "      navigator.sendBeacon = function (url, data) {\n"
        "        try { if (isEventsUrl(url)) data = rewriteBody(data); } catch (e) {}\n"
        "        return origBeacon(url, data);\n"
        "      };\n"
        "    }\n"
        "  } catch (e) {}\n"
        "})();"
    )


def _parse_events_body(post_data: str) -> Any | None:
    if not post_data:
        return None
    try:
        return json.loads(post_data)
    except json.JSONDecodeError:
        return None
