#!/usr/bin/env python3
"""Ручной прогон страницы Минцифр (в cron входит в run_daily, 2 раза в день)."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.chrome_lock import ChromeBusyError, chrome_run_lock
from monitor.config import INFLUX_ENABLED
from monitor.github_dispatch import notify_github_on_failure
from monitor.lk_checks import run_mincifry_checks
from monitor.metrics import failures_from_checks, write_check_results, write_failure_events


def main() -> int:
    print("=== BID Минцифр (ручной прогон) ===")
    start = time.perf_counter()
    wait_sec = float(os.getenv("CHROME_LOCK_WAIT_HEALTH_SEC", "120"))
    try:
        with chrome_run_lock(owner="mincifry", wait_sec=wait_sec):
            results = run_mincifry_checks()
    except ChromeBusyError as exc:
        print(f"SKIP Минцифр (chrome busy): {exc}")
        return 0

    for item in results:
        st = "OK" if item.success else "FAIL"
        print(f"[{st}] {item.name} {item.duration_ms:.0f}ms {item.error}")

    duration_sec = time.perf_counter() - start
    overall_ok = bool(results) and all(item.success for item in results)

    if INFLUX_ENABLED:
        try:
            write_check_results(results)
            failed = [r for r in results if not r.success]
            if failed:
                write_failure_events(run_type="mincifry", failures=failures_from_checks(failed))
            print("Metrics sent to InfluxDB")
        except Exception as exc:
            print(f"WARN: InfluxDB write failed: {exc}")

    if not overall_ok:
        # Ручной скрипт по умолчанию не спамит почту; алерты — из run_daily.
        if os.getenv("MINCIFRY_ALERT", "false").lower() in ("1", "true", "yes"):
            notify_github_on_failure(
                run_type="mincifry",
                http_results=results,
                failed_count=sum(1 for r in results if not r.success),
                duration_sec=duration_sec,
            )
        else:
            print("Alert skipped (ручной прогон). Для письма: MINCIFRY_ALERT=true")
        print(f"Mincifry finished in {duration_sec:.1f}s — FAIL")
        return 1

    print(f"Mincifry finished in {duration_sec:.1f}s — OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
