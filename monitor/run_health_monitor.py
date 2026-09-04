#!/usr/bin/env python3
"""
Health-мониторинг: лендинг (HTTP) + ЛК (вход, ФИО, компания).

Один контур для prod: «сайт жив» + «ЛК доступен».
Запуск: cron каждые 5 мин (см. monitor/MONITOR-ARCH.md).

Тяжёлый регресс ЛК — отдельно: run_lk_pytest.py (каждые 2 ч + Allure).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import BASE_URL
from monitor.chrome_lock import ChromeBusyError, chrome_run_lock
from monitor.checks import CheckResult, _check_get
from monitor.config import INFLUX_ENABLED, LK_MONITOR_ENABLED
from monitor.github_dispatch import notify_github_on_failure
from monitor.http_session import create_monitor_session
from monitor.lk_checks import run_lk_monitor_checks
from monitor.metrics import (
    failures_from_checks,
    write_check_results,
    write_failure_events,
    write_lk_check_results,
    write_lk_run,
)
from monitor.probe_alert import should_send_lk_telegram


def main() -> int:
    print("=== BID Health Monitor (landing + LK) ===")
    start = time.perf_counter()
    all_results: list[CheckResult] = []

    session = create_monitor_session()
    landing = _check_get(session, "main_page", BASE_URL)
    all_results.append(landing)
    status = "OK" if landing.success else "FAIL"
    print(f"[{status}] main_page {landing.http_code} {landing.duration_ms:.0f}ms {landing.error}")

    lk_ok = True
    lk_skipped_busy = False
    if LK_MONITOR_ENABLED:
        if not landing.success:
            print("SKIP LK: лендинг недоступен")
            lk_ok = False
        else:
            lk_wait = float(os.getenv("CHROME_LOCK_WAIT_HEALTH_SEC", "120"))
            try:
                with chrome_run_lock(owner="health", wait_sec=lk_wait):
                    lk_results = run_lk_monitor_checks()
            except ChromeBusyError as exc:
                lk_skipped_busy = True
                lk_results = []
                print(f"SKIP LK: {exc}")
            for item in lk_results:
                st = "OK" if item.success else "FAIL"
                print(f"[{st}] {item.name} {item.duration_ms:.0f}ms {item.error}")
            if lk_results:
                lk_ok = all(item.success for item in lk_results)
            elif not lk_skipped_busy:
                lk_ok = False
            if lk_results:
                all_results.extend(lk_results)
    else:
        print("SKIP LK: MONITOR_RUN_LK=false или нет credentials")

    duration_sec = time.perf_counter() - start
    http_ok = landing.success
    overall_ok = http_ok and (lk_ok or not LK_MONITOR_ENABLED or lk_skipped_busy)

    if INFLUX_ENABLED:
        try:
            write_check_results([landing])
            if LK_MONITOR_ENABLED and landing.success and not lk_skipped_busy:
                lk_only = [r for r in all_results if r.name.startswith("lk_")]
                if lk_only:
                    write_lk_check_results(lk_only)
                    write_lk_run(
                        success=lk_ok,
                        failed_count=sum(1 for r in lk_only if not r.success),
                        duration_sec=duration_sec,
                    )
            print("Metrics sent to InfluxDB")
        except Exception as exc:
            print(f"WARN: InfluxDB write failed: {exc}")

    failed_results = [r for r in all_results if not r.success]
    if INFLUX_ENABLED and failed_results:
        try:
            write_failure_events(run_type="health", failures=failures_from_checks(failed_results))
        except Exception as exc:
            print(f"WARN: InfluxDB failure events: {exc}")

    if not overall_ok and should_send_lk_telegram(overall_ok=overall_ok):
        notify_github_on_failure(
            run_type="health",
            http_results=all_results,
            failed_count=sum(1 for r in all_results if not r.success),
            duration_sec=duration_sec,
        )

    print(f"Health monitor finished in {duration_sec:.1f}s — {'OK' if overall_ok else 'FAIL'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
