#!/usr/bin/env python3
"""Дописать daily-столбцы, которые прогон сделал, а Influx не записал (диск 100%).

  2.11 17:01 МСК и 3.11 05:01 МСК — pytest 39/39, Минцифр OK.
  cd /opt/test_BID_AI && .venv/bin/python monitor/rewrite_missing_daily.py --apply
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL

# Date из ответа Influx « WAL write (UTC).
TARGETS = (
    datetime.fromisoformat("2026-11-02T14:01:36+00:00"),
    datetime.fromisoformat("2026-11-03T02:01:16+00:00"),
)
WINDOW = timedelta(seconds=5)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1

    print(f"Influx {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    print("apply" if args.apply else "dry-run")

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()
        for stamp in TARGETS:
            start, stop = stamp - WINDOW, stamp + WINDOW
            flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: time(v: "{start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"), stop: time(v: "{stop.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"))
  |> filter(fn: (r) => r._measurement == "bid_run")
  |> pivot(rowKey: ["_time", "run_status"], columnKey: ["_field"], valueColumn: "_value")
'''
            existing = [r for tab in query_api.query(flux, org=INFLUXDB_ORG) for r in tab.records]
            print(f"\n=== {stamp.isoformat()} existing={len(existing)} ===")
            if existing:
                print("SKIP: точка уже есть", existing[0].values)
                continue
            if not args.apply:
                print("dry-run: написали бы bid_run ok 39/39")
                continue
            point = (
                Point("bid_run")
                .tag("run_status", "ok")
                .field("total", 39)
                .field("passed", 39)
                .field("failed", 0)
                .field("success", 1)
                .field("duration_sec", 10.0)
                .time(stamp)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print("  -> ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
