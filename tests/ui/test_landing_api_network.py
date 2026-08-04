"""Динамический сбор API из Network log браузера при загрузке лендинга."""

import pytest

from pages.landing_page import LandingPage
from utils.auth_filter import is_auth_url
from utils.network_monitor import collect_network_responses


def _is_api_request(url: str) -> bool:
    api_markers = (
        "/api/",
        "/config.json",
        "/version",
        "spa-back.gazprom-neft.ru/events",
        "spa-back.gazprom-neft.ru/static/",
    )
    return any(marker in url for marker in api_markers)


@pytest.mark.api
@pytest.mark.network
@pytest.mark.ui
def test_all_landing_api_from_devtools_return_success(landing_page: LandingPage):
    """
    Собирает все API-запросы из Network log Chrome при загрузке лендинга
    и проверяет 2xx/3xx (кроме auth URL).
    """
    responses = collect_network_responses(landing_page.driver)
    api_responses = [
        r for r in responses
        if _is_api_request(r["url"]) and not is_auth_url(r["url"])
    ]

    if not api_responses:
        pytest.skip("Network log пуст — проверяем через статический каталог API")

    failed = [
        r for r in api_responses
        if not (200 <= r["status"] < 400)
    ]
    assert not failed, (
        "API из DevTools с ошибками:\n"
        + "\n".join(f"{i['status']} {i['url']}" for i in failed[:20])
    )


@pytest.mark.api
@pytest.mark.network
@pytest.mark.ui
def test_devtools_contains_core_landing_apis(landing_page: LandingPage):
    """На лендинге вызываются ключевые API из DevTools."""
    responses = collect_network_responses(landing_page.driver)
    urls = [r["url"] for r in responses]

    expected_fragments = [
        "/config.json",
        "/api/gateway/public/api/public/service-provider",
        "/api/gateway/global/legal-documents/v1",
        "/version",
    ]
    for fragment in expected_fragments:
        assert any(fragment in url for url in urls), (
            f"API {fragment} не найден в Network log"
        )
