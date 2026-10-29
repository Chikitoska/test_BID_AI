"""Unit tests: richer pytest / Selenium failure messages for bid_failure."""

from __future__ import annotations

from monitor.checks import CheckResult
from monitor.metrics import failures_from_checks
from monitor.pytest_failures import (
    brief_exception_text,
    extract_failure_url,
    format_rich_failure_error,
    parse_pytest_failures,
)


def test_brief_empty_timeout_message() -> None:
    detail = "selenium.common.exceptions.TimeoutException: Message:"
    assert brief_exception_text(detail) == (
        "TimeoutException: element not found / wait timed out"
    )


def test_brief_empty_timeout_message_with_trailing_space() -> None:
    detail = "TimeoutException: Message: "
    assert brief_exception_text(detail) == (
        "TimeoutException: element not found / wait timed out"
    )


def test_brief_keeps_nonempty_message() -> None:
    detail = "TimeoutException: Message: Processor: «ФИО» пустой"
    assert brief_exception_text(detail) == "TimeoutException: Processor: «ФИО» пустой"


def test_format_rich_with_url() -> None:
    err = format_rich_failure_error(
        test_name="test_lk_accreditation_navigation",
        detail="selenium.common.exceptions.TimeoutException: Message:",
        url="https://lk.bid.gazprom-neft.ru/accreditation",
    )
    assert err == (
        "test_lk_accreditation_navigation | "
        "https://lk.bid.gazprom-neft.ru/accreditation | "
        "TimeoutException: element not found / wait timed out"
    )


def test_format_rich_without_url() -> None:
    err = format_rich_failure_error(
        test_name="test_lk_nav_menu_items",
        detail="TimeoutException: Message:",
        url=None,
    )
    assert err == (
        "test_lk_nav_menu_items | TimeoutException: element not found / wait timed out"
    )


def test_parse_pytest_empty_message_no_url() -> None:
    output = (
        "FAILED tests/lk/test_lk_smoke.py::test_lk_accreditation_fallback - "
        "selenium.common.exceptions.TimeoutException: Message:\n"
    )
    events = parse_pytest_failures(output)
    assert len(events) == 1
    assert events[0].check == "test_lk_accreditation_fallback"
    assert events[0].error == (
        "test_lk_accreditation_fallback | "
        "TimeoutException: element not found / wait timed out"
    )


def test_parse_pytest_extracts_url_from_traceback_section() -> None:
    output = """
=================================== FAILURES ===================================
_______________________ test_lk_accreditation_navigation _______________________
pages/lk_page.py:125: in open_section
    raise TimeoutException(f'Раздел не загрузился (URL: {self.driver.current_url})')
E   selenium.common.exceptions.TimeoutException: Message: Раздел не загрузился (URL: https://lk.bid.gazprom-neft.ru/service-providers/accreditation)
=========================== short test summary info ============================
FAILED tests/lk/test_lk_accreditation.py::test_lk_accreditation_navigation - selenium.common.exceptions.TimeoutException: Message: Раздел не загрузился (URL: https://lk.bid.gazprom-neft.ru/service-providers/accreditation)
"""
    events = parse_pytest_failures(output)
    assert len(events) == 1
    assert "test_lk_accreditation_navigation" in events[0].error
    assert "https://lk.bid.gazprom-neft.ru/service-providers/accreditation" in events[0].error
    assert "TimeoutException:" in events[0].error
    assert "Message:" not in events[0].error or "Раздел" in events[0].error


def test_parse_pytest_empty_message_url_from_section() -> None:
    output = """
=================================== FAILURES ===================================
_________________________ test_lk_nav_profile_and_back _________________________
pages/lk_flow.py:180: in step
    self._log('stuck at https://lk.bid.gazprom-neft.ru/profile')
E   selenium.common.exceptions.TimeoutException: Message:
=========================== short test summary info ============================
FAILED tests/lk/test_lk_smoke.py::test_lk_nav_profile_and_back - selenium.common.exceptions.TimeoutException: Message:
"""
    events = parse_pytest_failures(output)
    assert len(events) == 1
    assert events[0].error == (
        "test_lk_nav_profile_and_back | "
        "https://lk.bid.gazprom-neft.ru/profile | "
        "TimeoutException: element not found / wait timed out"
    )


def test_extract_failure_url_prefers_lk() -> None:
    text = (
        "see https://www.selenium.dev/documentation/webdriver "
        "and https://lk.bid.gazprom-neft.ru/foo"
    )
    assert extract_failure_url(text) == "https://lk.bid.gazprom-neft.ru/foo"


def test_failures_from_checks_enriches_ui_empty_message() -> None:
    results = [
        CheckResult(
            name="lk_auth_login",
            url="https://lk.bid.gazprom-neft.ru/service-providers",
            method="UI",
            success=False,
            http_code=0,
            duration_ms=1200.0,
            error="selenium.common.exceptions.TimeoutException: Message: ",
        )
    ]
    events = failures_from_checks(results)
    assert len(events) == 1
    assert events[0].error == (
        "lk_auth_login | "
        "https://lk.bid.gazprom-neft.ru/service-providers | "
        "TimeoutException: element not found / wait timed out"
    )
