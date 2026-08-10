"""Fixtures Selenium UI-тестов."""

import pytest


@pytest.fixture(scope="function")
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    from config.settings import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

    service = ChromeService(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    browser.implicitly_wait(IMPLICIT_WAIT)
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Performance.enable", {})

    yield browser

    browser.quit()


@pytest.fixture(scope="function")
def landing_page(driver):
    from pages.landing_page import LandingPage

    return LandingPage(driver).open()
