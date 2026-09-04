#!/usr/bin/env python3
"""
Полный мониторинг BID (cron каждый час):
1. HTTP-проверки публичных API
2. pytest tests/api/ (опционально)
3. метрики → InfluxDB
4. алерт через GitHub → Telegram при ошибках
"""

from __future__ import annotations

import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.alert_policy import notify_full_run_result
from monitor.checks import run_http_checks
from monitor.config import INFLUX_ENABLED, MONITOR_RUN_PYTEST, MONITOR_RUN_UI, PROJECT_ROOT
from monitor.github_dispatch import notify_github_on_failure
from monitor.http_session import create_monitor_session
from monitor.metrics import (
    failures_from_checks,
    write_check_results,
    write_failure_events,
    write_pytest_run,
)
from monitor.probe_alert import should_send_daily_telegram
from monitor.pytest_failures import parse_pytest_failures, pytest_summary_failure


@dataclass
class PytestResult:
    total: int
    passed: int
    failed: int
    errors: int
    duration_sec: float
    output: str
    crashed: bool

    @property
    def pytest_failed(self) -> int:
        return self.failed + self.errors


def _run_pytest() -> PytestResult:
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
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    duration = time.perf_counter() - start
    output = (proc.stdout or "") + (proc.stderr or "")

    passed = failed = errors = 0
    if match := re.search(r"(\d+) passed", output):
        passed = int(match.group(1))
    if match := re.search(r"(\d+) failed", output):
        failed = int(match.group(1))
    if match := re.search(r"(\d+) error", output):
        errors = int(match.group(1))
    total = passed + failed + errors
    crashed = proc.returncode != 0 and total == 0
    if crashed:
        errors = 1

    return PytestResult(
        total=total,
        passed=passed,
        failed=failed,
        errors=errors,
        duration_sec=duration,
        output=output,
        crashed=crashed,
    )


def _pytest_error_snippet(result: PytestResult) -> str:
    lines = [line.strip() for line in result.output.splitlines() if line.strip()]
    tail = "\n".join(lines[-8:])
    if result.crashed:
        return f"Pytest не запустился (ошибка окружения):\n{tail[:400]}"
    if result.pytest_failed:
        return tail[:400]
    return ""


def main() -> int:
    print("=== BID Daily Monitor ===")

    session = create_monitor_session()
    http_results = run_http_checks(session)
    http_failed = [r for r in http_results if not r.success]

    for item in http_results:
        status = "OK" if item.success else "FAIL"
        print(f"[{status}] {item.name} {item.http_code} {item.duration_ms:.0f}ms {item.error}")

    if MONITOR_RUN_PYTEST:
        pytest_result = _run_pytest()
        print(
            f"Pytest: {pytest_result.passed}/{pytest_result.total} passed, "
            f"failed={pytest_result.failed}, errors={pytest_result.errors} "
            f"in {pytest_result.duration_sec:.1f}s"
        )
        if pytest_result.crashed:
            print("Pytest crashed — см. cron.log")
            print(pytest_result.output[-500:])
    else:
        pytest_result = PytestResult(0, 0, 0, 0, 0.0, "", False)
        print("Pytest: skipped (MONITOR_RUN_PYTEST=false)")

    if INFLUX_ENABLED:
        try:
            write_check_results(http_results)
            write_pytest_run(
                total=pytest_result.total,
                passed=pytest_result.passed,
                failed=pytest_result.pytest_failed,
                duration_sec=pytest_result.duration_sec,
            )
            print("Metrics sent to InfluxDB")
        except Exception as exc:
            print(f"WARN: InfluxDB write failed: {exc}")

    failure_events = failures_from_checks(http_failed)
    if pytest_result.pytest_failed:
        parsed = parse_pytest_failures(pytest_result.output)
        failure_events.extend(parsed)
        if not parsed:
            failure_events.append(
                pytest_summary_failure(
                    failed=pytest_result.pytest_failed,
                    total=pytest_result.total,
                    output=pytest_result.output,
                    crashed=pytest_result.crashed,
                )
            )
    if INFLUX_ENABLED and failure_events:
        try:
            write_failure_events(run_type="full", failures=failure_events)
        except Exception as exc:
            print(f"WARN: InfluxDB failure events: {exc}")

    overall_ok = not http_failed and pytest_result.pytest_failed == 0

    notify_full_run_result(
        http_results,
        overall_ok=overall_ok,
        passed=pytest_result.passed,
        total=pytest_result.total,
        pytest_failed=pytest_result.pytest_failed,
        pytest_output=pytest_result.output,
    )

    if not overall_ok and should_send_daily_telegram(overall_ok=overall_ok):
        notify_github_on_failure(
            run_type="full",
            http_results=http_results,
            failed_count=len(http_failed),
            duration_sec=pytest_result.duration_sec,
            pytest_failed=pytest_result.pytest_failed,
            pytest_total=pytest_result.total,
            pytest_error=_pytest_error_snippet(pytest_result),
        )

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
