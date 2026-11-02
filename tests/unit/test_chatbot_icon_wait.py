"""Иконка чат-бота: 15 с, displayed = успех, нет = красный fail (не жёлтый)."""

from types import SimpleNamespace

from monitor.checks import CheckResult
from monitor.health_classify import (
    classify_health_failure,
    health_run_status,
    is_autotest_error,
    is_widget_icon_miss,
)
from monitor.pytest_failures import classify_lk_pytest_failure
from pages.chatbot_widget import ICON_WAIT_SEC, ChatbotWidget, _LAUNCHER_JS, is_displayed_launcher


def test_icon_wait_is_15_seconds():
    assert ICON_WAIT_SEC == 15
    widget = ChatbotWidget(SimpleNamespace())
    assert widget.timeout == 15


def test_launcher_js_has_no_size_or_fold_heuristics():
    assert "r.bottom" not in _LAUNCHER_JS
    assert "width <= 120" not in _LAUNCHER_JS
    assert "r.width <" not in _LAUNCHER_JS
    assert "allDeep" in _LAUNCHER_JS


def test_is_displayed_launcher_is_just_displayed():
    visible = SimpleNamespace(is_displayed=lambda: True)
    tiny = SimpleNamespace(is_displayed=lambda: True, size={"width": 4, "height": 4})
    hidden = SimpleNamespace(is_displayed=lambda: False)
    assert is_displayed_launcher(visible) is True
    assert is_displayed_launcher(tiny) is True
    assert is_displayed_launcher(hidden) is False


def test_missing_icon_is_red_fail_not_autotest():
    err = "ChatbotError: Лендинг: иконка чат-бота не отображается"
    assert is_widget_icon_miss(err) is True
    assert is_autotest_error(err) is False
    results = [
        CheckResult("main_page", "https://bid.gazprom-neft.ru/", "GET", True, 200, 10.0),
        CheckResult(
            "landing_chatbot_icon",
            "https://bid.gazprom-neft.ru/",
            "UI",
            False,
            0,
            15.0,
            error=err,
        ),
    ]
    assert classify_health_failure(results) == "prod"
    assert health_run_status(overall_ok=False, failure_kind="prod") == "fail"


def test_missing_icon_pytest_is_prod_not_autotest():
    out = (
        "FAILED tests/ui/selenium_ui/test_landing_chatbot.py::"
        "test_landing_chatbot_skips_login_and_registration - "
        "ChatbotError: Лендинг: иконка чат-бота не отображается\n"
        "1 failed"
    )
    assert classify_lk_pytest_failure(out, failed=1, total=5) == "prod"
