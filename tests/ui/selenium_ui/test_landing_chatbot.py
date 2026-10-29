"""Чат-бот ассистент на лендинге."""

import pytest

from pages.chatbot_widget import ChatbotWidget
from pages.landing_page import LandingPage


@pytest.mark.ui
@pytest.mark.selenium
def test_landing_chatbot_full_flow(landing_page: LandingPage):
    ChatbotWidget(landing_page.driver).assert_interactive(context="Лендинг")
