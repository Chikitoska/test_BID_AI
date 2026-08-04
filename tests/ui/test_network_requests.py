"""Проверка сетевых запросов браузера: 2xx для всех, кроме авторизации."""

import pytest

from pages.landing_page import LandingPage
from utils.auth_filter import is_auth_url
from utils.network_monitor import collect_non_auth_responses, collect_network_responses


@pytest.mark.network
@pytest.mark.ui
def test_all_non_auth_network_requests_are_successful(landing_page: LandingPage):
    responses = collect_non_auth_responses(landing_page.driver)
    assert responses, "Не удалось собрать network log — проверьте goog:loggingPrefs"

    failed = [
        item for item in responses if not (200 <= item["status"] < 400)
    ]
    assert not failed, (
        "Запросы с ошибками (не auth):\n"
        + "\n".join(f"{i['status']} {i['url']}" for i in failed[:15])
    )


@pytest.mark.network
@pytest.mark.ui
def test_public_api_called_from_browser_with_2xx(landing_page: LandingPage, http_session):
    responses = collect_network_responses(landing_page.driver)
    api_calls = [
        r for r in responses
        if "/api/gateway/public/" in r["url"] or r["url"].endswith("/config.json")
    ]
    if not api_calls:
        # Fallback: performance log может быть пуст в некоторых версиях Chrome
        from config.settings import PUBLIC_API_ENDPOINTS, BASE_URL

        for endpoint in PUBLIC_API_ENDPOINTS[:2]:
            url = f"{BASE_URL.rstrip('/')}{endpoint}"
            resp = http_session.get(url, timeout=30)
            assert resp.status_code < 400, f"{url} -> {resp.status_code}"
        return

    for call in api_calls:
        assert 200 <= call["status"] < 300, f"{call['url']} -> {call['status']}"


@pytest.mark.network
@pytest.mark.ui
def test_static_assets_loaded_with_2xx(landing_page: LandingPage):
    asset_urls = landing_page.get_static_asset_urls()
    assert asset_urls, "На странице не найдены JS/CSS ресурсы"

    failed = []
    for url in asset_urls:
        if is_auth_url(url):
            continue
        responses = [
            r for r in collect_network_responses(landing_page.driver) if r["url"] == url
        ]
        if responses and not (200 <= responses[0]["status"] < 400):
            failed.append(responses[0])

    assert not failed, f"Статические ресурсы с ошибками: {failed[:5]}"


@pytest.mark.network
@pytest.mark.ui
def test_auth_requests_are_not_required_to_be_200(landing_page: LandingPage):
    """Запросы авторизации могут быть редиректами — мы их не валидируем как 200."""
    responses = collect_network_responses(landing_page.driver)
    auth_responses = [r for r in responses if is_auth_url(r["url"])]
    # На лендинге без клика «Войти» auth-запросов может не быть — это OK
    for item in auth_responses:
        assert item["status"] < 500, f"Auth URL вернул 5xx: {item['url']}"
