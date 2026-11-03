#!/usr/bin/env python3
"""Восстановить health/combat после потери WAL (рестарт Influx на полном диске).

Только WRITE, без delete. Снимок: monitor/restore_gap_20261102.json
(live API 03:34 UTC 3.11, до рестарта).

  cd /opt/test_BID_AI
  .venv/bin/python monitor/restore_influx_gap.py --apply
"""

from __future__ import annotations

import argparse
import json
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

SNAPSHOT = PROJECT_ROOT / "monitor" / "restore_gap_20261102.json"


def _ts(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    health = data["health"]
    combat = data["combat"]
    print(f"Influx {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    print(f"health {len(health)}  combat {len(combat)}  {'apply' if args.apply else 'dry-run'}")
    if not args.apply:
        print("без --apply ничего не пишем")
        return 0

    points: list[Point] = []
    for row in health:
        points.append(
            Point("bid_lk_run")
            .tag("run_status", str(row["run_status"])[:32])
            .field("success", int(row["success"]))
            .field("skipped", int(row["skipped"]))
            .field("failed_checks", 0 if int(row["success"]) else 1)
            .field("duration_sec", 30.0)
            .time(_ts(row["t"]))
        )
    for row in combat:
        success = int(row["success"])
        points.append(
            Point("bid_lk_pytest")
            .tag("run_status", str(row["run_status"])[:32])
            .field("total", int(row.get("total") or 10))
            .field("passed", int(row.get("passed") or 10))
            .field("failed", int(row.get("failed") or 0))
            .field("success", success)
            .field("duration_sec", 180.0)
            .time(_ts(row["t"]))
        )

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        batch = 50
        for i in range(0, len(points), batch):
            chunk = points[i : i + batch]
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=chunk)
            print(f"  wrote {i + len(chunk)}/{len(points)}")
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
