"""Отправка метрик в InfluxDB."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from monitor.check_catalog import get_check_label, get_check_order
from monitor.checks import CheckResult
from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL
from monitor.run_labels import get_run_label


@dataclass
class FailureEvent:
    check: str
    label: str
    error: str


def failures_from_checks(results: list[CheckResult]) -> list[FailureEvent]:
    from monitor.alerts import failure_detail

    return [
        FailureEvent(
            check=item.name,
            label=get_check_label(item.name),
            error=failure_detail(item),
        )
        for item in results
        if not item.success
    ]


def write_failure_events(*, run_type: str, failures: list[FailureEvent]) -> None:
    """Ошибки прогона → bid_failure (таблица в Grafana)."""
    if not INFLUXDB_TOKEN or not failures:
        return

    run_label = get_run_label(run_type)
    now = datetime.now(timezone.utc)
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        points = []
        for item in failures:
            points.append(
                Point("bid_failure")
                .tag("run_type", run_type)
                .tag("run_label", run_label)
                .tag("check", item.check[:128])
                .tag("label", item.label[:256])
                .field("error", item.error[:2000])
                .time(now)
            )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)


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
                .tag("label", get_check_label(item.name))
                .tag("order", str(get_check_order(item.name)))
                .tag("method", item.method)
                .field("success", 1 if item.success else 0)
                .field("http_code", int(item.http_code))
                .field("duration_ms", float(item.duration_ms))
                .field("error", item.error or "")
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
    """run_daily → bid_run (Лендинг + API autotests)."""
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
    """run_light → bid_probe (Мониторинг каждые 5 мин)."""
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
    """run_health_monitor → bid_lk_run (Лендинг + мин ЛК)."""
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


def write_lk_pytest_run(
    *,
    total: int,
    passed: int,
    failed: int,
    duration_sec: float,
) -> None:
    """run_lk_pytest → bid_lk_pytest (Боевой прогон ЛК)."""
    if not INFLUXDB_TOKEN:
        return

    success = 1 if failed == 0 and total > 0 else 0
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point("bid_lk_pytest")
            .field("total", total)
            .field("passed", passed)
            .field("failed", failed)
            .field("success", success)
            .field("duration_sec", duration_sec)
            .time(datetime.now(timezone.utc))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
