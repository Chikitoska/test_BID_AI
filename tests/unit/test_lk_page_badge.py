"""Health шапка ЛК: компания по тексту бейджа, не только Selenium visibility."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from pages.lk_page import LkPage


class _Child:
    def __init__(self, text: str, *, displayed: bool = True):
        self.text = text
        self._displayed = displayed

    def is_displayed(self) -> bool:
        return self._displayed


class _Badge:
    def __init__(self, children: list[_Child], *, displayed: bool = True):
        self._children = children
        self._displayed = displayed

    def is_displayed(self) -> bool:
        return self._displayed

    def find_elements(self, _by, value: str) -> list[_Child]:
        if value == ".User-Info":
            return list(self._children)
        return []


class _StaleThenLiveBadge(_Badge):
    def __init__(self, children: list[_Child]):
        super().__init__(children)
        self._calls = 0

    def is_displayed(self) -> bool:
        self._calls += 1
        if self._calls == 1:
            raise StaleElementReferenceException("stale element not found")
        return True


class _FakeDriver:
    def __init__(self, *, badge: _Badge | None = None, combined: list[_Child] | None = None):
        self.current_url = "https://lk.bid.gazprom-neft.ru/service-providers"
        self._badge = badge
        self._combined = combined or []

    def find_elements(self, _by, value: str):
        if value == LkPage.USER_BADGE:
            return [self._badge] if self._badge is not None else []
        if value == f"{LkPage.USER_BADGE} .User-Info":
            return list(self._combined)
        return []

    def find_element(self, by, value: str):
        found = self.find_elements(by, value)
        if found:
            return found[0]
        raise TimeoutException(value)


def _page(driver, *, wait_sec: float = 0.8) -> LkPage:
    return LkPage(driver, wait_sec=wait_sec)


@patch("pages.lk_page.accept_lk_consent_modals", return_value=False)
@patch("pages.lk_page.dismiss_blocking_lk_modals", return_value=False)
def test_company_reads_text_even_if_child_not_visible(_dismiss, _consent) -> None:
    child = _Child("ООО Тест", displayed=False)
    page = _page(_FakeDriver(badge=_Badge([child])))
    assert page.read_user_company() == "ООО Тест"


@patch("pages.lk_page.accept_lk_consent_modals", return_value=False)
@patch("pages.lk_page.dismiss_blocking_lk_modals", return_value=False)
def test_company_recovers_after_stale_badge(_dismiss, _consent) -> None:
    child = _Child("ООО Тест")
    page = _page(_FakeDriver(badge=_StaleThenLiveBadge([child])))
    assert page.read_user_company() == "ООО Тест"


@patch("pages.lk_page.accept_lk_consent_modals", return_value=False)
@patch("pages.lk_page.dismiss_blocking_lk_modals", return_value=False)
def test_company_timeout_names_selector(_dismiss, _consent) -> None:
    page = _page(_FakeDriver(), wait_sec=0.6)
    with pytest.raises(TimeoutException) as exc:
        page.read_user_company()
    message = str(exc.value)
    assert "компания" in message
    assert "md-user_badge" in message
    assert ".User-Info" in message
