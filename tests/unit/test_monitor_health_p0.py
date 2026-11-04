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
from monitor.http_status import prefer_http_error, prefer_http_error_results, results_have_http_4xx_or_5xx
from monitor.metrics import failures_from_checks
from monitor.probe_alert import should_send_lk_pytest_telegram, should_send_lk_telegram
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


def test_classify_chatbot_topic_fail_is_autotest_not_prod() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui(
            "lk_chatbot_topics",
            "ЛК: после открытия чата темы не отображаются. Текст: "
            "'Витрина\\nПодтвердите роль куратора'",
        ),
    ]
    assert is_autotest_error(results[1].error) is True
    assert classify_health_failure(results) == "autotest"


def test_classify_assistant_unavailable_is_prod_not_autotest() -> None:
    err = (
        "Лендинг: после открытия чата темы не отображаются. Текст: "
        "'Ассистент\\nНеизвестная ошибка\\n\\n"
        "Сейчас ассистент недоступен — попробуйте вернуться позже или обратитесь в поддержку'"
    )
    results = [
        _http("main_page", code=200, success=True),
        _ui("landing_chatbot_topics", err),
    ]
    assert is_autotest_error(err) is False
    assert classify_health_failure(results) == "prod"
    assert health_run_status(overall_ok=False, failure_kind="prod") == "fail"


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


def test_health_run_status_busy_http_ok_is_green() -> None:
    """HTTP лендинга прошёл — весь health не красим в skipped_busy."""
    assert health_run_status(overall_ok=True, lk_skipped_busy=True, http_ok=True) == "ok"


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


def test_classify_health_enospc_is_autotest_not_prod(monkeypatch, tmp_path) -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui(
            "chrome_disk",
            "ENOSPC: Avail=12MB < 500MB — Chrome not launched (no space left on device)",
        ),
    ]
    assert is_autotest_error(results[1].error) is True
    assert classify_health_failure(results) == "autotest"
    assert health_run_status(overall_ok=False, failure_kind="autotest") == "autotest"
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", tmp_path / "alert_state.json")
    monkeypatch.setattr(st, "ALERT_STATE_FILE", tmp_path / "alert_state.json")
    assert should_send_lk_telegram(overall_ok=False, failure_kind="autotest") is False


def test_classify_lk_pytest_enospc_is_autotest_not_prod(monkeypatch, tmp_path) -> None:
    out = (
        "Pytest не запустился:\n"
        'File "/opt/test_BID_AI/.venv/lib/python3.12/site-packages/'
        'allure_commons/logger.py", line 25, in _report_item\n'
        'OSError: [Errno 28] No space left on device\n'
    )
    assert classify_lk_pytest_failure(out, failed=1, total=0) == "autotest"
    assert classify_lk_pytest_failure(out, failed=1, total=10) == "autotest"
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", tmp_path / "alert_state.json")
    monkeypatch.setattr(st, "ALERT_STATE_FILE", tmp_path / "alert_state.json")
    assert (
        should_send_lk_pytest_telegram(overall_ok=False, pytest_output=out, failed=1, total=0)
        is False
    )


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


def test_classify_events_harness_miss_is_autotest() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui(
            "landing_chatbot_events",
            "landing_chatbot: POST /events не обнаружен (harness: страница 200, сниффер пуст)",
        ),
    ]
    assert is_autotest_error(results[1].error) is True
    assert classify_health_failure(results) == "autotest"


def test_classify_spa_back_5xx_is_prod() -> None:
    results = [
        _http("main_page", code=200, success=True),
        _ui("landing_chatbot_events", "landing_chatbot: spa-back HTTP 502 — POST /events"),
    ]
    assert is_autotest_error(results[1].error) is False
    assert classify_health_failure(results) == "prod"


def test_classify_lk_pytest_dns_prod() -> None:
    out = (
        "FAILED tests/lk/x.py::t - "
        "NameResolutionError: Temporary failure in name resolution\n1 failed"
    )
    assert classify_lk_pytest_failure(out, failed=1, total=5) == "prod"


def test_get_500_then_retry_200_stays_fail_and_alerts(monkeypatch, tmp_path) -> None:
    """Первый GET 500 в слоте не затирается retry 200: red + bid_failure + email."""
    first = _http("main_page", code=500, error="landing HTTP 500: Internal Server Error", success=False)
    retry = _http("main_page", code=200, success=True)
    kept = prefer_http_error(first, retry)
    assert kept.success is False
    assert kept.http_code == 500
    assert classify_health_failure([kept]) == "prod"
    assert health_run_status(overall_ok=False, failure_kind="prod") == "fail"
    events = failures_from_checks([kept])
    assert events
    assert events[0].check == "main_page"
    assert "500" in events[0].error
    import monitor.config as cfg
    import monitor.state as st

    monkeypatch.setattr(cfg, "ALERT_STATE_FILE", tmp_path / "alert_state.json")
    monkeypatch.setattr(st, "ALERT_STATE_FILE", tmp_path / "alert_state.json")
    monkeypatch.setattr(cfg, "MONITOR_ALERT_AFTER_FAILURES", 2)
    assert should_send_lk_telegram(overall_ok=False, confirmed_http_error=True) is True


def test_main_page_retry_keeps_first_500(monkeypatch) -> None:
    from monitor import run_health_monitor as rhm

    seq = [
        _http("main_page", code=500, error="HTTP 500", success=False),
        _http("main_page", code=200, success=True),
    ]
    monkeypatch.setattr(rhm, "_check_get", lambda *_a, **_k: seq.pop(0))
    monkeypatch.setattr(rhm, "MONITOR_PROBE_RETRIES", 1)
    monkeypatch.setattr(rhm.time, "sleep", lambda _s: None)
    result = rhm._check_main_page_with_retry(session=None)
    assert result.success is False
    assert result.http_code == 500


def test_lk_retry_200_does_not_erase_500(monkeypatch) -> None:
    import monitor.lk_checks as lk_checks

    fail = [
        CheckResult(
            name="lk_auth_login",
            url="https://lk.bid.gazprom-neft.ru/error/500",
            method="UI",
            success=False,
            http_code=500,
            duration_ms=100.0,
            error=(
                "lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | "
                "HTTP 500 | ЛК вернул HTTP error page после входа"
            ),
        )
    ]
    ok = [
        CheckResult(
            name="lk_auth_login",
            url="https://lk.bid.gazprom-neft.ru/",
            method="UI",
            success=True,
            http_code=200,
            duration_ms=80.0,
            error="",
        )
    ]
    calls = {"n": 0}

    def _once(*, include_lk: bool = True):
        calls["n"] += 1
        return fail if calls["n"] == 1 else ok

    monkeypatch.setattr(lk_checks, "_run_lk_monitor_checks_once", _once)
    monkeypatch.setattr(lk_checks.time, "sleep", lambda _s: None)
    results = lk_checks.run_lk_monitor_checks()
    assert calls["n"] == 2
    assert results_have_http_4xx_or_5xx(results)
    assert results[0].success is False
    assert results[0].http_code == 500
    assert prefer_http_error_results([fail, ok]) == fail
