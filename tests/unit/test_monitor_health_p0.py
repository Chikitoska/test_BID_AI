"""Unit tests: health Chrome infra vs prod, busy skip semantics."""

from __future__ import annotations

from monitor.checks import CheckResult
from monitor.health_classify import (
    classify_health_failure,
    health_run_status,
    is_chrome_infra_error,
)
from monitor.probe_alert import should_send_lk_telegram


def _ui(name: str, error: str, *, success: bool = False) -> CheckResult:
    return CheckResult(
        name=name,
        url="https://example/lk",
        method="UI",
        success=success,
        http_code=0 if not success else 200,
        duration_ms=100.0,
        error=error,
    )


def _http(name: str, *, code: int = 0, error: str = "", success: bool = False) -> CheckResult:
    return CheckResult(
        name=name,
        url="https://example/",
        method="GET",
        success=success,
        http_code=code,
        duration_ms=50.0,
        error=error,
    )


def test_is_chrome_infra_empty_message_stacktrace() -> None:
    err = "Message: \nStacktrace:\n#0 0x5ab910d8a86a <unknown>"
    assert is_chrome_infra_error(err) is True


def test_is_chrome_infra_chromedriver_exit() -> None:
    assert is_chrome_infra_error("chromedriver unexpectedly exited; status=1") is True


def test_is_chrome_infra_not_auth_or_http() -> None:
    assert is_chrome_infra_error("ЛК не загрузился после логина") is False
    assert is_chrome_infra_error("HTTP 502: Bad Gateway") is False
    assert is_chrome_infra_error("page /error/500") is False


def test_is_chrome_infra_not_timeout_exception() -> None:
    """TimeoutException с пустым Message — не глушим как Chrome-infra (возможен реальный ЛК)."""
    err = (
        "selenium.common.exceptions.TimeoutException: Message: \n"
        "Stacktrace:\n#0 0x5ab910d8a86a <unknown>"
    )
    assert is_chrome_infra_error(err) is False
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", err),
    ]
    assert classify_health_failure(results) == "prod"


def test_classify_infra_when_all_ui_chrome() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", "Message: \nStacktrace:\n#0 dead"),
    ]
    assert classify_health_failure(results) == "infra"


def test_classify_prod_on_http_5xx() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", "Открылась страница ошибки: /error/500"),
    ]
    assert classify_health_failure(results) == "prod"


def test_classify_prod_on_landing_timeout() -> None:
    results = [
        _http("main_page", error="HTTPSConnectionPool: Read timed out", success=False),
    ]
    assert classify_health_failure(results) == "prod"


def test_classify_prod_on_auth_text() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", "Keycloak: неверный логин или ЛК не загрузился"),
    ]
    assert classify_health_failure(results) == "prod"


def test_health_run_status_busy() -> None:
    assert health_run_status(overall_ok=False, lk_skipped_busy=True) == "skipped_busy"


def test_health_run_status_infra() -> None:
    assert health_run_status(overall_ok=False, failure_kind="infra") == "infra"


def test_should_send_suppresses_infra(monkeypatch, tmp_path) -> None:
    state_file = tmp_path / "alert_state.json"
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", state_file)
    monkeypatch.setattr(st, "ALERT_STATE_FILE", state_file)

    assert should_send_lk_telegram(overall_ok=False, failure_kind="infra") is False
    assert not state_file.exists() or "consecutive_lk_failures" not in state_file.read_text()


def test_should_send_suppresses_busy(monkeypatch, tmp_path) -> None:
    state_file = tmp_path / "alert_state.json"
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", state_file)
    monkeypatch.setattr(st, "ALERT_STATE_FILE", state_file)

    assert should_send_lk_telegram(overall_ok=False, lk_skipped_busy=True) is False


def test_should_send_prod_confirmed_http(monkeypatch, tmp_path) -> None:
    state_file = tmp_path / "alert_state.json"
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", state_file)
    monkeypatch.setattr(st, "ALERT_STATE_FILE", state_file)
    monkeypatch.setattr(cfg, "MONITOR_ALERT_AFTER_FAILURES", 2)

    assert should_send_lk_telegram(overall_ok=False, confirmed_http_error=True) is True
