"""Страница Минцифр / российские сертификаты на лендинге."""

from __future__ import annotations

from pathlib import Path

import pytest

from pages.landing_page import LandingPage
from pages.mincifry_page import MincifryPage
from tests.ui.selenium_ui.live_bid import require_live_bid

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.ui
@pytest.mark.selenium
def test_mincifry_card_click_skips_login_and_registration(driver):
    """Баннер — JS-карточка; «Войти» и /registration рядом, клик должен идти в сертификаты."""
    driver.get((FIXTURE_DIR / "mincifry_landing.html").as_uri())
    MincifryPage(driver, timeout=10).assert_full_flow()
    url = (driver.current_url or "").lower()
    assert "mincifry_certs.html" in url
    assert "openid-connect" not in url
    assert "self-authentication" not in url
    assert "/registration" not in url


@pytest.mark.ui
@pytest.mark.selenium
def test_landing_mincifry_full_flow(driver):
    require_live_bid()
    LandingPage(driver).open()
    MincifryPage(driver).assert_full_flow()
