"""Фильтрация URL авторизации из backend-проверок."""

from config.settings import AUTH_URL_PATTERNS


def is_auth_url(url: str) -> bool:
    """True, если URL относится к авторизации (Войти / Keycloak / OIDC)."""
    lower_url = url.lower()
    return any(pattern.lower() in lower_url for pattern in AUTH_URL_PATTERNS)


def filter_non_auth_urls(urls: list[str]) -> list[str]:
    return [url for url in urls if not is_auth_url(url)]
