"""Fixtures Selenium UI-тестов.

На VPS (combat pytest) тот же Chrome, что и у монитора: CHROME_BINARY / GOST,
а не ChromeDriverManager (из‑за него SessionNotCreated: Chrome instance exited).
"""

from __future__ import annotations

import pytest
from selenium.common.exceptions import WebDriverException

from utils.selenium_factory import create_chrome_driver


@pytest.fixture(scope="function")
def driver():
    browser = create_chrome_driver(enable_performance_log=True)
    yield browser
    try:
        browser.quit()
    except WebDriverException:
        pass


@pytest.fixture(scope="function")
def landing_page(driver):
    from pages.landing_page import LandingPage

    return LandingPage(driver).open()
