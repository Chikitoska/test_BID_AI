"""Чат-бот ассистент в ЛК (боевой pytest каждые 2 ч + health каждые 5 мин)."""

from pages.chatbot_widget import ChatbotWidget
from pages.lk_page import LkPage


def test_lk_chatbot_full_flow(lk_page: LkPage):
    ChatbotWidget(lk_page.driver).assert_interactive(context="ЛК")
