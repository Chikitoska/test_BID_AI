#!/usr/bin/env python3
"""Проверка данных bid_check в InfluxDB: последнее значение по каждой HTTP-проверке (не вся история)."""

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
success = from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "bid_check" and r._field == "success")
  |> group(columns: ["check"])
  |> last()
  |> rename(columns: {{_value: "success", _time: "checked_at"}})

duration = from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "bid_check" and r._field == "duration_ms")
  |> group(columns: ["check"])
  |> last()
  |> rename(columns: {{_value: "duration_ms"}})
  |> keep(columns: ["check", "duration_ms"])

http = from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "bid_check" and r._field == "http_code")
  |> group(columns: ["check"])
  |> last()
  |> rename(columns: {{_value: "http_code"}})
  |> keep(columns: ["check", "http_code"])

errors = from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "bid_check" and r._field == "error")
  |> group(columns: ["check"])
  |> last()
  |> rename(columns: {{_value: "error"}})
  |> keep(columns: ["check", "error"])

sd = join(tables: {{s: success, d: duration}}, on: ["check"])
sdh = join(tables: {{sd: sd, h: http}}, on: ["check"])
join(tables: {{sdh: sdh, e: errors}}, on: ["check"])
  |> sort(columns: ["order", "check"], desc: false)
'''
    try:
        from influxdb_client import InfluxDBClient
    except ModuleNotFoundError:
        print("ERROR: influxdb_client не установлен")
        print("Запускайте через venv: .venv/bin/python monitor/verify_influx_table.py")
        print("или: ./monitor/verify_influx_table.sh")
        return 1

    print(f"InfluxDB: {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        tables = client.query_api().query(query, org=INFLUXDB_ORG)
        rows = 0
        for table in tables:
            for record in table.records:
                rows += 1
                print(dict(record.values))
        print(f"Rows: {rows} (по одной последней записи на каждый тип проверки, не вся история)")
        print("Полная история: bash monitor/verify_influx_history.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
