#!/usr/bin/env python3
"""Сколько точек в Influx по каждому прогону (история, не last())."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from influxdb_client import InfluxDBClient  # noqa: E402
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL  # noqa: E402


def main() -> int:
    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1

    days = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    print(f"InfluxDB: {INFLUXDB_URL} bucket={INFLUXDB_BUCKET} (последние {days} дн.)")
    print()

    query = f'''
import "date"
start = date.sub(d: {days}d, from: now())

from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: start)
  |> filter(fn: (r) =>
      r._measurement == "bid_lk_run" or
      r._measurement == "bid_run" or
      r._measurement == "bid_lk_pytest" or
      r._measurement == "bid_probe" or
      r._measurement == "bid_check" or
      r._measurement == "bid_failure"
  )
  |> group(columns: ["_measurement"])
  |> count()
  |> sort(columns: ["_value"], desc: true)
'''

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        tables = client.query_api().query(query, org=INFLUXDB_ORG)
        rows = 0
        for table in tables:
            for record in table.records:
                rows += 1
                measurement = record.values.get("_measurement", "?")
                count = record.values.get("_value", 0)
                print(f"  {measurement:16} {count:6} точек")

        if rows == 0:
            print("  (пусто — мониторинг не писал метрики за период)")
            return 1

    print()
    print("bid_lk_run     — health каждые 5 мин (график ①)")
    print("bid_run        — daily 2×/день (график ②)")
    print("bid_lk_pytest  — pytest ЛК каждые 2 ч (график ③)")
    print("bid_check      — детали HTTP (verify_influx_table, не графики)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
