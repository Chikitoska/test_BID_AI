#!/usr/bin/env python3
"""
Health-мониторинг: лендинг (HTTP) + чат-бот лендинга/ЛК + ЛК (вход, ФИО, компания).

Один контур для prod: «сайт жив» + «ассистент работает» + «ЛК доступен».
Запуск: cron каждые 5 мин.

Тяжёлый регресс ЛК — отдельно: run_lk_pytest.py (каждые 2 ч + Allure).
"""

from __future__ import annotations

import os
import signal
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import BASE_URL
from monitor.chrome_lock import ChromeBusyError, chrome_run_lock
from monitor.checks import CheckResult, _check_get
from monitor.config import (
    INFLUX_ENABLED,
    LK_MONITOR_ENABLED,
    MONITOR_HEALTH_RETRY_DELAY_SEC,
    MONITOR_PROBE_RETRIES,
)
from monitor.github_dispatch import notify_github_on_failure
from monitor.health_classify import (
    classify_health_failure,
    health_run_status,
    is_autotest_failure_kind,
)
from monitor.http_session import create_monitor_session
from monitor.http_status import is_http_4xx_or_5xx, results_have_http_4xx_or_5xx
from monitor.lk_checks import run_lk_monitor_checks
from monitor.metrics import (
    failures_from_checks,
    write_check_results,
    write_failure_events,
    write_lk_check_results,
    write_lk_run,
)
from monitor.probe_alert import should_send_lk_telegram

# Слот cron = 5 мин. Ждать lock 600 с = два пропущенных столбца и риск зависания.
HEALTH_LOCK_WAIT_CAP_SEC = 90.0
HEALTH_SLOT_SEC_DEFAULT = 220.0


class HealthSlotTimeout(Exception):
    """Health не уложился в слот 5 мин (Chrome hang / lock wait)."""


def health_lock_wait_sec(configured: float, *, cap: float = HEALTH_LOCK_WAIT_CAP_SEC) -> float:
    """Health ждёт Chrome не дольше cap — иначе пропускает слот без точки."""
    return max(5.0, min(float(configured), cap))


def _slot_handler(signum, frame) -> None:
    raise HealthSlotTimeout(f"signal {signum}: health превысил слот 5 мин")


def _check_main_page_with_retry(session) -> CheckResult:
    """GET с повтором при timeout/4xx/5xx — снижает ложные алерты на флапах."""
    landing = _check_get(session, "main_page", BASE_URL)
    if landing.success or MONITOR_PROBE_RETRIES <= 0:
        return landing

    reason = landing.error or f"HTTP {landing.http_code}"
    print(
        f"main_page FAIL ({reason}), "
        f"повтор через {MONITOR_HEALTH_RETRY_DELAY_SEC} с "
        f"(ещё {MONITOR_PROBE_RETRIES} раз)…",
        flush=True,
    )
    time.sleep(MONITOR_HEALTH_RETRY_DELAY_SEC)
    return _check_get(session, "main_page", BASE_URL)


def _flush_health_influx(
    *,
    landing: CheckResult,
    all_results: list[CheckResult],
    overall_ok: bool,
    lk_skipped_busy: bool,
    run_status: str,
    duration_sec: float,
    http_ok: bool,
) -> None:
    """bid_lk_run пишем отдельно: пульс не должен пропадать, если упал write_check_results."""
    if not INFLUX_ENABLED:
        return
    try:
        write_lk_run(
            success=overall_ok,
            failed_count=sum(1 for r in all_results if not r.success),
            duration_sec=duration_sec,
            skipped=lk_skipped_busy,
            run_status=run_status,
        )
        if lk_skipped_busy and http_ok:
            print(
                f"Metrics sent to InfluxDB (run_status={run_status}, "
                "HTTP лендинга записан, UI skipped из‑за Chrome busy)"
            )
        elif lk_skipped_busy:
            print("Metrics sent to InfluxDB (run_status=skipped_busy, skipped=1, success=0)")
        else:
            print(f"Metrics sent to InfluxDB (run_status={run_status})")
    except Exception as exc:
        print(f"WARN: InfluxDB write_lk_run failed: {exc}")
    try:
        write_check_results(
            [landing]
            + [r for r in all_results if r.name.startswith("landing_chatbot")]
        )
        if landing.success and not lk_skipped_busy:
            lk_only = [r for r in all_results if r.name.startswith("lk_")]
            if lk_only:
                write_lk_check_results(lk_only)
    except Exception as exc:
        print(f"WARN: InfluxDB write checks failed: {exc}")
    failed_results = [r for r in all_results if not r.success]
    if failed_results:
        try:
            write_failure_events(run_type="health", failures=failures_from_checks(failed_results))
        except Exception as exc:
            print(f"WARN: InfluxDB failure events: {exc}")


