"""Классификация хоста BID: лендинг vs spa-back vs ЛК.

spa-back timeout не должен выглядеть как «лендинг лежит».
"""

from __future__ import annotations

import re
from typing import Literal
from urllib.parse import urlparse

HostKind = Literal["landing", "spa-back", "lk", "unknown"]

_URL_RE = re.compile(r"https?://[^\s\]\)\"'>,|;]+")


def classify_bid_host(url_or_text: str) -> HostKind:
    """landing | spa-back | lk | unknown — по URL или тексту ошибки."""
    text = (url_or_text or "").lower()
    if not text.strip():
        return "unknown"
    if "spa-back.gazprom-neft.ru" in text:
        return "spa-back"
    if any(token in text for token in ("lk.bid.", "processor.gazprom", "processor.bid")):
        return "lk"
    if any(token in text for token in ("id.bid.", "openid-connect", "keycloak")):
        return "lk"
    if "bid.gazprom-neft.ru" in text:
        return "landing"
    return "unknown"


def host_from_url(url: str) -> str:
    """Короткое имя хоста без www, либо пустая строка."""
    raw = (url or "").strip()
    if not raw:
        return ""
    if "://" not in raw:
        raw = "https://" + raw
    try:
        parsed = urlparse(raw)
    except ValueError:
        return ""
    return (parsed.hostname or "").lower()


def extract_http_code(text: str) -> int | None:
    raw = text or ""
    match = re.search(r"\bHTTP\s*([1-5]\d{2})\b", raw, flags=re.I)
    if match:
        return int(match.group(1))
    match = re.search(r"/error/([1-5]\d{2})\b", raw, flags=re.I)
    if match:
        return int(match.group(1))
    match = re.search(r"\b([1-5]\d{2})\s+(?:Bad Gateway|Not Found|Forbidden|Gateway|Internal)", raw)
    if match:
        return int(match.group(1))
    return None


def is_timeout_text(text: str) -> bool:
    lower = (text or "").lower()
    return any(
        token in lower
        for token in (
            "timed out",
            "timeout",
            "timeoutexception",
            "read timed out",
            "connecttimeout",
            "gateway time-out",
            "err_timed_out",
        )
    )


def short_network_kind(text: str) -> str:
    """timeout | dns | refused | http | network."""
    lower = (text or "").lower()
    if is_timeout_text(lower):
        return "timeout"
    if any(token in lower for token in ("nameresolution", "name or service not known", "dns")):
        return "dns"
    if "refused" in lower:
        return "refused"
    if extract_http_code(text):
        return "http"
    return "network"


def format_host_error(
    *,
    url: str = "",
    error: str = "",
    http_code: int = 0,
    method: str = "GET",
) -> str:
    """Короткое сообщение: «spa-back timeout: host — …», без дампа urllib3/Selenium."""
    host_kind = classify_bid_host(url or error)
    host = host_from_url(url)
    code = http_code or extract_http_code(error) or 0
    kind = short_network_kind(error)
    if code:
        kind = f"HTTP {code}"
    elif kind == "http" and not code:
        kind = "HTTP"
    prefix = host_kind if host_kind != "unknown" else (host or "host")
    where = host or url or ""
    if where:
        return f"{prefix} {kind}: {where}"
    return f"{prefix} {kind}"


def first_url(text: str) -> str:
    match = _URL_RE.search(text or "")
    return match.group(0).rstrip(".,;:)") if match else ""
