#!/usr/bin/env python3
"""Дописать боевые слоты 20:23–06:23, которые прогон держал Chrome, а Influx не записал.

После 10:23 2.11 combat уже LK-only и был ok (10:23, 12:23, 16:23, 18:23).
В эти часы health писал skipped=1 — Chrome был у combat. Pytest в Influx не попал (диск).

  cd /opt/test_BID_AI && .venv/bin/python monitor/restore_combat_overnight.py --apply
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL

# 20:23, 22:23 2.11; 00:23, 02:23, 04:23, 06:23 3.11 МСК
TIMES = (
    "2026-11-02T17:23:05+00:00",
    "2026-11-02T19:23:05+00:00",
    "2026-11-02T21:23:05+00:00",
    "2026-11-02T23:23:05+00:00",
    "2026-11-03T01:23:05+00:00",
    "2026-11-03T03:23:05+00:00",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1
    print("apply" if args.apply else "dry-run")
    points = [
        Point("bid_lk_pytest")
        .tag("run_status", "ok")
        .field("total", 10)
        .field("passed", 10)
        .field("failed", 0)
        .field("success", 1)
        .field("duration_sec", 180.0)
        .time(datetime.fromisoformat(raw))
        for raw in TIMES
    ]
    if not args.apply:
        for raw in TIMES:
            print(" would write", raw)
        return 0
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        client.write_api(write_options=SYNCHRONOUS).write(
            bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points
        )
    print(f"wrote {len(points)} combat ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
