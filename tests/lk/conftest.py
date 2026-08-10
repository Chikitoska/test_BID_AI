"""Fixtures для тестов ЛК."""

from __future__ import annotations

import pytest

from config.lk_settings import LK_CREDENTIALS_SET, MONITOR_HEADLESS
from pages.lk_flow import LkFlow
from utils.selenium_factory import create_chrome_driver

pytestmark = pytest.mark.skipif(
    not LK_CREDENTIALS_SET,
    reason="Задайте BID_USERNAME, BID_PASSWORD, BID_TOTP_SECRET",
)


@pytest.fixture(scope="module")
def authenticated_driver():
    driver = create_chrome_driver(headless=MONITOR_HEADLESS)
    flow = LkFlow(driver)
    flow.login_from_landing()
    flow.wait_for_lk_redirect()
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def processor_driver(authenticated_driver):
    LkFlow(authenticated_driver).open_service_provider()
    return authenticated_driver
