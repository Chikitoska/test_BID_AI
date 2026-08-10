"""Политика Telegram-алертов для prod-мониторинга."""

from monitor.alerts import (
    format_failure_alert,
    format_probe_failure_alert,
    format_recovery_message,
    format_success_message,
    send_telegram,
)
from monitor.checks import CheckResult
from monitor.config import (
    ALERTS_ENABLED,
    GITHUB_DISPATCH_ENABLED,
    TELEGRAM_ALERT_ON_SUCCESS,
    TELEGRAM_ALERT_REPEAT_HOURS,
    TELEGRAM_DIRECT_ALLOWED,
    TELEGRAM_FULL_RUN_SUMMARY,
)
from monitor.state import AlertState


def notify_probe_result(
    http_results: list[CheckResult],
    *,
    overall_ok: bool,
) -> None:
    if not ALERTS_ENABLED or (GITHUB_DISPATCH_ENABLED and not TELEGRAM_DIRECT_ALLOWED):
        return

    state = AlertState.load()
    notify_failure, notify_recovery = state.mark_probe_result(overall_ok)

    if overall_ok:
        if notify_recovery:
            send_telegram(format_recovery_message())
        return

    if notify_failure or state.should_repeat_failure_alert(TELEGRAM_ALERT_REPEAT_HOURS):
        send_telegram(format_probe_failure_alert(http_results))


def notify_full_run_result(
    http_results: list[CheckResult],
    *,
    overall_ok: bool,
    passed: int,
    total: int,
    pytest_failed: int,
    pytest_output: str,
) -> None:
    if not ALERTS_ENABLED or (GITHUB_DISPATCH_ENABLED and not TELEGRAM_DIRECT_ALLOWED):
        return

    if overall_ok:
        if TELEGRAM_FULL_RUN_SUMMARY or TELEGRAM_ALERT_ON_SUCCESS:
            send_telegram(format_success_message(passed, total, run_type="full"))
        return

    send_telegram(
        format_failure_alert(
            http_results,
            pytest_failed,
            pytest_output,
            run_type="full",
        )
    )
