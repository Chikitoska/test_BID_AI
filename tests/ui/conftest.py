"""Fixtures Selenium UI-тестов."""

from pathlib import Path

import pytest
from selenium.common.exceptions import WebDriverException

from monitor.load_env import load_project_env

# Как tests/lk/conftest.py: .env до импорта фабрики (MONITOR_HEADLESS, CHROME_BINARY).
load_project_env(Path(__file__).resolve().parents[2])


@pytest.fixture(scope="function")
def driver():
    """Тот же Chrome, что у ЛК/health: headless на VPS, system chromedriver, retry.

    Старый путь (ChromeDriverManager + maximize без --headless) на сервере без DISPLAY
    даёт SessionNotCreatedException: Chrome instance exited — в т.ч. на локальных HTML-фикстурах.
    """
    from config.settings import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT
    from utils.selenium_factory import create_chrome_driver

    browser = create_chrome_driver(enable_performance_log=True)
    browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    browser.implicitly_wait(IMPLICIT_WAIT)
    try:
        yield browser
    finally:
        try:
            browser.quit()
        except WebDriverException:
            pass


@pytest.fixture(scope="function")
def landing_page(driver):
    from pages.landing_page import LandingPage

    return LandingPage(driver).open()
