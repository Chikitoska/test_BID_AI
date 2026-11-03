"""Unit tests: stale badge/modal after LK login must not abort lk_auth_login."""

from __future__ import annotations

from selenium.common.exceptions import StaleElementReferenceException

from pages.lk_flow import HttpStatusError, LkAuthError, LkFlow


class _StaleBadge:
    def is_displayed(self) -> bool:
        raise StaleElementReferenceException("stale element not found")


class _VisibleBadge:
    def is_displayed(self) -> bool:
        return True


class _FakeDriver:
    def __init__(self, url: str, elements_seq: list[list[object]]):
        self.current_url = url
        self._elements_seq = list(elements_seq)

    def find_elements(self, _by, _value):
        if self._elements_seq:
            return self._elements_seq.pop(0)
        return []


def test_has_lk_session_stale_badge_is_not_ready() -> None:
    driver = _FakeDriver(
        "https://lk.bid.gazprom-neft.ru/service-providers",
        [[_StaleBadge()], [_StaleBadge()], [_StaleBadge()]],
    )
    flow = LkFlow(driver, wait_sec=1)
    assert flow._has_lk_session() is False


def test_has_lk_session_recovers_after_stale_rerender() -> None:
    driver = _FakeDriver(
        "https://lk.bid.gazprom-neft.ru/service-providers",
        [[_StaleBadge()], [_VisibleBadge()]],
    )
    flow = LkFlow(driver, wait_sec=1)
    assert flow._has_lk_session() is True


def test_has_lk_session_false_off_lk_host() -> None:
    driver = _FakeDriver("https://id.bid.gazprom-neft.ru/realms/x", [[_VisibleBadge()]])
    flow = LkFlow(driver, wait_sec=1)
    assert flow._has_lk_session() is False


def test_find_visible_skips_stale_and_returns_next() -> None:
    class _Enabled:
        def is_displayed(self) -> bool:
            return True

        def is_enabled(self) -> bool:
            return True

    class _Stale:
        def is_displayed(self) -> bool:
            raise StaleElementReferenceException("stale")

        def is_enabled(self) -> bool:
            return True

    live = _Enabled()
    driver = _FakeDriver("https://id.bid.gazprom-neft.ru/", [[_Stale(), live]])
    flow = LkFlow(driver, wait_sec=1)
    assert flow._find_visible((("css selector", "#otp"),)) is live


def test_ensure_lk_ready_continues_after_stale_then_sees_badge(monkeypatch) -> None:
    calls = {"n": 0}

    def _modals(_driver, timeout=3):
        calls["n"] += 1
        if calls["n"] == 1:
            raise StaleElementReferenceException("modal rerender")
        return False

    driver = _FakeDriver(
        "https://lk.bid.gazprom-neft.ru/service-providers",
        [[_VisibleBadge()]],
    )
    flow = LkFlow(driver, wait_sec=1)
    monkeypatch.setattr("pages.lk_flow.accept_lk_consent_modals", _modals)
    flow._ensure_lk_ready()


def test_ensure_lk_ready_still_raises_http_500(monkeypatch) -> None:
    monkeypatch.setattr("pages.lk_flow.LK_UI_WAIT_SEC", 0)
    monkeypatch.setattr("pages.lk_flow.accept_lk_consent_modals", lambda *_a, **_k: False)
    driver = _FakeDriver("https://lk.bid.gazprom-neft.ru/error/500", [[]])
    flow = LkFlow(driver, wait_sec=1)
    try:
        flow._ensure_lk_ready()
    except HttpStatusError as exc:
        assert "/error/500" in str(exc)
    else:
        raise AssertionError("expected HttpStatusError")


def test_ensure_lk_ready_times_out_without_badge(monkeypatch) -> None:
    monkeypatch.setattr("pages.lk_flow.LK_UI_WAIT_SEC", 0)
    monkeypatch.setattr("pages.lk_flow.accept_lk_consent_modals", lambda *_a, **_k: False)
    driver = _FakeDriver("https://lk.bid.gazprom-neft.ru/service-providers", [[]])
    flow = LkFlow(driver, wait_sec=1)
    flow.wait_sec = 0
    try:
        flow._ensure_lk_ready()
    except LkAuthError as exc:
        assert "нет бейджа" in str(exc)
    else:
        raise AssertionError("expected LkAuthError")
