"""Страница Минцифр / российские сертификаты на лендинге."""

from __future__ import annotations

import socket
from pathlib import Path

import pytest

from pages.landing_page import LandingPage
from pages.mincifry_page import MincifryPage

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def _bid_tcp_ok(timeout: float = 5) -> bool:
    try:
        with socket.create_connection(("bid.gazprom-neft.ru", 443), timeout=timeout):
            return True
    except OSError:
        return False


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
    if not _bid_tcp_ok():
        pytest.skip(
            "BID недоступен с этой машины (TCP :443 timeout) — живой прогон лендинга пропущен"
        )
    LandingPage(driver).open()
    MincifryPage(driver).assert_full_flow()
