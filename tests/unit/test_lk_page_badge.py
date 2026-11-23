"""Health шапка ЛК: компания по тексту, не только Selenium visibility."""

from __future__ import annotations

import pytest
from selenium.common.exceptions import StaleElementReferenceException

from pages.lk_page import LkPage, LkPageError


class _Child:
    def __init__(self, text: str, *, displayed: bool = True):
        self.text = text
        self._displayed = displayed

    def is_displayed(self) -> bool:
        return self._displayed


class _StaleThenLive:
    def __init__(self, live: _Child):
        self._live = live
        self._calls = 0

    def find_elements(self, _by, _value):
        self._calls += 1
        if self._calls == 1:
            raise StaleElementReferenceException("stale element not found")
        return [self._live]


class _FakeDriver:
    def __init__(self, *, children: list[_Child] | None = None, finder=None):
        self.current_url = "https://lk.bid.gazprom-neft.ru/service-providers"
        self._children = children or []
        self._finder = finder

    def find_elements(self, _by, value: str):
        if self._finder is not None:
            return self._finder.find_elements(_by, value)
        if value.endswith(".User-Info") or value.endswith(".User-Name"):
            return list(self._children)
        return []


def _page(driver, *, wait_sec: float = 0.8) -> LkPage:
    return LkPage(driver, wait_sec=wait_sec)


def test_company_reads_text_even_if_child_not_visible() -> None:
    child = _Child("ООО Тест", displayed=False)
    page = _page(_FakeDriver(children=[child]))
    assert page.read_user_company() == "ООО Тест"


def test_company_recovers_after_stale_badge() -> None:
    child = _Child("ООО Тест")
    page = _page(_FakeDriver(finder=_StaleThenLive(child)))
    assert page.read_user_company() == "ООО Тест"


def test_company_timeout_names_microservice() -> None:
    page = _page(_FakeDriver(), wait_sec=1)
    page._ms_data_wait_sec = lambda: 1
    with pytest.raises(LkPageError) as exc:
        page.read_user_company()
    message = str(exc.value)
    assert "компании" in message
    assert "микросервис company" in message
