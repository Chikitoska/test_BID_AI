"""Playwright: сценарии лендинга BID (зеркало Selenium)."""

import pytest
from playwright.sync_api import Page, expect

from config import locators as L
from pages.landing_page_playwright import LandingPagePlaywright
from tests.ui.scenarios import (
    assert_get_id_link,
    assert_inn_filled,
    assert_landing_opened,
    assert_login_visible_not_used,
)


@pytest.fixture
def landing_pw(page: Page) -> LandingPagePlaywright:
    return LandingPagePlaywright(page).open()


@pytest.mark.ui
@pytest.mark.playwright
class TestLandingScenariosPlaywright:
    """Набор сценариев лендинга на Playwright."""

    def test_scenario_01_landing_opens(self, landing_pw: LandingPagePlaywright):
        assert_landing_opened(landing_pw.title, landing_pw.url)

    def test_scenario_02_login_visible_not_clicked(self, landing_pw: LandingPagePlaywright):
        expect(landing_pw.page.locator(f"xpath={L.LOGIN_LINK}")).to_be_visible()
        expect(landing_pw.page.locator(f"xpath={L.LOGIN_BUTTON}")).to_be_visible()
        assert_login_visible_not_used(landing_pw.login_link_href())

    def test_scenario_03_get_id_link(self, landing_pw: LandingPagePlaywright):
        expect(landing_pw.page.locator(f"xpath={L.GET_ID_LINK}").first).to_be_visible()
        assert_get_id_link(landing_pw.get_id_link_href())

    def test_scenario_04_inn_block(self, landing_pw: LandingPagePlaywright):
        expect(landing_pw.page.locator(f"xpath={L.INN_INPUT}")).to_be_visible()
        expect(landing_pw.page.locator(f"xpath={L.ADD_INN_BUTTON}")).to_be_visible()
        landing_pw.fill_inn(L.TEST_INN)
        assert_inn_filled(landing_pw.inn_value())

    def test_scenario_05_navigation_tab(self, landing_pw: LandingPagePlaywright):
        landing_pw.click_tab("Потребителям")
        expect(landing_pw.page.get_by_role("button", name="Потребителям", exact=True)).to_be_visible()

    @pytest.mark.parametrize("tab_name", L.NAV_TABS)
    def test_scenario_06_all_tabs_present(self, landing_pw: LandingPagePlaywright, tab_name: str):
        expect(landing_pw.page.get_by_role("button", name=tab_name, exact=True)).to_be_attached()

    def test_scenario_07_contact_form(self, landing_pw: LandingPagePlaywright):
        for placeholder in L.CONTACT_FIELDS.values():
            expect(landing_pw.page.get_by_placeholder(placeholder)).to_be_visible()

    def test_scenario_08_submit_disabled(self, landing_pw: LandingPagePlaywright):
        expect(landing_pw.page.locator(f"xpath={L.SUBMIT_REQUEST}")).to_be_disabled()

    def test_scenario_09_brand_content(self, landing_pw: LandingPagePlaywright):
        assert landing_pw.page_source_contains("Газпром") or landing_pw.page_source_contains("Бизнес ID")
