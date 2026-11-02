"""Иконка чат-бота: wait + не строгий JS, промах = autotest/жёлтый."""

from types import SimpleNamespace

from monitor.checks import CheckResult
from monitor.health_classify import classify_health_failure, is_autotest_error
from pages.chatbot_widget import ChatbotWidget, _LAUNCHER_JS, is_displayed_launcher


def test_launcher_js_accepts_visible_icon_without_bottom_cut():
    assert "r.bottom <= 0" not in _LAUNCHER_JS
    assert "width <= 120" not in _LAUNCHER_JS
    assert "allDeep" in _LAUNCHER_JS
    assert "scrollIntoView" in _LAUNCHER_JS


def test_is_displayed_launcher_accepts_visible_fab():
    el = SimpleNamespace(
        is_displayed=lambda: True,
        size={"width": 56, "height": 56},
    )
    assert is_displayed_launcher(el) is True


def test_is_displayed_launcher_rejects_hidden_or_tiny():
    hidden = SimpleNamespace(is_displayed=lambda: False, size={"width": 56, "height": 56})
    tiny = SimpleNamespace(is_displayed=lambda: True, size={"width": 4, "height": 4})
    assert is_displayed_launcher(hidden) is False
    assert is_displayed_launcher(tiny) is False


def test_missing_icon_after_wait_stays_autotest_yellow():
    err = "ChatbotError: Лендинг: иконка чат-бота не отображается"
    assert is_autotest_error(err) is True
    results = [
        CheckResult("main_page", "https://bid.gazprom-neft.ru/", "GET", True, 200, 10.0),
        CheckResult(
            "landing_chatbot_icon",
            "https://bid.gazprom-neft.ru/",
            "UI",
            False,
            0,
            10.0,
            error=err,
        ),
    ]
    assert classify_health_failure(results) == "autotest"


def test_widget_default_timeout_waits_several_seconds():
    class Dummy:
        pass

    widget = ChatbotWidget(Dummy(), timeout=20)
    assert widget.timeout == 20
    assert hasattr(widget, "step_icon_visible")
