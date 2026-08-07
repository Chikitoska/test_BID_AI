#!/usr/bin/env python3
"""Проверка данных bid_check в InfluxDB (запуск на сервере)."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL


def main() -> int:
    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        print("Проверьте /opt/test_BID_AI/monitor/.env или /opt/test_BID_AI/.env")
        return 1

    query = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "bid_check")
  |> group(columns: ["check", "label", "_field"])
  |> last()
  |> map(fn: (r) => ({{ r with _value: string(v: r._value) }}))
  |> group()
  |> pivot(rowKey: ["check", "label"], columnKey: ["_field"], valueColumn: "_value")
'''
    from influxdb_client import InfluxDBClient

    print(f"InfluxDB: {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        tables = client.query_api().query(query, org=INFLUXDB_ORG)
        rows = 0
        for table in tables:
            for record in table.records:
                rows += 1
                print(dict(record.values))
        print(f"Rows: {rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
