"""HTTP-проверки для backend-тестов."""

import requests

from config.settings import AUTH_URL_PATTERNS, HTTP_TIMEOUT


class HttpCheckError(AssertionError):
    pass


def assert_success_status(response: requests.Response, url: str) -> None:
    """Проверяет, что ответ 2xx (не 4xx/5xx)."""
    status = response.status_code
    if 200 <= status < 300:
        return
    raise HttpCheckError(
        f"URL {url} вернул {status}, ожидался 2xx. Body: {response.text[:300]}"
    )


def get_with_checks(url: str, session: requests.Session | None = None) -> requests.Response:
    client = session or requests
    response = client.get(url, timeout=HTTP_TIMEOUT, allow_redirects=True)
    assert_success_status(response, url)
    return response


def is_auth_related_url(url: str) -> bool:
    lower_url = url.lower()
    return any(pattern.lower() in lower_url for pattern in AUTH_URL_PATTERNS)
