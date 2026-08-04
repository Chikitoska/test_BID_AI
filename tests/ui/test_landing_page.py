"""UI-тесты лендинга BID (без авторизации / без клика «Войти»)."""

import pytest

from pages.landing_page import LandingPage


@pytest.mark.ui
@pytest.mark.smoke
def test_page_title(landing_page: LandingPage):
    assert landing_page.driver.title == LandingPage.TITLE


@pytest.mark.ui
@pytest.mark.smoke
def test_page_url(landing_page: LandingPage):
    assert landing_page.driver.current_url.rstrip("/") == LandingPage.URL.rstrip("/")


@pytest.mark.ui
def test_login_button_visible_but_not_used(landing_page: LandingPage):
    """Кнопка «Войти» видна, но мы её не нажимаем (авторизация вне scope)."""
    login_link = landing_page.wait_visible(landing_page.LOGIN_LINK)
    login_btn = landing_page.wait_visible(landing_page.LOGIN_BUTTON)
    assert login_link.is_displayed()
    assert login_btn.is_displayed()
    assert "self-authentication" in login_link.get_attribute("href")


@pytest.mark.ui
def test_get_id_link_visible(landing_page: LandingPage):
    link = landing_page.wait_visible(landing_page.GET_ID_LINK)
    assert link.is_displayed()
    assert "registration" in link.get_attribute("href")


@pytest.mark.ui
def test_inn_block_visible(landing_page: LandingPage):
    inn_input = landing_page.wait_visible(landing_page.INN_INPUT)
    add_btn = landing_page.wait_visible(landing_page.ADD_INN_BUTTON)
    assert inn_input.is_displayed()
    assert add_btn.is_displayed()


@pytest.mark.ui
def test_inn_input_accepts_digits(landing_page: LandingPage):
    inn_input = landing_page.wait_visible(landing_page.INN_INPUT)
    inn_input.clear()
    inn_input.send_keys("7707083893")
    value = inn_input.get_attribute("value")
    assert value and "7707083893" in value.replace(" ", "")


@pytest.mark.ui
def test_checkboxes_visible(landing_page: LandingPage):
    assert landing_page.wait_visible(landing_page.NON_RESIDENT_CHECKBOX).is_displayed()
    assert landing_page.wait_visible(landing_page.BRANCH_CHECKBOX).is_displayed()


@pytest.mark.ui
@pytest.mark.parametrize("tab_name", list(LandingPage.NAV_TABS.keys()))
def test_navigation_tabs_visible(landing_page: LandingPage, tab_name: str):
    tab = landing_page.wait_present(LandingPage.NAV_TABS[tab_name])
    assert tab is not None


@pytest.mark.ui
@pytest.mark.parametrize("tab_name", list(LandingPage.NAV_TABS.keys()))
def test_navigation_tab_clickable(landing_page: LandingPage, tab_name: str):
    landing_page.click_tab(tab_name)
    tab = landing_page.wait_present(LandingPage.NAV_TABS[tab_name])
    assert tab is not None


@pytest.mark.ui
def test_contact_form_fields_visible(landing_page: LandingPage):
    assert landing_page.wait_visible(landing_page.CONTACT_NAME).is_displayed()
    assert landing_page.wait_visible(landing_page.CONTACT_EMAIL).is_displayed()
    assert landing_page.wait_visible(landing_page.CONTACT_PHONE).is_displayed()
    assert landing_page.wait_visible(landing_page.CONTACT_INN).is_displayed()


@pytest.mark.ui
def test_contact_form_submit_disabled_by_default(landing_page: LandingPage):
    submit = landing_page.wait_visible(landing_page.SUBMIT_REQUEST)
    assert submit.is_displayed()
    assert submit.get_attribute("disabled") is not None


@pytest.mark.ui
def test_contact_form_fill_fields(landing_page: LandingPage):
    landing_page.wait_visible(landing_page.CONTACT_NAME).send_keys("Тест")
    landing_page.wait_visible(landing_page.CONTACT_EMAIL).send_keys("test@example.com")
    landing_page.wait_visible(landing_page.CONTACT_PHONE).send_keys("+79991234567")
    landing_page.wait_visible(landing_page.CONTACT_INN).send_keys("7707083893")

    name_val = landing_page.driver.find_element(*landing_page.CONTACT_NAME).get_attribute("value")
    email_val = landing_page.driver.find_element(*landing_page.CONTACT_EMAIL).get_attribute("value")
    assert "Тест" in name_val
    assert "test@example.com" in email_val


@pytest.mark.ui
def test_page_has_body_content(landing_page: LandingPage):
    source = landing_page.driver.page_source
    assert "Газпром" in source or "Бизнес ID" in source


@pytest.mark.ui
def test_no_severe_browser_console_errors(landing_page: LandingPage):
    logs = landing_page.driver.get_log("browser")
    severe = [entry for entry in logs if entry.get("level") == "SEVERE"]
    # Фильтруем известные внешние/аналитические шумы
    critical = [
        entry
        for entry in severe
        if "favicon" not in entry.get("message", "").lower()
        and "chrome-extension" not in entry.get("message", "").lower()
    ]
    assert not critical, f"Severe console errors: {critical[:3]}"
