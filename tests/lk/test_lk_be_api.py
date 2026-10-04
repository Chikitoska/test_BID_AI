"""BE API smoke ЛК: один FE-логин → токен → GET polling (ожидаем HTTP 200).

Маркер: ``lk_be`` (также ``lk``, ``api``, ``smoke``).

Запуск локально::

    .venv/bin/pytest -m lk_be tests/lk/test_lk_be_api.py -v

Входит в ``monitor/run_lk_pytest.py`` (весь ``tests/lk/``).
В ``run_daily`` (``tests/api/``) **не** подключён — нужен Chrome + TOTP;
подключить позже: ``pytest -m lk_be`` или отдельный путь в daily.
"""

from __future__ import annotations

import pytest
import requests

from config.lk_be_api_catalog import (
    LK_BE_ACTIVE_ENDPOINTS,
    LK_BE_SKIPPED_ENDPOINTS,
    LK_ORIGIN,
    LkBeEndpoint,
)
from config.settings import HTTP_TIMEOUT
from pages.lk_flow import LkFlow
from pages.lk_page import LkPage
from utils.lk_auth_token import (
    LkAuthMaterial,
    apply_lk_auth,
    dump_auth_debug,
    extract_lk_auth,
)

pytestmark = [
    pytest.mark.lk,
    pytest.mark.lk_be,
    pytest.mark.api,
    pytest.mark.smoke,
]


class LkBeApiClient:
    """requests-клиент с одноразовым refresh auth при 401."""

    def __init__(self, driver, session: requests.Session, material: LkAuthMaterial):
        self.driver = driver
        self.session = session
        self.material = material
        self._refreshed = False
        apply_lk_auth(self.session, self.material)

    def refresh_auth(self, *, re_login: bool = False) -> None:
        if re_login:
            print("[lk_be] re-login after 401…", flush=True)
            LkFlow(self.driver).login()
            page = LkPage(self.driver)
            page.dismiss_consent_modals()
            page.wait_ready()
        self.material = extract_lk_auth(self.driver)
        if not self.material.has_auth:
            raise AssertionError(
                "После refresh нет cookie/Bearer для ЛК API: "
                + dump_auth_debug(self.material)
            )
        apply_lk_auth(self.session, self.material)

    def request(self, method: str, url: str) -> requests.Response:
        response = self.session.request(
            method.upper(),
            url,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        if response.status_code != 401 or self._refreshed:
            return response
        self._refreshed = True
        print(f"[lk_be] 401 on {method} {url} → refresh auth once", flush=True)
        try:
            self.refresh_auth(re_login=False)
            response = self.session.request(
                method.upper(),
                url,
                timeout=HTTP_TIMEOUT,
                allow_redirects=True,
            )
            if response.status_code != 401:
                return response
            self.refresh_auth(re_login=True)
            return self.session.request(
                method.upper(),
                url,
                timeout=HTTP_TIMEOUT,
                allow_redirects=True,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[lk_be] refresh failed: {exc}", flush=True)
            return response


@pytest.fixture(scope="module")
def lk_be_api_client(lk_driver) -> LkBeApiClient:
    """Один логин на модуль (через session ``lk_driver``) → HTTP client."""
    driver = lk_driver
    # Убеждаемся, что вкладка на домене ЛК — иначе storage/cookies пустые.
    if LK_ORIGIN.split("://", 1)[-1] not in (driver.current_url or ""):
        driver.get(f"{LK_ORIGIN}/service-providers")
    page = LkPage(driver)
    page.dismiss_consent_modals()
    page.wait_ready()

    material = extract_lk_auth(driver)
    assert material.has_auth, (
        "Не удалось извлечь cookie/Bearer после логина в ЛК. "
        f"debug={dump_auth_debug(material)}"
    )

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9",
            "Referer": f"{LK_ORIGIN}/",
            "Origin": LK_ORIGIN,
        }
    )
    client = LkBeApiClient(driver, session, material)
    yield client
    session.close()


@pytest.mark.parametrize(
    "endpoint",
    LK_BE_ACTIVE_ENDPOINTS,
    ids=lambda ep: ep.name,
)
def test_lk_be_endpoint_returns_200(lk_be_api_client: LkBeApiClient, endpoint: LkBeEndpoint):
    response = lk_be_api_client.request(endpoint.method, endpoint.url)
    assert response.status_code == endpoint.expect_status, (
        f"{endpoint.method} {endpoint.url} → {response.status_code}, "
        f"ожидался {endpoint.expect_status}. Body: {response.text[:300]}"
    )


@pytest.mark.parametrize(
    "endpoint",
    LK_BE_SKIPPED_ENDPOINTS,
    ids=lambda ep: ep.name,
)
def test_lk_be_endpoint_deferred(endpoint: LkBeEndpoint):
    """Каталог: GOST / archived ACL / analytics POST — пока вне daily green path."""
    pytest.skip(endpoint.skip_reason or "deferred")
