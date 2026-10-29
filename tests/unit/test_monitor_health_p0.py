"""Unit tests: health/prod vs autotest, busy skip, TG suppress."""

from __future__ import annotations

from monitor.checks import CheckResult
from monitor.health_classify import (
    classify_health_failure,
    health_run_status,
    is_autotest_error,
    is_chrome_infra_error,
    pytest_run_status,
)
from monitor.probe_alert import should_send_lk_telegram
from monitor.pytest_failures import classify_lk_pytest_failure


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
    assert is_autotest_error(err) is True


def test_is_chrome_infra_chromedriver_exit() -> None:
    assert is_chrome_infra_error("chromedriver unexpectedly exited; status=1") is True


def test_is_chrome_infra_not_auth_or_http() -> None:
    assert is_chrome_infra_error("ЛК не загрузился после логина") is False
    assert is_chrome_infra_error("HTTP 502: Bad Gateway") is False
    assert is_chrome_infra_error("page /error/500") is False


def test_timeout_exception_is_autotest_not_chrome_only() -> None:
    """TimeoutException — autotest (оранжевый), не сеть/4xx/5xx."""
    err = (
        "selenium.common.exceptions.TimeoutException: Message: \n"
        "Stacktrace:\n#0 0x5ab910d8a86a <unknown>"
    )
    assert is_chrome_infra_error(err) is False
    assert is_autotest_error(err) is True
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", err),
    ]
    assert classify_health_failure(results) == "autotest"
    assert health_run_status(overall_ok=False, failure_kind="autotest") == "autotest"


def test_classify_autotest_when_all_ui_chrome() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", "Message: \nStacktrace:\n#0 dead"),
    ]
    assert classify_health_failure(results) == "autotest"


def test_classify_prod_on_http_5xx() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui("lk_auth_login", "Открылась страница ошибки: /error/500"),
    ]
    assert classify_health_failure(results) == "prod"
    assert health_run_status(overall_ok=False, failure_kind="prod") == "fail"


def test_classify_prod_on_http_4xx() -> None:
    results = [
        _http("main_page", code=403, error="HTTP 403 Forbidden", success=False),
    ]
    assert classify_health_failure(results) == "prod"


def test_classify_prod_on_landing_dns() -> None:
    results = [
        _http(
            "main_page",
            error="NameResolutionError: Temporary failure in name resolution",
            success=False,
        ),
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


def test_health_run_status_legacy_infra_alias() -> None:
    assert health_run_status(overall_ok=False, failure_kind="infra") == "autotest"


def test_pytest_run_status_tags() -> None:
    assert pytest_run_status(overall_ok=True) == "ok"
    assert pytest_run_status(overall_ok=False, failure_kind="autotest") == "autotest"
    assert pytest_run_status(overall_ok=False, failure_kind="prod") == "fail"


def test_should_send_suppresses_autotest(monkeypatch, tmp_path) -> None:
    state_file = tmp_path / "alert_state.json"
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", state_file)
    monkeypatch.setattr(st, "ALERT_STATE_FILE", state_file)

    assert should_send_lk_telegram(overall_ok=False, failure_kind="autotest") is False
    assert should_send_lk_telegram(overall_ok=False, failure_kind="infra") is False


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


def test_classify_lk_pytest_timeout_autotest() -> None:
    out = (
        "FAILED tests/lk/test_lk_smoke.py::test_lk_nav - "
        "selenium.common.exceptions.TimeoutException: Message:\n"
        "1 failed"
    )
    assert classify_lk_pytest_failure(out, failed=1, total=5) == "autotest"
    assert pytest_run_status(overall_ok=False, failure_kind="autotest") == "autotest"


def test_classify_lk_pytest_chrome_crash_autotest() -> None:
    out = "ERROR ... chromedriver unexpectedly exited; status=1\n1 error"
    assert classify_lk_pytest_failure(out, failed=1, total=5) == "autotest"


def test_classify_lk_pytest_http_5xx_prod() -> None:
    out = "FAILED tests/lk/x.py::t - HttpStatusError: /error/500\n1 failed"
    assert classify_lk_pytest_failure(out, failed=1, total=5) == "prod"
    assert pytest_run_status(overall_ok=False, failure_kind="prod") == "fail"


def test_classify_lk_pytest_dns_prod() -> None:
    out = (
        "FAILED tests/lk/x.py::t - "
        "NameResolutionError: Temporary failure in name resolution\n1 failed"
    )
    assert classify_lk_pytest_failure(out, failed=1, total=5) == "prod"
