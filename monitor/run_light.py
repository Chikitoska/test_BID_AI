#!/usr/bin/env python3
"""
Быстрый prod-probe BID (только HTTP):
- каждые 10 минут через cron
- Grafana: OK и FAIL (после retry)
- Telegram: только подтверждённый сбой (anti-flap + GitHub relay)
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.checks import run_http_checks
from monitor.config import INFLUX_ENABLED, MONITOR_PROBE_RETRIES, MONITOR_PROBE_RETRY_DELAY_SEC
from monitor.github_dispatch import notify_github_on_failure
from monitor.http_session import create_monitor_session
from monitor.metrics import write_check_results, write_probe_run
from monitor.probe_alert import notify_probe_failure_direct, should_send_probe_telegram


def _run_checks_with_retry(session):
    results = run_http_checks(session)
    if all(item.success for item in results) or MONITOR_PROBE_RETRIES <= 0:
        return results

    print(
        f"Probe failed ({sum(1 for r in results if not r.success)} checks), "
        f"retry in {MONITOR_PROBE_RETRY_DELAY_SEC}s..."
    )
    time.sleep(MONITOR_PROBE_RETRY_DELAY_SEC)
    return run_http_checks(session)


def main() -> int:
    print("=== BID Probe (HTTP) ===")
    start = time.perf_counter()

    session = create_monitor_session()
    http_results = _run_checks_with_retry(session)
    http_failed = [r for r in http_results if not r.success]

    for item in http_results:
        status = "OK" if item.success else "FAIL"
        print(f"[{status}] {item.name} {item.http_code} {item.duration_ms:.0f}ms {item.error}")

    duration_sec = time.perf_counter() - start
    overall_ok = not http_failed

    if INFLUX_ENABLED:
        try:
            write_check_results(http_results)
            write_probe_run(
                success=overall_ok,
                failed_count=len(http_failed),
                duration_sec=duration_sec,
            )
            print("Metrics sent to InfluxDB")
        except Exception as exc:
            print(f"WARN: InfluxDB write failed: {exc}")

    send_telegram_alert = should_send_probe_telegram(overall_ok=overall_ok)
    if send_telegram_alert:
        notify_github_on_failure(
            run_type="probe",
            http_results=http_results,
            failed_count=len(http_failed),
            duration_sec=duration_sec,
        )
        notify_probe_failure_direct(http_results)

    print(f"Probe finished in {duration_sec:.1f}s — {'OK' if overall_ok else 'FAIL'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
