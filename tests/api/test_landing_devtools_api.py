"""Расширенные API-тесты всех методов лендинга из DevTools Network."""

import pytest
import requests

from config.api_catalog import (
    CONFIG_REQUIRED_KEYS,
    EXTERNAL_LANDING_API_METHODS,
    LANDING_API_METHODS,
    LANDING_SERVICE_TAGS,
    LEGAL_DOCUMENT_NAMES,
    SERVICE_PROVIDER_REQUIRED_FIELDS,
    LandingApiMethod,
)
from config.settings import BASE_URL
from utils.http_checks import assert_success_status


def _url(api: LandingApiMethod) -> str:
    return f"{api.base.rstrip('/')}{api.path}"


@pytest.mark.api
@pytest.mark.parametrize("api_method", LANDING_API_METHODS, ids=lambda m: m.name)
def test_landing_api_method_returns_2xx(http_session, api_method: LandingApiMethod):
    """Каждый API-метод лендинга из DevTools отвечает 2xx."""
    if api_method.method != "GET":
        pytest.skip(f"Метод {api_method.method} проверяется отдельно")
    response = http_session.get(_url(api_method), timeout=30)
    assert_success_status(response, _url(api_method))


@pytest.mark.api
@pytest.mark.parametrize("api_method", EXTERNAL_LANDING_API_METHODS, ids=lambda m: m.name)
def test_external_landing_api_methods(http_session, api_method: LandingApiMethod):
    url = _url(api_method)
    if api_method.method == "GET":
        response = http_session.get(url, timeout=30)
        assert_success_status(response, url)
    elif api_method.method == "POST":
        # Формат тела: list[RegisterEventInput] (как в Network DevTools)
        payload = [{"event": "page_view", "counterId": 1212}]
        response = http_session.post(
            url,
            json=payload,
            timeout=30,
            headers={
                "Origin": BASE_URL.rstrip("/"),
                "Referer": BASE_URL,
            },
        )
        assert response.status_code < 500, (
            f"POST {url} -> {response.status_code}: {response.text[:200]}"
        )
        assert 200 <= response.status_code < 300, (
            f"POST {url} -> {response.status_code}, ожидался 2xx"
        )


@pytest.mark.api
@pytest.mark.parametrize("doc_name", LEGAL_DOCUMENT_NAMES)
def test_legal_document_by_name_returns_2xx(http_session, doc_name: str):
    """GET legal-documents/v1 для каждого документа из bulk-запроса лендинга."""
    url = (
        f"{BASE_URL.rstrip('/')}/api/gateway/global/legal-documents/v1"
        f"?filtering=name%20in%20({doc_name})%20and%20isValid%20eq%20true"
    )
    response = http_session.get(url, timeout=30)
    assert_success_status(response, url)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1, f"Документ {doc_name} не найден"
    assert data[0]["name"] == doc_name


@pytest.mark.api
@pytest.mark.parametrize("tag", LANDING_SERVICE_TAGS)
def test_service_provider_filter_by_tag_returns_2xx(http_session, tag: str):
    """Фильтрация сервис-провайдеров по тегам вкладок лендинга."""
    from urllib.parse import quote

    filtering = quote(f"tags.label eq '{tag}'")
    url = (
        f"{BASE_URL.rstrip('/')}/api/gateway/public/api/public/service-provider"
        f"?filtering={filtering}"
    )
    response = http_session.get(url, timeout=30)
    assert_success_status(response, url)
    providers = response.json()
    assert isinstance(providers, list)


@pytest.mark.api
def test_config_json_has_required_keys(http_session):
    response = http_session.get(f"{BASE_URL.rstrip('/')}/config.json", timeout=30)
    assert_success_status(response, "config.json")
    data = response.json()
    for key in CONFIG_REQUIRED_KEYS:
        assert key in data, f"В config.json отсутствует ключ {key}"


@pytest.mark.api
def test_config_json_spa_urls_match_catalog(http_session):
    response = http_session.get(f"{BASE_URL.rstrip('/')}/config.json", timeout=30)
    data = response.json()
    assert "spa-back.gazprom-neft.ru" in data["gpn_spa_counter_url"]
    assert "spa-back.gazprom-neft.ru" in data["gpn_spa_events_url"]
    assert data["gpn_spa_counter_id"] == 1212


@pytest.mark.api
def test_service_provider_items_have_required_fields(http_session):
    url = f"{BASE_URL.rstrip('/')}/api/gateway/public/api/public/service-provider"
    providers = http_session.get(url, timeout=30).json()
    assert len(providers) > 0
    for item in providers[:5]:
        for field in SERVICE_PROVIDER_REQUIRED_FIELDS:
            assert field in item, f"У сервиса {item.get('name')} нет поля {field}"


@pytest.mark.api
def test_service_provider_tags_match_landing_tabs(http_session):
    url = f"{BASE_URL.rstrip('/')}/api/gateway/public/api/public/service-provider"
    providers = http_session.get(url, timeout=30).json()
    all_tags = {
        tag["label"]
        for provider in providers
        for tag in provider.get("tags", [])
    }
    for landing_tag in LANDING_SERVICE_TAGS:
        assert landing_tag in all_tags, f"Тег вкладки '{landing_tag}' не найден в API"


@pytest.mark.api
def test_version_with_cache_buster_returns_2xx(http_session):
    """Запрос /version?k=... как в Network DevTools."""
    url = f"{BASE_URL.rstrip('/')}/version?k=1785732399863"
    response = http_session.get(url, timeout=30)
    assert_success_status(response, url)


@pytest.mark.api
def test_help_section_public_page_200(http_session):
    url = "https://lk.bid.gazprom-neft.ru/help-section"
    response = http_session.get(url, timeout=30, allow_redirects=True)
    assert_success_status(response, url)


@pytest.mark.api
def test_spa_events_get_returns_405_not_5xx(http_session):
    """GET /events — только POST (405), не 5xx."""
    url = "https://spa-back.gazprom-neft.ru/events"
    response = http_session.get(url, timeout=30)
    assert response.status_code == 405
    assert "POST" in response.headers.get("allow", "")
