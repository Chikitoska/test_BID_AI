"""Отправка метрик в InfluxDB."""

from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from monitor.check_catalog import get_check_label
from monitor.checks import CheckResult
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL


def write_check_results(results: list[CheckResult]) -> None:
    if not INFLUXDB_TOKEN:
        return

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        now = datetime.now(timezone.utc)
        points = []
        for item in results:
            point = (
                Point("bid_check")
                .tag("check", item.name)
                .tag("method", item.method)
                .field("success", 1 if item.success else 0)
                .field("http_code", int(item.http_code))
                .field("duration_ms", float(item.duration_ms))
                .field("error", item.error or "")
                .field("label", get_check_label(item.name))
                .time(now)
            )
            points.append(point)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)


def write_pytest_run(
    *,
    total: int,
    passed: int,
    failed: int,
    duration_sec: float,
) -> None:
    if not INFLUXDB_TOKEN:
        return

    success = 1 if failed == 0 and total > 0 else 0
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point("bid_run")
            .field("total", total)
            .field("passed", passed)
            .field("failed", failed)
            .field("success", success)
            .field("duration_sec", duration_sec)
            .time(datetime.now(timezone.utc))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)


def write_probe_run(*, success: bool, failed_count: int, duration_sec: float) -> None:
    if not INFLUXDB_TOKEN:
        return

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point("bid_probe")
            .field("success", 1 if success else 0)
            .field("failed_checks", failed_count)
            .field("duration_sec", duration_sec)
            .time(datetime.now(timezone.utc))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)


def write_lk_check_results(results: list[CheckResult]) -> None:
    if not INFLUXDB_TOKEN:
        return

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        now = datetime.now(timezone.utc)
        points = []
        for item in results:
            point = (
                Point("bid_lk_check")
                .tag("check", item.name)
                .tag("method", item.method)
                .field("success", 1 if item.success else 0)
                .field("http_code", int(item.http_code))
                .field("duration_ms", float(item.duration_ms))
                .field("error", item.error or "")
                .time(now)
            )
            points.append(point)
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)


def write_lk_run(*, success: bool, failed_count: int, duration_sec: float) -> None:
    if not INFLUXDB_TOKEN:
        return

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point("bid_lk_run")
            .field("success", 1 if success else 0)
            .field("failed_checks", failed_count)
            .field("duration_sec", duration_sec)
            .time(datetime.now(timezone.utc))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
