"""Anti-flap логика Telegram-алертов для probe (один канал — GitHub relay)."""

from __future__ import annotations

from monitor.alerts import format_probe_failure_alert, send_telegram
from monitor.checks import CheckResult
from monitor.config import (
    ALERTS_ENABLED,
    GITHUB_DISPATCH_ENABLED,
    MONITOR_ALERT_AFTER_FAILURES,
    TELEGRAM_ALERT_ON_RECOVERY,
    TELEGRAM_ALERT_REPEAT_HOURS,
)
from monitor.state import AlertState


def should_send_probe_telegram(*, overall_ok: bool) -> bool:
    """
    Решает, слать ли алерт в Telegram.
    - retry уже выполнен в run_light
    - алерт только после N подряд неуспешных probe (по cron)
    """
    state = AlertState.load()
    send_fail, send_recovery = state.evaluate_probe_alert(
        overall_ok,
        threshold=MONITOR_ALERT_AFTER_FAILURES,
        repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
    )

    if not overall_ok and not send_fail:
        print(
            f"Alert suppressed: fail streak {state.consecutive_probe_failures}/"
            f"{MONITOR_ALERT_AFTER_FAILURES} (need consecutive cron failures)"
        )

    if send_recovery and TELEGRAM_ALERT_ON_RECOVERY:
        _send_recovery_direct()

    return send_fail


def _send_recovery_direct() -> None:
    if not ALERTS_ENABLED or GITHUB_DISPATCH_ENABLED:
        return
    from monitor.alerts import format_recovery_message

    send_telegram(format_recovery_message())


def notify_probe_failure_direct(http_results: list[CheckResult]) -> None:
    """Fallback: прямой Telegram с VPS, если GitHub relay не настроен."""
    if not ALERTS_ENABLED or GITHUB_DISPATCH_ENABLED:
        return
    send_telegram(format_probe_failure_alert(http_results))
