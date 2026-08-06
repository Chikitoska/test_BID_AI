#!/usr/bin/env python3
"""
Быстрый prod-probe BID (только HTTP):
- каждые 5–10 минут через cron
- алерт в Telegram только при падении / восстановлении
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.alert_policy import notify_probe_result
from monitor.checks import run_http_checks
from monitor.config import INFLUX_ENABLED
from monitor.github_dispatch import notify_github_probe_status
from monitor.http_session import create_monitor_session
from monitor.metrics import write_check_results, write_probe_run


def main() -> int:
    print("=== BID Probe (HTTP) ===")
    start = time.perf_counter()

    session = create_monitor_session()
    http_results = run_http_checks(session)
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

    notify_probe_result(http_results, overall_ok=overall_ok)
    notify_github_probe_status(
        status="ok" if overall_ok else "fail",
        failed_count=len(http_failed),
        duration_sec=duration_sec,
    )

    print(f"Probe finished in {duration_sec:.1f}s — {'OK' if overall_ok else 'FAIL'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