def main() -> int:
    print("=== BID Health Monitor (landing + LK) ===")
    start = time.perf_counter()
    all_results: list[CheckResult] = []
    slot_sec = float(os.getenv("HEALTH_SLOT_SEC", str(HEALTH_SLOT_SEC_DEFAULT)))
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, _slot_handler)
        signal.alarm(max(1, int(slot_sec)))
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _slot_handler)

    landing = CheckResult(
        name="main_page",
        url=BASE_URL,
        method="GET",
        success=False,
        http_code=0,
        duration_ms=0.0,
        error="health aborted before HTTP",
    )
    lk_ok = True
    lk_skipped_busy = False
    lk_results: list[CheckResult] = []
    try:
        session = create_monitor_session()
        landing = _check_main_page_with_retry(session)
        all_results.append(landing)
        status = "OK" if landing.success else "FAIL"
        print(f"[{status}] main_page {landing.http_code} {landing.duration_ms:.0f}ms {landing.error}")

        if not landing.success:
            print("SKIP UI: лендинг недоступен (чат-бот и ЛК не проверяем)")
            lk_ok = False
        else:
            configured_wait = float(os.getenv("CHROME_LOCK_WAIT_HEALTH_SEC", "90"))
            lk_wait = health_lock_wait_sec(configured_wait)
            if lk_wait < configured_wait:
                print(
                    f"[chrome-lock] health wait capped {configured_wait:.0f}s → {lk_wait:.0f}s "
                    "(слот cron 5 мин)",
                    flush=True,
                )
            try:
                with chrome_run_lock(owner="health", wait_sec=lk_wait):
                    lk_results = run_lk_monitor_checks(include_lk=LK_MONITOR_ENABLED)
            except ChromeBusyError as exc:
                lk_skipped_busy = True
                print(f"SKIP UI (chrome busy): {exc}")
                print(
                    "UI/chatbot/LK пропущены (Chrome занят); "
                    "HTTP лендинга уже записан и остаётся источником пульса",
                    flush=True,
                )
            except HealthSlotTimeout as exc:
                print(f"SKIP UI (slot timeout): {exc}", flush=True)
                lk_ok = False
                all_results.append(
                    CheckResult(
                        name="health_slot",
                        url=BASE_URL,
                        method="UI",
                        success=False,
                        http_code=0,
                        duration_ms=(time.perf_counter() - start) * 1000,
                        error="TimeoutException: health UI exceeded 5-min slot (Chrome hang)",
                    )
                )
            for item in lk_results:
                st = "OK" if item.success else "FAIL"
                print(f"[{st}] {item.name} {item.duration_ms:.0f}ms {item.error}")
            if lk_results:
                lk_ok = all(item.success for item in lk_results)
            elif not lk_skipped_busy:
                lk_ok = False
            if lk_results:
                all_results.extend(lk_results)
            if not LK_MONITOR_ENABLED and not lk_skipped_busy:
                print("SKIP LK auth: MONITOR_RUN_LK=false или нет credentials (чат-бот лендинга уже проверен)")
    except HealthSlotTimeout as exc:
        print(f"Health slot timeout: {exc}", flush=True)
        lk_ok = False
        if not any(item.name == "main_page" for item in all_results):
            all_results.append(landing)
        if not any(item.name == "health_slot" for item in all_results):
            all_results.append(
                CheckResult(
                    name="health_slot",
                    url=BASE_URL,
                    method="UI",
                    success=False,
                    http_code=0,
                    duration_ms=(time.perf_counter() - start) * 1000,
                    error="TimeoutException: health UI exceeded 5-min slot (Chrome hang)",
                )
            )
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)

    duration_sec = time.perf_counter() - start
    http_ok = landing.success
    # Chrome busy: HTTP лендинга уже есть — не красим весь health в skipped_busy.
    # UI/chatbot/LK пропускаем, но успешный HTTP = пульс зелёный.
    if lk_skipped_busy:
        overall_ok = http_ok
    else:
        overall_ok = http_ok and lk_ok

    failure_kind = None
    if not overall_ok and not lk_skipped_busy:
        failure_kind = classify_health_failure(all_results)
        if is_autotest_failure_kind(failure_kind):
            print(
                "CLASSIFIED=autotest — UI flake / Chrome/WebDriver; "
                "не считаем подтверждённым падением ЛК/PROD",
                flush=True,
            )

    run_status = health_run_status(
        overall_ok=overall_ok,
        lk_skipped_busy=lk_skipped_busy,
        failure_kind=failure_kind,
        http_ok=http_ok,
    )

    _flush_health_influx(
        landing=landing,
        all_results=all_results,
        overall_ok=overall_ok,
        lk_skipped_busy=lk_skipped_busy,
        run_status=run_status,
        duration_sec=duration_sec,
        http_ok=http_ok,
    )

    # 4xx/5xx уже перепроверены в этом же прогоне → алертим сразу, не ждём следующий cron.
    # Autotest/busy — не confirmed prod.
    confirmed_http_error = (
        (not overall_ok)
        and (not lk_skipped_busy)
        and (not is_autotest_failure_kind(failure_kind))
        and (
            results_have_http_4xx_or_5xx(all_results)
            or is_http_4xx_or_5xx(http_code=landing.http_code, error=landing.error)
        )
    )
    send_alert = should_send_lk_telegram(
        overall_ok=overall_ok,
        confirmed_http_error=confirmed_http_error,
        failure_kind=failure_kind,
        lk_skipped_busy=lk_skipped_busy,
    )
    # TG/email только при prod (не autotest, не busy).
    if not overall_ok and send_alert and not is_autotest_failure_kind(failure_kind) and not lk_skipped_busy:
        notify_github_on_failure(
            run_type="health",
            http_results=all_results,
            failed_count=sum(1 for r in all_results if not r.success),
            duration_sec=duration_sec,
        )

    if lk_skipped_busy and http_ok:
        outcome = "OK_HTTP_UI_SKIPPED"
        exit_code = 0
    elif lk_skipped_busy:
        outcome = "SKIPPED_BUSY"
        # Exit 0: cron не шумит; HTTP лендинга неуспешен + UI не проверили.
        exit_code = 0
    elif overall_ok:
        outcome = "OK"
        exit_code = 0
    elif is_autotest_failure_kind(failure_kind):
        outcome = "FAIL_AUTOTEST"
        exit_code = 1
    else:
        outcome = "FAIL"
        exit_code = 1

    print(f"Health monitor finished in {duration_sec:.1f}s — {outcome} (run_status={run_status})")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
