"""Чат-бот ассистент на лендинге."""

from __future__ import annotations

import socket
from pathlib import Path

import pytest

from pages.chatbot_widget import ChatbotWidget
from pages.landing_page import LandingPage

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def _bid_tcp_ok(timeout: float = 5) -> bool:
    try:
        with socket.create_connection(("bid.gazprom-neft.ru", 443), timeout=timeout):
            return True
    except OSError:
        return False


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
    if not _bid_tcp_ok():
        pytest.skip(
            "BID недоступен с этой машины (TCP :443 timeout) — живой прогон лендинга пропущен"
        )
    ChatbotWidget(landing_page.driver).assert_interactive(context="Лендинг")
