"""Fixtures Playwright для UI-тестов."""

import pytest
from playwright.sync_api import Page, sync_playwright


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser) -> Page:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU",
    )
    page = context.new_page()
    yield page
    context.close()
