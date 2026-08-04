"""Page Object лендинга BID для Playwright."""

from playwright.sync_api import Page, expect

from config import locators as L


class LandingPagePlaywright:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> "LandingPagePlaywright":
        self.page.goto(L.BASE_URL, wait_until="domcontentloaded")
        expect(self.page).to_have_title(L.PAGE_TITLE)
        expect(self.page.locator(f"xpath={L.LOGIN_LINK}")).to_be_visible(timeout=30_000)
        expect(self.page.get_by_role("button", name=L.NAV_TABS[0], exact=True)).to_be_attached(
            timeout=30_000
        )
        return self

    @property
    def title(self) -> str:
        return self.page.title()

    @property
    def url(self) -> str:
        return self.page.url

    def login_link_href(self) -> str:
        return self.page.locator(f"xpath={L.LOGIN_LINK}").get_attribute("href") or ""

    def get_id_link_href(self) -> str:
        return self.page.locator(f"xpath={L.GET_ID_LINK}").first.get_attribute("href") or ""

    def fill_inn(self, inn: str = L.TEST_INN) -> None:
        field = self.page.locator(f"xpath={L.INN_INPUT}")
        field.scroll_into_view_if_needed()
        field.fill(inn)

    def inn_value(self) -> str:
        return self.page.locator(f"xpath={L.INN_INPUT}").input_value()

    def click_tab(self, tab_name: str) -> None:
        tab = self.page.get_by_role("button", name=tab_name, exact=True)
        tab.scroll_into_view_if_needed()
        tab.click()

    def is_submit_disabled(self) -> bool:
        return self.page.locator(f"xpath={L.SUBMIT_REQUEST}").is_disabled()

    def page_source_contains(self, text: str) -> bool:
        return text in self.page.content()
