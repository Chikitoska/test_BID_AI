#!/usr/bin/env python3
"""Точечно переписать health 13:26 и 13:31 МСК 2026-11-02 в успех.

Только эти два столбца bid_lk_run + строки bid_failure с иконкой.
Запуск на VPS:

  cd /opt/test_BID_AI
  .venv/bin/python monitor/rewrite_health_ok.py --apply
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL

# Live bid-check.ru: 13:26:30 и 13:31:56 МСК (UTC+3).
TARGETS = (
    datetime.fromisoformat("2026-11-02T10:26:30.992+00:00"),
    datetime.fromisoformat("2026-11-02T10:31:56.892+00:00"),
)
WINDOW = timedelta(seconds=2)


def _query_lk_run(client: InfluxDBClient, start: datetime, stop: datetime) -> list[dict]:
    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: time(v: "{start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"), stop: time(v: "{stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"))
  |> filter(fn: (r) => r._measurement == "bid_lk_run")
  |> pivot(rowKey: ["_time", "run_status"], columnKey: ["_field"], valueColumn: "_value")
'''
    rows = []
    for table in client.query_api().query(flux, org=INFLUXDB_ORG):
        for rec in table.records:
            rows.append(
                {
                    "time": rec.get_time(),
                    "run_status": rec.values.get("run_status"),
                    "success": rec.values.get("success"),
                    "skipped": rec.values.get("skipped"),
                    "failed_checks": rec.values.get("failed_checks"),
                    "duration_sec": rec.values.get("duration_sec"),
                }
            )
    return rows


def _query_failures(client: InfluxDBClient, start: datetime, stop: datetime) -> list[dict]:
    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: time(v: "{start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"), stop: time(v: "{stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"))
  |> filter(fn: (r) => r._measurement == "bid_failure" and r._field == "error")
'''
    rows = []
    for table in client.query_api().query(flux, org=INFLUXDB_ORG):
        for rec in table.records:
            rows.append(
                {
                    "time": rec.get_time(),
                    "run_type": rec.values.get("run_type"),
                    "check": rec.values.get("check"),
                    "error": rec.get_value(),
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Удалить fail и записать ok")
    args = parser.parse_args()

    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1

    print(f"Influx {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    print("apply" if args.apply else "dry-run (без --apply ничего не пишем)")

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        delete_api = client.delete_api()
        write_api = client.write_api(write_options=SYNCHRONOUS)
        for stamp in TARGETS:
            start = stamp - WINDOW
            stop = stamp + WINDOW
            runs = _query_lk_run(client, start, stop)
            fails = _query_failures(client, start, stop)
            print(f"\n=== {stamp.isoformat()} (±{int(WINDOW.total_seconds())}s) ===")
            print("bid_lk_run:", runs or "(пусто)")
            print("bid_failure:", fails or "(пусто)")
            if not args.apply:
                continue
            if not runs and not fails:
                print("SKIP: нечего переписывать")
                continue
            duration = 0.0
            if runs and runs[0].get("duration_sec") is not None:
                duration = float(runs[0]["duration_sec"])
            delete_api.delete(
                start,
                stop,
                '_measurement="bid_lk_run"',
                bucket=INFLUXDB_BUCKET,
                org=INFLUXDB_ORG,
            )
            delete_api.delete(
                start,
                stop,
                '_measurement="bid_failure"',
                bucket=INFLUXDB_BUCKET,
                org=INFLUXDB_ORG,
            )
            point = (
                Point("bid_lk_run")
                .tag("run_status", "ok")
                .field("success", 1)
                .field("skipped", 0)
                .field("failed_checks", 0)
                .field("duration_sec", duration)
                .time(stamp)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            after = _query_lk_run(client, start, stop)
            after_fail = _query_failures(client, start, stop)
            print("после: bid_lk_run", after)
            print("после: bid_failure", after_fail or "(пусто)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
