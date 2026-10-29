"""Проверка целевых ссылок виджетов (Минцифры / чат-бот)."""

from __future__ import annotations

import re

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


def normalize_page_text(text: str | None) -> str:
    """Сжать пробелы и пунктуацию: «Яндекс.\\xa0Браузер» → «яндекс браузер»."""
    raw = (text or "").lower().replace("ё", "е")
    raw = re.sub(r"[\s\u00a0\u202f\u2007\u2009\u200a\u200b]+", " ", raw)
    raw = re.sub(r"[«»\"'`()\[\].,;:!?/\\|_+*=~-]+", " ", raw)
    return " ".join(raw.split())


def mentions_yandex_browser(text: str | None) -> bool:
    normalized = normalize_page_text(text)
    if "яндекс" in normalized and "браузер" in normalized:
        return True
    if "yandex" in normalized and "browser" in normalized:
        return True
    return False


def is_login_target(url: str | None) -> bool:
    """Войти / регистрация / Keycloak — не страница сертификатов Минцифры."""
    href = (url or "").lower()
    return any(
        token in href
        for token in (
            "openid-connect",
            "self-authentication",
            "id.bid.gazprom-neft.ru",
            "/login",
            "/registration",
            "keycloak",
        )
    )


def is_certs_href(url: str | None) -> bool:
    """Только URL страницы сертификатов, не «Войти» и не регистрация."""
    href = (url or "").lower()
    if not href or is_login_target(href) or is_blank_target(href):
        return False
    return any(
        token in href
        for token in (
            "gosuslugi.ru/crt",
            "/certs",
            "/crt",
            "certificate",
            "mincifry",
            "mintsifr",
            "сертификат",
        )
    )


def is_certs_target(url: str | None, text: str | None = None) -> bool:
    if is_certs_href(url):
        return True
    label = " ".join((text or "").split())
    if len(label) > 120 or is_login_target(label):
        return False
    lower = label.lower()
    if any(s in lower for s in ("войти", "регистрац", "получить id", "получить идентификатор")):
        return False
    return any(s in lower for s in ("сертификат", "минцифр"))


def is_yandex_browser_href(url: str | None) -> bool:
    href = (url or "").lower()
    return any(
        token in href
        for token in (
            "browser.yandex",
            "yandex.ru/download",
            "ya.ru/browser",
            "browser.yandex.ru",
        )
    )
