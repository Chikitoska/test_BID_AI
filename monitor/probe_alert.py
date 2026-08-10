"""Anti-flap алерты для probe и daily autotests."""

from __future__ import annotations

from monitor.config import (
    MONITOR_ALERT_AFTER_FAILURES,
    TELEGRAM_ALERT_ON_RECOVERY,
    TELEGRAM_ALERT_REPEAT_HOURS,
)
from monitor.state import AlertState


def should_send_probe_telegram(*, overall_ok: bool) -> bool:
    state = AlertState.load()
    send_fail, send_recovery = state.evaluate_probe_alert(
        overall_ok,
        threshold=MONITOR_ALERT_AFTER_FAILURES,
        repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
    )

    if not overall_ok and not send_fail:
        print(
            f"Alert suppressed: probe fail streak {state.consecutive_probe_failures}/"
            f"{MONITOR_ALERT_AFTER_FAILURES}"
        )

    if send_recovery and TELEGRAM_ALERT_ON_RECOVERY:
        from monitor.alerts import format_recovery_message, send_telegram
        from monitor.config import ALERTS_ENABLED, GITHUB_DISPATCH_ENABLED

        if ALERTS_ENABLED and not GITHUB_DISPATCH_ENABLED:
            send_telegram(format_recovery_message())

    return send_fail


def should_send_daily_telegram(*, overall_ok: bool) -> bool:
    state = AlertState.load()
    send_fail = state.evaluate_daily_alert(overall_ok, repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS)

    if not overall_ok and not send_fail:
        print("Alert suppressed: daily fail already reported (anti-flap)")

    return send_fail


def notify_probe_failure_direct(http_results) -> None:
    from monitor.alerts import format_probe_failure_alert, send_telegram
    from monitor.config import ALERTS_ENABLED, GITHUB_DISPATCH_ENABLED

    if not ALERTS_ENABLED or GITHUB_DISPATCH_ENABLED:
        return
    send_telegram(format_probe_failure_alert(http_results))
