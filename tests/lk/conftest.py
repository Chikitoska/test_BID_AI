"""Fixtures для тестов ЛК."""

from __future__ import annotations

import time
from pathlib import Path

from monitor.load_env import load_project_env

# .env должен загрузиться до импорта lk_settings (значения читаются при import).
load_project_env(Path(__file__).resolve().parents[2])

import pytest
from selenium.common.exceptions import WebDriverException

try:
    import allure
except ImportError:
    allure = None

from config.lk_settings import BID_LK_EXPECTED_URL, LK_CREDENTIALS_SET, MONITOR_HEADLESS
from pages.lk_flow import LkAuthError, LkFlow
from pages.lk_page import LkPage
from utils.selenium_factory import create_chrome_driver

pytestmark = pytest.mark.skipif(
    not LK_CREDENTIALS_SET,
    reason="Задайте BID_USERNAME, BID_PASSWORD, BID_TOTP_SECRET",
)

LK_LOGIN_ATTEMPTS = 3
LK_LOGIN_RETRY_DELAY_SEC = 5


def _login_with_retries(*, headless: bool):
    last_error: Exception | None = None
    driver = None
    for attempt in range(1, LK_LOGIN_ATTEMPTS + 1):
        if driver is not None:
            try:
                driver.quit()
            except WebDriverException:
                pass
        driver = create_chrome_driver(headless=headless)
        flow = LkFlow(driver)
        try:
            flow.login()
            print(f"[lk] вход выполнен (попытка {attempt}/{LK_LOGIN_ATTEMPTS})", flush=True)
            return driver
        except (LkAuthError, WebDriverException) as exc:
            last_error = exc
            print(
                f"[lk] вход не удался ({attempt}/{LK_LOGIN_ATTEMPTS}): {exc}",
                flush=True,
            )
            if attempt < LK_LOGIN_ATTEMPTS:
                time.sleep(LK_LOGIN_RETRY_DELAY_SEC)
    assert driver is not None
    assert last_error is not None
    raise last_error


@pytest.fixture(scope="session")
def lk_driver():
    driver = _login_with_retries(headless=MONITOR_HEADLESS)
    yield driver
    try:
        driver.quit()
    except WebDriverException:
        pass


@pytest.fixture(scope="function")
def authenticated_driver(lk_driver):
    main_window = lk_driver.window_handles[0]
    for handle in lk_driver.window_handles[1:]:
        lk_driver.switch_to.window(handle)
        lk_driver.close()
    lk_driver.switch_to.window(main_window)
    page = LkPage(lk_driver)
    if BID_LK_EXPECTED_URL not in lk_driver.current_url:
        lk_driver.get(BID_LK_EXPECTED_URL)
    page.dismiss_consent_modals()
    page.wait_ready()
    return lk_driver


@pytest.fixture(scope="function")
def lk_page(authenticated_driver):
    page = LkPage(authenticated_driver)
    page.open_vitrina()
    page.wait_ready()
    return page


@pytest.fixture(scope="function")
def processor_driver(authenticated_driver):
    driver = authenticated_driver
    main_window = driver.current_window_handle
    try:
        page = LkPage(driver)
        page.open_vitrina()
        page.wait_ready()
        LkFlow(driver).open_service_provider()
        yield driver
    finally:
        for handle in list(driver.window_handles):
            if handle != main_window:
                try:
                    driver.switch_to.window(handle)
                    driver.close()
                except WebDriverException:
                    pass
        try:
            driver.switch_to.window(main_window)
            if BID_LK_EXPECTED_URL not in driver.current_url:
                driver.get(BID_LK_EXPECTED_URL)
            LkPage(driver).dismiss_consent_modals()
        except WebDriverException:
            pass


def _find_driver(item):
    for name in ("processor_driver", "authenticated_driver", "lk_driver", "lk_page"):
        if name in item.funcargs:
            value = item.funcargs[name]
            if name == "lk_page":
                return value.driver
            return value
    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if allure is None or report.failed is False:
        return
    if call.when not in ("setup", "call"):
        return

    driver = _find_driver(item)
    if driver is None:
        return

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"screenshot-{call.when}",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            driver.current_url,
            name=f"url-{call.when}",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception:
        pass
