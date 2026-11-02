"""Fixtures Selenium UI-тестов.

На VPS (combat pytest) тот же Chrome, что и у монитора: CHROME_BINARY / GOST,
а не ChromeDriverManager (из‑за него SessionNotCreated: Chrome instance exited).

Пока жива сессия ЛК (session-scoped lk_driver) второй Chrome не стартуем:
чат-бот/Минцифр лендинга уже в health/daily; повторный браузер в combat
ломает сессию (SessionNotCreated).
"""

from __future__ import annotations

import os

import pytest
from selenium.common.exceptions import WebDriverException

from utils.selenium_factory import create_chrome_driver, quit_chrome_driver


def _lk_session_alive() -> bool:
    return os.getenv("BID_LK_SESSION_ALIVE", "").lower() in ("1", "true", "yes")


@pytest.fixture(scope="function")
def driver():
    if _lk_session_alive():
        pytest.skip(
            "Второй Chrome не стартуем: сессия ЛК уже жива. "
            "Чат-бот и Минцифр лендинга покрыты health/daily; "
            "повторный Chrome в боевом pytest даёт SessionNotCreated."
        )
    browser = create_chrome_driver(enable_performance_log=True)
    try:
        yield browser
    finally:
        try:
            quit_chrome_driver(browser)
        except WebDriverException:
            pass


@pytest.fixture(scope="function")
def landing_page(driver):
    from pages.landing_page import LandingPage

    return LandingPage(driver).open()
