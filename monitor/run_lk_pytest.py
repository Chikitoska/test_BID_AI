#!/usr/bin/env python3
"""
Полный регресс ЛК (pytest tests/lk/ + Allure).

Боевой прогон 2 раза в день — не prod-мониторинг, а детальная проверка UI.
Результаты: allure-results/lk-YYYYMMDD-HHMM/
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.config import INFLUX_ENABLED, PROJECT_ROOT as CFG_ROOT
from monitor.chrome_lock import ChromeBusyError, chrome_run_lock
from monitor.github_dispatch import notify_github_on_failure
from monitor.metrics import FailureEvent, write_failure_events, write_lk_pytest_run
from monitor.probe_alert import should_send_daily_telegram
from monitor.pytest_failures import parse_pytest_failures, pytest_failure_snippet, pytest_summary_failure


@dataclass
class PytestResult:
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration_sec: float
    output: str
    allure_dir: Path

    @property
    def pytest_failed(self) -> int:
        return self.failed + self.errors


def _run_lk_pytest() -> PytestResult:
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    allure_dir = PROJECT_ROOT / "allure-results" / f"lk-{stamp}"
    allure_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(CFG_ROOT / ".venv" / "bin" / "pytest"),
        "tests/lk/",
        "-v",
        "--tb=short",
        "--reruns",
        "2",
        "--reruns-delay",
        "10",
        "--only-rerun",
        "WebDriverException",
        "--only-rerun",
        "InvalidSessionIdException",
        "--only-rerun",
        "TimeoutException",
        f"--alluredir={allure_dir}",
    ]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    duration = time.perf_counter() - start
    output = (proc.stdout or "") + (proc.stderr or "")

    passed = failed = skipped = errors = 0
    if match := re.search(r"(\d+) passed", output):
        passed = int(match.group(1))
    if match := re.search(r"(\d+) failed", output):
        failed = int(match.group(1))
    if match := re.search(r"(\d+) skipped", output):
        skipped = int(match.group(1))
    if match := re.search(r"(\d+) error", output):
        errors = int(match.group(1))

    return PytestResult(
        total=passed + failed + skipped + errors,
        passed=passed,
        failed=failed,
        skipped=skipped,
        errors=errors,
        duration_sec=duration,
        output=output,
        allure_dir=allure_dir,
    )


def main() -> int:
    print("=== BID LK Full Pytest (Allure) ===", flush=True)
    lk_wait = float(os.getenv("CHROME_LOCK_WAIT_LK_PYTEST_SEC", "900"))
    try:
        with chrome_run_lock(owner="lk_pytest", wait_sec=lk_wait):
            print("Запуск pytest tests/lk/ … обычно 4–5 мин, подождите", flush=True)
            result = _run_lk_pytest()
    except ChromeBusyError as exc:
        print(f"FAIL: {exc}", flush=True)
        if INFLUX_ENABLED:
            try:
                write_lk_pytest_run(total=0, passed=0, failed=1, duration_sec=0.0)
                write_failure_events(
                    run_type="lk_pytest",
                    failures=[
                        FailureEvent(
                            check="chrome_lock",
                            label="Chrome занят другим прогоном",
                            error=str(exc)[:2000],
                        )
                    ],
                )
                print("Pytest metrics + failure sent to InfluxDB")
            except Exception as write_exc:
                print(f"WARN: InfluxDB write failed: {write_exc}")
        return 1

    print(result.output[-3000:] if len(result.output) > 3000 else result.output)
    print(
        f"LK pytest: {result.passed}/{result.total} passed, "
        f"failed={result.failed}, errors={result.errors}, skipped={result.skipped} "
        f"in {result.duration_sec:.1f}s"
    )
    print(f"Allure results: {result.allure_dir}")

    if INFLUX_ENABLED:
        try:
            write_lk_pytest_run(
                total=result.total,
                passed=result.passed,
                failed=result.pytest_failed,
                duration_sec=result.duration_sec,
            )
            print("Pytest metrics sent to InfluxDB")
        except Exception as exc:
            print(f"WARN: InfluxDB write failed: {exc}")

    failure_events = parse_pytest_failures(result.output)
    overall_ok = result.pytest_failed == 0 and result.total > 0

    if result.pytest_failed and not failure_events:
        failure_events = [
            pytest_summary_failure(
                failed=result.pytest_failed,
                total=result.total,
                output=result.output,
            )
        ]
    elif not overall_ok and not failure_events:
        # pytest упал/не стартовал (total=0) — на графике FAIL, но раньше таблица была пустой
        failure_events = [
            pytest_summary_failure(
                failed=max(result.pytest_failed, 1),
                total=result.total,
                output=result.output,
                crashed=result.total == 0,
            )
        ]

    if INFLUX_ENABLED and failure_events:
        try:
            write_failure_events(run_type="lk_pytest", failures=failure_events)
            print("Failure events sent to InfluxDB (таблица Grafana)")
        except Exception as exc:
            print(f"WARN: InfluxDB failure events: {exc}")

    if not overall_ok and should_send_daily_telegram(overall_ok=overall_ok):
        notify_github_on_failure(
            run_type="lk_pytest",
            http_results=[],
            failed_count=result.pytest_failed,
            duration_sec=result.duration_sec,
            pytest_failed=result.pytest_failed,
            pytest_total=result.total,
            pytest_error=pytest_failure_snippet(result.output),
        )

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
