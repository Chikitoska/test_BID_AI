#!/usr/bin/env python3
"""WRITE-only: один красный бар health 13:02 МСК 2026-11-03.

bid_failure уже есть (lk_auth_login, /error/500, HTTP 500).
write_lk_run в слоте не успел — Overview остался на 12:56 green.

Только WRITE, без delete. Ровно одна точка, ровно этот timestamp.
Запуск на VPS (не с Mac):

  cd /opt/test_BID_AI
  .venv/bin/python monitor/write_health_fail_1302.py
  .venv/bin/python monitor/write_health_fail_1302.py --apply
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

# 13:02:46.852 МСК = 10:02:46.852 UTC. Единственная точка, без диапазона.
STAMP = datetime.fromisoformat("2026-11-03T10:02:46.852+00:00")
if STAMP != datetime(2026, 11, 3, 10, 2, 46, 852000, tzinfo=timezone.utc):
    raise RuntimeError("hard cap: only 2026-11-03T10:02:46.852Z")

# Flux range обязателен для SELECT; пишем не диапазон, а одну точку STAMP.
_QUERY_STOP = STAMP + timedelta(seconds=1)


def _flux_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _query_lk_run(client: InfluxDBClient) -> list[dict]:
    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: time(v: "{_flux_time(STAMP)}"), stop: time(v: "{_flux_time(_QUERY_STOP)}"))
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


def _query_failure_evidence(client: InfluxDBClient) -> list[dict]:
    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: time(v: "{_flux_time(STAMP)}"), stop: time(v: "{_flux_time(_QUERY_STOP)}"))
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


def _fail_point() -> Point:
    # Схема как write_lk_run: tag run_status, fields success/skipped/failed_checks/duration_sec.
    return (
        Point("bid_lk_run")
        .tag("run_status", "fail")
        .field("success", 0)
        .field("skipped", 0)
        .field("failed_checks", 1)
        .field("duration_sec", 120.0)
        .time(STAMP)
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="WRITE-only one bid_lk_run fail at 13:02 MSK 2026-11-03"
    )
    parser.add_argument("--apply", action="store_true", help="Записать одну точку (без delete)")
    args = parser.parse_args()

    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1

    print(f"Influx {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    print("WRITE-only, no delete. Hard cap: 1 point at", STAMP.isoformat())
    print("apply" if args.apply else "dry-run (без --apply ничего не пишем)")

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        before_run = _query_lk_run(client)
        evidence = _query_failure_evidence(client)
        print("before: bid_lk_run:", before_run or "(пусто)")
        print("evidence: bid_failure:", evidence or "(пусто)")
        print(
            "would write: measurement=bid_lk_run time="
            f"{STAMP.isoformat()} run_status=fail success=0 skipped=0 "
            "failed_checks=1 duration_sec=120.0"
        )
        if not args.apply:
            return 0

        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = _fail_point()
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        after_run = _query_lk_run(client)
        print("after: bid_lk_run:", after_run or "(пусто)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
