#!/usr/bin/env python3
"""
Ежедневный мониторинг BID:
1. HTTP-проверки публичных API
2. pytest tests/api/
3. метрики → InfluxDB
4. алерт в Telegram при ошибках
"""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.alert_policy import notify_full_run_result
from monitor.checks import run_http_checks
from monitor.config import INFLUX_ENABLED, MONITOR_RUN_UI, PROJECT_ROOT
from monitor.http_session import create_monitor_session
from monitor.metrics import write_check_results, write_pytest_run


def _run_pytest() -> tuple[int, int, int, float, str]:
    """Запуск pytest, возвращает total, passed, failed, duration, output."""
    test_paths = ["tests/api/"]
    if MONITOR_RUN_UI:
        test_paths.append(
            "tests/ui/selenium_ui/test_landing_scenarios.py::"
            "TestLandingScenariosSelenium::test_scenario_01_landing_opens"
        )

    cmd = [
        str(PROJECT_ROOT / ".venv" / "bin" / "pytest"),
        *test_paths,
        "-q",
        "--tb=line",
    ]
    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    duration = time.perf_counter() - start
    output = (proc.stdout or "") + (proc.stderr or "")

    passed = failed = 0
    match = re.search(r"(\d+) passed", output)
    if match:
        passed = int(match.group(1))
    match = re.search(r"(\d+) failed", output)
    if match:
        failed = int(match.group(1))
    total = passed + failed
    if total == 0 and proc.returncode != 0:
        failed = 1

    return total, passed, failed, duration, output


def main() -> int:
    print("=== BID Daily Monitor ===")

    session = create_monitor_session()
    http_results = run_http_checks(session)
    http_failed = [r for r in http_results if not r.success]

    for item in http_results:
        status = "OK" if item.success else "FAIL"
        print(f"[{status}] {item.name} {item.http_code} {item.duration_ms:.0f}ms {item.error}")

    total, passed, failed, pytest_duration, pytest_output = _run_pytest()
    print(f"Pytest: {passed}/{total} passed in {pytest_duration:.1f}s")

    if INFLUX_ENABLED:
        try:
            write_check_results(http_results)
            write_pytest_run(
                total=total,
                passed=passed,
                failed=failed,
                duration_sec=pytest_duration,
            )
            print("Metrics sent to InfluxDB")
        except Exception as exc:
            print(f"WARN: InfluxDB write failed: {exc}")
    else:
        print("WARN: INFLUXDB_TOKEN не задан — метрики не записаны")

    overall_ok = not http_failed and failed == 0

    notify_full_run_result(
        http_results,
        overall_ok=overall_ok,
        passed=passed,
        total=total,
        pytest_failed=failed,
        pytest_output=pytest_output,
    )

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
