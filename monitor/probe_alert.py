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


def should_send_lk_telegram(*, overall_ok: bool, confirmed_http_error: bool = False) -> bool:
    """Health-алерт. При подтверждённом 4xx/5xx после in-run retry — сразу (threshold=1)."""
    state = AlertState.load()
    threshold = 1 if confirmed_http_error else MONITOR_ALERT_AFTER_FAILURES
    send_fail = state.evaluate_lk_alert(
        overall_ok,
        threshold=threshold,
        repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
    )

    if not overall_ok and not send_fail:
        print(
            f"Alert suppressed: health fail streak {state.consecutive_lk_failures}/"
            f"{threshold}"
        )
    elif not overall_ok and send_fail and confirmed_http_error:
        print("Alert: confirmed HTTP 4xx/5xx after in-run retry — notifying")

    return send_fail


def should_send_lk_pytest_telegram(
    *,
    overall_ok: bool,
    pytest_output: str = "",
    failed: int = 0,
    total: int = 0,
) -> bool:
    """Боевой pytest ЛК: TG/email только при prod/сети, не при UI-флаках автотеста.

    Быстрый пульс «PROD лежит» — это health каждые 5 мин.
    Боевой прогон — глубокий UI; спамить селекторами нельзя, но сеть/5xx — сразу.
    """
    from monitor.pytest_failures import classify_lk_pytest_failure

    state = AlertState.load()

    if overall_ok:
        state.evaluate_lk_pytest_alert(
            True,
            threshold=1,
            repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
        )
        return False

    kind = classify_lk_pytest_failure(pytest_output, failed=failed, total=total)
    if kind == "autotest":
        # Не копить «streak» ради UI-флака — иначе через 2 ч прилетит ложный prod-пейдж.
        state.evaluate_lk_pytest_alert(
            True,
            threshold=1,
            repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
        )
        print(
            "Alert suppressed: lk_pytest failures look like autotest/UI flake "
            "(TimeoutException/assert/selector) — Grafana only; "
            "prod pulse is health every 5 min"
        )
        return False

    # prod/сеть/массовый провал — алерт с первого такого прогона (не ждать 2 часа).
    send_fail = state.evaluate_lk_pytest_alert(
        False,
        threshold=1,
        repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
    )
    if not send_fail:
        print(
            f"Alert suppressed: lk_pytest prod fail already reported "
            f"(anti-flap {TELEGRAM_ALERT_REPEAT_HOURS}h)"
        )
    else:
        print("Alert: lk_pytest classified as prod/network — notifying")
    return send_fail


def notify_probe_failure_direct(http_results) -> None:
    from monitor.alerts import format_probe_failure_alert, send_telegram
    from monitor.config import ALERTS_ENABLED, GITHUB_DISPATCH_ENABLED

    if not ALERTS_ENABLED or GITHUB_DISPATCH_ENABLED:
        return
    send_telegram(format_probe_failure_alert(http_results))
