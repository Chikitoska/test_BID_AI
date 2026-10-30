"""Чат-бот ассистент на лендинге."""

from __future__ import annotations

from pathlib import Path

import pytest

from pages.chatbot_widget import ChatbotWidget
from pages.landing_page import LandingPage
from tests.ui.selenium_ui.live_bid import require_live_bid

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.ui
@pytest.mark.selenium
def test_landing_chatbot_skips_login_and_registration(driver):
    """Иконка ассистента рядом с «Войти» / «Получить ID» — клик только в виджет."""
    driver.get((FIXTURE_DIR / "chatbot_landing.html").as_uri())
    ChatbotWidget(driver, timeout=10).assert_interactive(context="Лендинг")
    url = (driver.current_url or "").lower()
    assert "openid-connect" not in url
    assert "self-authentication" not in url
    assert "/registration" not in url
    assert "chatbot_landing.html" in url


@pytest.mark.ui
@pytest.mark.selenium
def test_landing_chatbot_full_flow(landing_page: LandingPage):
    require_live_bid()
    ChatbotWidget(landing_page.driver).assert_interactive(context="Лендинг")
