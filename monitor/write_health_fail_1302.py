#!/usr/bin/env python3
"""WRITE-only: красный бар health 13:02 МСК 2026-11-03 + две строки bid_failure.

WAL потерян при рестарте Influx (даже при свободном диске). Восстанавливаем
ровно этот слот: bid_lk_run fail + landing_chatbot_topics + lk_auth_login.

Только WRITE, без delete. Не диапазон, не bulk.
Основной restore графиков: monitor/restore_influx_now.py (включает этот слот).
Точечно:

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

# 13:02:46.852 МСК = 10:02:46.852 UTC. Бар — эта миллисекунда; evidence — WAL ns.
STAMP = datetime.fromisoformat("2026-11-03T10:02:46.852+00:00")
FAIL_STAMP = datetime.fromisoformat("2026-11-03T10:02:46.852563+00:00")
if STAMP != datetime(2026, 11, 3, 10, 2, 46, 852000, tzinfo=timezone.utc):
    raise RuntimeError("hard cap: only 2026-11-03T10:02:46.852Z")
if FAIL_STAMP != datetime(2026, 11, 3, 10, 2, 46, 852563, tzinfo=timezone.utc):
    raise RuntimeError("hard cap: only 2026-11-03T10:02:46.852563Z")
if FAIL_STAMP - STAMP >= timedelta(seconds=1):
    raise RuntimeError("hard cap: failure stamp outside the 13:02 second")

# Flux range обязателен для SELECT; пишем не диапазон, а точки STAMP / FAIL_STAMP.
_QUERY_STOP = STAMP + timedelta(seconds=1)

# Снимок VPS-каталога на 13:02 (не локальный грязный check_catalog).
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


def _failure_points() -> list[Point]:
    # Схема как write_failure_events: tags run_type/run_label/check/label, field error.
    points = []
    for check, label, error in _FAILURES:
        points.append(
            Point("bid_failure")
            .tag("run_type", "health")
            .tag("run_label", _HEALTH_RUN_LABEL)
            .tag("check", check[:128])
            .tag("label", label[:256])
            .field("error", error[:2000])
            .time(FAIL_STAMP)
        )
    return points


def _print_would_write() -> None:
    print(
        "would write: measurement=bid_lk_run time="
        f"{STAMP.isoformat()} run_status=fail success=0 skipped=0 "
        "failed_checks=1 duration_sec=120.0"
    )
    for check, label, error in _FAILURES:
        print(
            "would write: measurement=bid_failure time="
            f"{FAIL_STAMP.isoformat()} run_type=health check={check} "
            f"label={label} error={error[:120]}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="WRITE-only bid_lk_run fail + 2 bid_failure at 13:02 MSK 2026-11-03"
    )
    parser.add_argument("--apply", action="store_true", help="Записать бар и 2 строки (без delete)")
    args = parser.parse_args()

    if not INFLUXDB_TOKEN:
        print("ERROR: INFLUXDB_TOKEN не задан")
        return 1

    print(f"Influx {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")
    print(
        "WRITE-only, no delete. Hard cap: 1 bid_lk_run at",
        STAMP.isoformat(),
        "+ 2 bid_failure at",
        FAIL_STAMP.isoformat(),
    )
    print("apply" if args.apply else "dry-run (без --apply ничего не пишем)")

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        before_run = _query_lk_run(client)
        evidence = _query_failure_evidence(client)
        print("before: bid_lk_run:", before_run or "(пусто)")
        print("evidence: bid_failure:", evidence or "(пусто)")
        _print_would_write()
        if not args.apply:
            return 0

        write_api = client.write_api(write_options=SYNCHRONOUS)
        records = [_fail_point(), *_failure_points()]
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=records)
        after_run = _query_lk_run(client)
        after_fail = _query_failure_evidence(client)
        print("after: bid_lk_run:", after_run or "(пусто)")
        print("after: bid_failure:", after_fail or "(пусто)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
