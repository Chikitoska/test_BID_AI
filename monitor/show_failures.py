#!/usr/bin/env python3
"""Показать последние записи bid_failure из InfluxDB (для отладки Grafana)."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from influxdb_client import InfluxDBClient  # noqa: E402
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL  # noqa: E402

RUN_NAMES = {
    "health": "Лендинг + мин ЛК (5 мин)",
    "full": "Лендинг + API autotests",
    "lk_pytest": "Боевой прогон ЛК (2 ч)",
}


def main() -> int:
    if not INFLUXDB_TOKEN:
        print("INFLUXDB_TOKEN не задан")
        return 1

    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    run_type = sys.argv[2] if len(sys.argv) > 2 else ""
    start = datetime.now(timezone.utc) - timedelta(hours=hours)

    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: {start.isoformat()})
  |> filter(fn: (r) => r._measurement == "bid_failure" and r._field == "error")
'''
    if run_type:
        flux += f'  |> filter(fn: (r) => r.run_type == "{run_type}")\n'
    flux += """
  |> sort(columns: ["_time"], desc: true)
  |> limit(n: 30)
"""

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        tables = client.query_api().query(flux)

    rows = []
    for table in tables:
        for record in table.records:
            tags = record.values
            rows.append(
                (
                    record.get_time(),
                    tags.get("run_type", "?"),
                    tags.get("check", ""),
                    tags.get("label", ""),
                    record.get_value(),
                )
            )

    if not rows:
        print(f"За последние {hours} ч записей bid_failure не найдено")
        if run_type:
            print(f"(фильтр run_type={run_type})")
        return 0

    print(f"Последние ошибки bid_failure (за {hours} ч):\n")
    for ts, rt, check, label, error in rows:
        name = RUN_NAMES.get(rt, rt)
        err = (error or "").replace("\n", " ")[:300]
        print(f"{ts} | {name}")
        print(f"  check: {check}")
        print(f"  label: {label}")
        print(f"  error: {err}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
