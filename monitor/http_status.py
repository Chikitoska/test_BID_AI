"""Определение HTTP 4xx/5xx в коде ответа или тексте ошибки (URL /error/500 и т.п.)."""

from __future__ import annotations

import re

# /error/500, HTTP 502, status=503 — префикс обязателен (не ловить голые «404» в тексте UI).
_HTTP_ERROR_RE = re.compile(
    r"(?:/error/|HTTP\s+|status[=:\s])(4\d{2}|5\d{2})\b",
    re.IGNORECASE,
)
_HTTP_ERROR_WORDS = (
    "bad gateway",
    "service unavailable",
    "gateway timeout",
    "internal server error",
    "http error 4",
    "http error 5",
)


def is_http_4xx_or_5xx(*, http_code: int = 0, error: str = "") -> bool:
    """True, если это клиентская/серверная HTTP-ошибка (не UI-селектор)."""
    if 400 <= int(http_code or 0) <= 599:
        return True
    text = (error or "").strip()
    if not text:
        return False
    lower = text.lower()
    if any(word in lower for word in _HTTP_ERROR_WORDS):
        return True
    return _HTTP_ERROR_RE.search(text) is not None


def results_have_http_4xx_or_5xx(results) -> bool:
    """Есть ли среди упавших проверок подтверждённый 4xx/5xx."""
    for item in results or []:
        if getattr(item, "success", True):
            continue
        if is_http_4xx_or_5xx(
            http_code=int(getattr(item, "http_code", 0) or 0),
            error=str(getattr(item, "error", "") or ""),
        ):
            return True
    return False
