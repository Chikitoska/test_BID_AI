"""Проверка целевых ссылок виджетов (Минцифры / чат-бот)."""

from __future__ import annotations

_BLANK = {
    "",
    "#",
    "about:blank",
    "about:blank#blocked",
    "javascript:void(0)",
    "javascript:void(0);",
    "javascript:;",
    "javascript:void 0",
}


def is_blank_target(url: str | None) -> bool:
    raw = (url or "").strip()
    if not raw:
        return True
    lower = raw.lower()
    if lower in _BLANK:
        return True
    if lower.startswith("javascript:"):
        return True
    return False
