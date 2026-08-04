"""Общие сценарии лендинга BID — эталонные проверки для Selenium и Playwright."""

from config import locators as L


def assert_landing_opened(title: str, url: str) -> None:
    assert title == L.PAGE_TITLE
    assert url.rstrip("/") == L.BASE_URL.rstrip("/")


def assert_login_visible_not_used(login_href: str) -> None:
    assert "self-authentication" in login_href


def assert_get_id_link(get_id_href: str) -> None:
    assert "registration" in get_id_href


def assert_inn_filled(inn_value: str, expected: str = L.TEST_INN) -> None:
    assert expected in inn_value.replace(" ", "")
