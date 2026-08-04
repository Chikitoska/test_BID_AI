"""Backend-тесты публичных эндпоинтов BID (без авторизации)."""

import pytest
import requests

from config.settings import BASE_URL, PUBLIC_API_ENDPOINTS, PUBLIC_EXTERNAL_URLS
from utils.auth_filter import is_auth_url
from utils.http_checks import assert_success_status, get_with_checks


@pytest.mark.api
@pytest.mark.smoke
def test_main_page_returns_200(http_session):
    response = http_session.get(BASE_URL, timeout=30)
    assert_success_status(response, BASE_URL)


@pytest.mark.api
@pytest.mark.parametrize("endpoint", PUBLIC_API_ENDPOINTS)
def test_public_api_endpoint_returns_2xx(http_session, endpoint: str):
    url = f"{BASE_URL.rstrip('/')}{endpoint}" if endpoint.startswith("/") else endpoint
    get_with_checks(url, session=http_session)


@pytest.mark.api
@pytest.mark.parametrize("url", PUBLIC_EXTERNAL_URLS)
def test_external_public_assets_return_2xx(http_session, url: str):
    get_with_checks(url, session=http_session)


@pytest.mark.api
def test_config_json_is_valid_json(http_session):
    url = f"{BASE_URL.rstrip('/')}/config.json"
    response = get_with_checks(url, session=http_session)
    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.api
def test_service_provider_api_returns_json(http_session):
    url = f"{BASE_URL.rstrip('/')}/api/gateway/public/api/public/service-provider"
    response = get_with_checks(url, session=http_session)
    data = response.json()
    assert data is not None


@pytest.mark.api
def test_legal_documents_api_returns_json(http_session):
    url = (
        f"{BASE_URL.rstrip('/')}/api/gateway/global/legal-documents/v1"
        "?filtering=name%20in%20(BID_Agreement_processing_of_personal_data)"
        "%20and%20isValid%20eq%20true"
    )
    response = get_with_checks(url, session=http_session)
    assert response.headers.get("content-type", "").startswith("application/json")


@pytest.mark.api
def test_registration_page_not_auth_endpoint(http_session):
    """Страница «Получить ID» — не Keycloak, должна открываться без 5xx."""
    url = "https://lk.bid.gazprom-neft.ru/registration"
    response = http_session.get(url, timeout=30, allow_redirects=True)
    assert response.status_code < 500, f"Registration page error: {response.status_code}"


@pytest.mark.api
def test_auth_login_url_is_excluded_from_success_checks(http_session):
    """URL «Войти» (Keycloak) исключён из обязательных 200-проверок."""
    auth_url = (
        "https://id.bid.gazprom-neft.ru/realms/ecoportal/protocol/openid-connect/auth"
        "?client_id=self-authentication"
    )
    assert is_auth_url(auth_url)
    response = http_session.get(auth_url, timeout=30, allow_redirects=True)
    # Без credentials может быть 400/401/302 — это нормально, главное не 5xx
    assert response.status_code < 500


@pytest.mark.api
def test_no_5xx_on_public_endpoints(http_session):
    """Сводная проверка: все публичные URL без 5xx."""
    urls = [BASE_URL] + [f"{BASE_URL.rstrip('/')}{ep}" for ep in PUBLIC_API_ENDPOINTS]
    urls.extend(PUBLIC_EXTERNAL_URLS)

    for url in urls:
        if is_auth_url(url):
            continue
        response = http_session.get(url, timeout=30, allow_redirects=True)
        assert response.status_code < 500, f"{url} -> {response.status_code}"
