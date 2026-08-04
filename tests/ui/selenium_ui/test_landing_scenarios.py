"""Selenium: сценарии лендинга BID (зеркало Playwright)."""

import pytest

from config import locators as L
from pages.landing_page import LandingPage
from tests.ui.scenarios import (
    assert_get_id_link,
    assert_inn_filled,
    assert_landing_opened,
    assert_login_visible_not_used,
)


@pytest.mark.ui
@pytest.mark.selenium
class TestLandingScenariosSelenium:
    """Набор сценариев лендинга на Selenium WebDriver."""

    def test_scenario_01_landing_opens(self, landing_page: LandingPage):
        assert_landing_opened(landing_page.driver.title, landing_page.driver.current_url)

    def test_scenario_02_login_visible_not_clicked(self, landing_page: LandingPage):
        login_link = landing_page.wait_visible(landing_page.LOGIN_LINK)
        login_btn = landing_page.wait_visible(landing_page.LOGIN_BUTTON)
        assert login_link.is_displayed()
        assert login_btn.is_displayed()
        assert_login_visible_not_used(login_link.get_attribute("href"))

    def test_scenario_03_get_id_link(self, landing_page: LandingPage):
        link = landing_page.wait_visible(landing_page.GET_ID_LINK)
        assert link.is_displayed()
        assert_get_id_link(link.get_attribute("href"))

    def test_scenario_04_inn_block(self, landing_page: LandingPage):
        inn = landing_page.wait_visible(landing_page.INN_INPUT)
        add_btn = landing_page.wait_visible(landing_page.ADD_INN_BUTTON)
        assert inn.is_displayed()
        assert add_btn.is_displayed()
        inn.clear()
        inn.send_keys(L.TEST_INN)
        assert_inn_filled(inn.get_attribute("value"))

    def test_scenario_05_navigation_tab(self, landing_page: LandingPage):
        landing_page.click_tab("Потребителям")
        tab = landing_page.wait_present(landing_page.NAV_TABS["Потребителям"])
        assert tab is not None

    @pytest.mark.parametrize("tab_name", L.NAV_TABS)
    def test_scenario_06_all_tabs_present(self, landing_page: LandingPage, tab_name: str):
        tab = landing_page.wait_present(landing_page.NAV_TABS[tab_name])
        assert tab is not None

    def test_scenario_07_contact_form(self, landing_page: LandingPage):
        assert landing_page.wait_visible(landing_page.CONTACT_NAME).is_displayed()
        assert landing_page.wait_visible(landing_page.CONTACT_EMAIL).is_displayed()
        assert landing_page.wait_visible(landing_page.CONTACT_PHONE).is_displayed()
        assert landing_page.wait_visible(landing_page.CONTACT_INN).is_displayed()

    def test_scenario_08_submit_disabled(self, landing_page: LandingPage):
        submit = landing_page.wait_visible(landing_page.SUBMIT_REQUEST)
        assert submit.get_attribute("disabled") is not None

    def test_scenario_09_brand_content(self, landing_page: LandingPage):
        source = landing_page.driver.page_source
        assert "Газпром" in source or "Бизнес ID" in source
