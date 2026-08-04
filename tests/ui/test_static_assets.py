"""Проверка статических ресурсов и производительности."""

import pytest
import requests

from pages.landing_page import LandingPage
from utils.auth_filter import is_auth_url
from utils.http_checks import assert_success_status


@pytest.mark.ui
@pytest.mark.parametrize("min_assets", [3])
def test_page_static_assets_return_200(http_session, landing_page: LandingPage, min_assets: int):
    asset_urls = landing_page.get_static_asset_urls()
    bid_assets = [u for u in asset_urls if "bid.gazprom-neft.ru" in u and not is_auth_url(u)]
    assert len(bid_assets) >= min_assets

    for url in bid_assets[:10]:
        response = http_session.get(url, timeout=30)
        assert_success_status(response, url)


@pytest.mark.ui
def test_page_load_time_under_threshold(landing_page: LandingPage):
    timing = landing_page.driver.execute_script(
        "return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart"
    )
    assert timing > 0, "Не удалось измерить время загрузки"
    assert timing < 60000, f"Страница грузится слишком долго: {timing} ms"
