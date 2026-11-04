#!/usr/bin/env python3
"""WRITE-only: восстановить графики после wipe WAL. Без delete, без писем.

Источники (на VPS после git pull):
  - monitor/restore_gap_20261102.json  (health/combat до 03:34Z 3.11)
  - overnight combat 20:23–06:23 МСК
  - daily 17:01 2.11 и 05:01 3.11 МСК
  - monitor/health.log, cron.log, lk-pytest.log — только слоты с датой
  - 13:02 МСК 3.11: bid_lk_run fail + 2 строки bid_failure

Неизвестные слоты НЕ красим в зелёный. 13:02 не переписываем в success=1.
Restore не шлёт email.

  cd /opt/test_BID_AI
  .venv/bin/python monitor/restore_influx_now.py
  .venv/bin/python monitor/restore_influx_now.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL

SNAPSHOT = PROJECT_ROOT / "monitor" / "restore_gap_20261102.json"
HEALTH_LOG = PROJECT_ROOT / "monitor" / "health.log"
CRON_LOG = PROJECT_ROOT / "monitor" / "cron.log"
COMBAT_LOG = PROJECT_ROOT / "monitor" / "lk-pytest.log"

FAIL_RUN_STAMP = datetime(2026, 11, 3, 10, 2, 46, 852000, tzinfo=timezone.utc)
FAIL_EVIDENCE_STAMP = datetime(2026, 11, 3, 10, 2, 46, 852563, tzinfo=timezone.utc)
FAIL_SLOT_START = datetime(2026, 11, 3, 10, 2, 0, tzinfo=timezone.utc)
FAIL_SLOT_STOP = datetime(2026, 11, 3, 10, 3, 0, tzinfo=timezone.utc)

# 20:23, 22:23 2.11; 00:23, 02:23, 04:23, 06:23 3.11 МСК — pytest 10/10, Influx ENOSPC.
OVERNIGHT_COMBAT = (
    "2026-11-02T17:23:05+00:00",
    "2026-11-02T19:23:05+00:00",
    "2026-11-02T21:23:05+00:00",
    "2026-11-02T23:23:05+00:00",
    "2026-11-03T01:23:05+00:00",
    "2026-11-03T03:23:05+00:00",
)

# 2.11 17:01 МСК и 3.11 05:01 МСК — pytest 39/39, WAL full.
MISSING_DAILY = (
    "2026-11-02T14:01:36+00:00",
    "2026-11-03T02:01:16+00:00",
)

_HEALTH_RUN_LABEL = "Лендинг + мин ЛК (каждые 5 мин)"
_FAILURES: tuple[tuple[str, str, str], ...] = (
    (
        "landing_chatbot_topics",
        "Лендинг: темы чат-бота",
        "landing_chatbot_topics | landing | https://bid.gazprom-neft.ru/ | "
        "Лендинг: после открытия чата темы не отображаются. Текст: "
        "'Ассистент\\nНеизвестная ошибка\\n\\n"
        "Сейчас ассистент недоступен — попробуйте вернуться позже или обратитесь в поддержку'",
    ),
    (
        "lk_auth_login",
        "ЛК: вход (логин + 2FA)",
        "lk_auth_login | lk | https://lk.bid.gazprom-neft.ru/error/500 | HTTP 500 | "
        "ЛК вернул HTTP error page после входа, "
        "URL: https://lk.bid.gazprom-neft.ru/error/500",
    ),
)

_DATE_RE = re.compile(
    r"Date:\s+([A-Za-z]{3}, \d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} GMT)"
)
_HEALTH_DONE_RE = re.compile(
    r"Health monitor finished in ([\d.]+)s — (\S+) \(run_status=(\w+)\)"
)
_COMBAT_DONE_RE = re.compile(
    r"LK pytest: (\d+)/(\d+) passed, failed=(\d+), errors=(\d+).*?in ([\d.]+)s"
)
_DAILY_PYTEST_RE = re.compile(
    r"Pytest: (\d+)/(\d+) passed, failed=(\d+), errors=(\d+) in ([\d.]+)s"
)
_RUN_STATUS_RE = re.compile(r"Metrics sent to InfluxDB \(run_status=(\w+)\)")


@dataclass
class RunPoint:
    measurement: str
    time: datetime
    success: int
    run_status: str
    skipped: int = 0
    total: int = 0
    passed: int = 0
    failed: int = 0
    duration_sec: float = 30.0
    failed_checks: int = 0
    source: str = ""


def _ts(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)


def in_fail_1302_slot(stamp: datetime) -> bool:
    value = stamp.astimezone(timezone.utc)
    return FAIL_SLOT_START <= value < FAIL_SLOT_STOP


def _parse_http_date(block: str) -> datetime | None:
    matches = _DATE_RE.findall(block)
    if not matches:
        return None
    try:
        parsed = parsedate_to_datetime(matches[-1])
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def points_from_snapshot(data: dict) -> list[RunPoint]:
    points: list[RunPoint] = []
    for row in data.get("health") or []:
        success = int(row["success"])
        points.append(
            RunPoint(
                measurement="bid_lk_run",
                time=_ts(row["t"]),
                success=success,
                run_status=str(row.get("run_status") or ("ok" if success else "fail")),
                skipped=int(row.get("skipped") or 0),
                failed_checks=0 if success else 1,
                duration_sec=30.0,
                source="snapshot",
            )
        )
    for row in data.get("combat") or []:
        success = int(row["success"])
        points.append(
            RunPoint(
                measurement="bid_lk_pytest",
                time=_ts(row["t"]),
                success=success,
                run_status=str(row.get("run_status") or ("ok" if success else "fail")),
                total=int(row.get("total") or 10),
                passed=int(row.get("passed") or 10),
                failed=int(row.get("failed") or 0),
                duration_sec=180.0,
                source="snapshot",
            )
        )
    return points


def points_from_overnight_combat() -> list[RunPoint]:
    return [
        RunPoint(
            measurement="bid_lk_pytest",
            time=_ts(raw),
            success=1,
            run_status="ok",
            total=10,
            passed=10,
            failed=0,
            duration_sec=180.0,
            source="overnight",
        )
        for raw in OVERNIGHT_COMBAT
    ]


def points_from_missing_daily() -> list[RunPoint]:
    return [
        RunPoint(
            measurement="bid_run",
            time=_ts(raw),
            success=1,
            run_status="ok",
            total=39,
            passed=39,
            failed=0,
            duration_sec=10.0,
            source="daily-missing",
        )
        for raw in MISSING_DAILY
    ]


def points_from_health_log(text: str) -> list[RunPoint]:
    points: list[RunPoint] = []
    blocks = re.split(r"(?=^=== BID Health Monitor)", text, flags=re.M)
    for block in blocks:
        if "Health monitor finished" not in block:
            continue
        stamp = _parse_http_date(block)
        done = _HEALTH_DONE_RE.search(block)
        if stamp is None or done is None:
            continue
        duration_sec = float(done.group(1))
        run_status = done.group(3)
        lower = block.lower()
        assistant_down = "ассистент недоступен" in lower
        http_5xx = bool(re.search(r"http 5\d\d|/error/5", lower))
        if assistant_down or http_5xx:
            run_status = "fail"
            success = 0
            failed_checks = 1
        elif run_status == "ok":
            success = 1
            failed_checks = 0
        else:
            success = 0
            failed_checks = 1
        points.append(
            RunPoint(
                measurement="bid_lk_run",
                time=stamp,
                success=success,
                run_status=run_status,
                skipped=1 if "skipped_busy" in block.lower() or "chrome busy" in lower else 0,
                failed_checks=failed_checks,
                duration_sec=duration_sec,
                source="health.log",
            )
        )
    return points


def points_from_combat_log(text: str) -> list[RunPoint]:
    points: list[RunPoint] = []
    blocks = re.split(r"(?=^=== BID LK Full Pytest)", text, flags=re.M)
    for block in blocks:
        if "LK pytest:" not in block:
            continue
        stamp = _parse_http_date(block)
        done = _COMBAT_DONE_RE.search(block)
        if stamp is None or done is None:
            continue
        passed = int(done.group(1))
        total = int(done.group(2))
        failed = int(done.group(3)) + int(done.group(4))
        duration_sec = float(done.group(5))
        success = 1 if failed == 0 and total > 0 else 0
        points.append(
            RunPoint(
                measurement="bid_lk_pytest",
                time=stamp,
                success=success,
                run_status="ok" if success else "fail",
                total=total,
                passed=passed,
                failed=failed,
                duration_sec=duration_sec,
                source="lk-pytest.log",
            )
        )
    return points


def points_from_cron_log(text: str) -> list[RunPoint]:
    points: list[RunPoint] = []
    blocks = re.split(r"(?=^=== BID Daily Monitor)", text, flags=re.M)
    for block in blocks:
        if "Pytest:" not in block:
            continue
        stamp = _parse_http_date(block)
        pytest = _DAILY_PYTEST_RE.search(block)
        if stamp is None or pytest is None:
            continue
        passed = int(pytest.group(1))
        total = int(pytest.group(2))
        failed = int(pytest.group(3)) + int(pytest.group(4))
        duration_sec = float(pytest.group(5))
        status_match = _RUN_STATUS_RE.search(block)
        success = 1 if failed == 0 and total > 0 else 0
        run_status = status_match.group(1) if status_match else ("ok" if success else "fail")
        points.append(
            RunPoint(
                measurement="bid_run",
                time=stamp,
                success=success,
                run_status=run_status,
                total=total,
                passed=passed,
                failed=failed,
                duration_sec=duration_sec,
                source="cron.log",
            )
        )
    return points


def fail_1302_run() -> RunPoint:
    return RunPoint(
        measurement="bid_lk_run",
        time=FAIL_RUN_STAMP,
        success=0,
        run_status="fail",
        skipped=0,
        failed_checks=1,
        duration_sec=120.0,
        source="13:02-fail",
    )


def failure_1302_points() -> list[Point]:
    points = []
    for check, label, error in _FAILURES:
        points.append(
            Point("bid_failure")
            .tag("run_type", "health")
            .tag("run_label", _HEALTH_RUN_LABEL)
            .tag("check", check[:128])
            .tag("label", label[:256])
            .field("error", error[:2000])
            .time(FAIL_EVIDENCE_STAMP)
        )
    return points


def _merge_key(point: RunPoint) -> tuple[str, str]:
    return (point.measurement, point.time.astimezone(timezone.utc).isoformat())


def collect_run_points(*, snapshot: dict | None, logs: dict[str, str]) -> list[RunPoint]:
    """Собрать точки. 13:02 fail всегда; success=1 в этой минуте отбрасывается."""
    merged: dict[tuple[str, str], RunPoint] = {}

    def add(point: RunPoint) -> None:
        if point.measurement == "bid_lk_run" and in_fail_1302_slot(point.time):
            if point.success == 1:
                return
            if point.source != "13:02-fail":
                # Не затираем канонический fail другой точкой той же минуты.
                return
        merged[_merge_key(point)] = point

    if snapshot:
        for point in points_from_snapshot(snapshot):
            add(point)
    for point in points_from_overnight_combat():
        add(point)
    for point in points_from_missing_daily():
        add(point)
    for point in points_from_health_log(logs.get("health") or ""):
        add(point)
    for point in points_from_combat_log(logs.get("combat") or ""):
        add(point)
    for point in points_from_cron_log(logs.get("cron") or ""):
        add(point)
    add(fail_1302_run())
    return sorted(merged.values(), key=lambda item: (item.measurement, item.time))


def to_influx_point(point: RunPoint) -> Point:
    if point.measurement == "bid_lk_run":
        return (
            Point("bid_lk_run")
            .tag("run_status", point.run_status[:32])
            .field("success", int(point.success))
            .field("skipped", int(point.skipped))
            .field("failed_checks", int(point.failed_checks))
            .field("duration_sec", float(point.duration_sec))
            .time(point.time)
        )
    if point.measurement == "bid_run":
        return (
            Point("bid_run")
            .tag("run_status", point.run_status[:32])
            .field("total", int(point.total))
            .field("passed", int(point.passed))
            .field("failed", int(point.failed))
            .field("success", int(point.success))
            .field("duration_sec", float(point.duration_sec))
            .time(point.time)
        )
    return (
        Point("bid_lk_pytest")
        .tag("run_status", point.run_status[:32])
        .field("total", int(point.total))
        .field("passed", int(point.passed))
        .field("failed", int(point.failed))
        .field("success", int(point.success))
        .field("duration_sec", float(point.duration_sec))
        .time(point.time)
    )


def load_snapshot() -> dict | None:
    if not SNAPSHOT.is_file():
        print(f"WARN: нет снимка {SNAPSHOT} — health до 06:30 МСК останется пустым")
        return None
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def _count_by_measurement(points: list[RunPoint]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for point in points:
        counts[point.measurement] = counts.get(point.measurement, 0) + 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="WRITE-only restore health/daily/combat + 13:02 fail (no delete, no email)"
    )
    parser.add_argument("--apply", action="store_true", help="Записать точки (без delete)")
    args = parser.parse_args()

    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1

    snapshot = load_snapshot()
    logs = {
        "health": _read_text(HEALTH_LOG),
        "cron": _read_text(CRON_LOG),
        "combat": _read_text(COMBAT_LOG),
    }
    missing_logs = [
        name
        for name, text in (
            ("health.log", logs["health"]),
            ("cron.log", logs["cron"]),
            ("lk-pytest.log", logs["combat"]),
        )
        if not text.strip()
    ]
    if missing_logs:
        print("WARN: нет логов, слоты после снимка не восстановим:", ", ".join(missing_logs))

    run_points = collect_run_points(snapshot=snapshot, logs=logs)
    fail_points = failure_1302_points()
    counts = _count_by_measurement(run_points)
    print(f"Influx {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    print("WRITE-only, no delete, no email replay")
    print(
        "would write:",
        f"bid_lk_run={counts.get('bid_lk_run', 0)}",
        f"bid_run={counts.get('bid_run', 0)}",
        f"bid_lk_pytest={counts.get('bid_lk_pytest', 0)}",
        f"bid_failure={len(fail_points)} (13:02)",
    )
    fail_run = next(p for p in run_points if p.source == "13:02-fail")
    print(
        "13:02 kept FAIL:",
        fail_run.time.isoformat(),
        f"success={fail_run.success}",
        f"run_status={fail_run.run_status}",
    )
    if any(p.measurement == "bid_lk_run" and in_fail_1302_slot(p.time) and p.success == 1 for p in run_points):
        print("ERROR: 13:02 painted green — abort")
        return 1
    print("apply" if args.apply else "dry-run (без --apply ничего не пишем)")
    if not args.apply:
        return 0

    records: list[Point] = [to_influx_point(point) for point in run_points]
    records.extend(fail_points)
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        batch = 50
        for i in range(0, len(records), batch):
            chunk = records[i : i + batch]
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=chunk)
            print(f"  wrote {i + len(chunk)}/{len(records)}")
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
