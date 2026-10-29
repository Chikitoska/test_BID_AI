"""Сборка XLSX с ошибками bid_failure из Influx (для Grafana export)."""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Sequence

from openpyxl import Workbook

from monitor.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL

# Influx run_type → колонка «прогон» в выгрузке (как просил пользователь).
RUN_TYPE_EXPORT: dict[str, str] = {
    "health": "health",
    "full": "daily",
    "daily": "daily",
    "lk_pytest": "lk_pytest",
    "probe": "probe",  # legacy run_light
}

MSK = timezone(timedelta(hours=3))
_DIGITS = re.compile(r"^\d+$")


@dataclass(frozen=True)
class ErrorRow:
    """Одна строка выгрузки: дата, ошибка, прогон."""

    date: datetime
    error: str
    run: str

    def date_display(self, *, tz: timezone = MSK) -> str:
        """МСК до секунд, без суффикса зоны (без UTC / UTC+03:00)."""
        local = self.date.astimezone(tz) if self.date.tzinfo else self.date.replace(tzinfo=timezone.utc).astimezone(tz)
        return local.strftime("%Y-%m-%d %H:%M:%S")


def normalize_run_type(run_type: str | None) -> str:
    key = (run_type or "").strip()
    if not key:
        return "unknown"
    return RUN_TYPE_EXPORT.get(key, key)


def parse_grafana_time(value: str | None, *, default: datetime | None = None) -> datetime:
    """Разбор ${__from}/${__to} из Grafana data/dashboard links.

    Grafana отдаёт миллисекунды epoch. Также принимаем секунды и ISO-8601.
    """
    raw = (value or "").strip()
    if not raw:
        if default is not None:
            return default
        raise ValueError("empty time value")

    if _DIGITS.match(raw):
        num = int(raw)
        # Grafana __from/__to — ms; 10 цифр ≈ секунды.
        if num >= 10**12:
            return datetime.fromtimestamp(num / 1000.0, tz=timezone.utc)
        return datetime.fromtimestamp(num, tz=timezone.utc)

    # ISO: 2024-01-01T00:00:00Z / +00:00
    iso = raw.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(iso)
    except ValueError as exc:
        raise ValueError(f"unsupported time format: {raw!r}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def resolve_time_range(
    from_raw: str | None,
    to_raw: str | None,
    *,
    default_hours: int = 24,
) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    start = parse_grafana_time(from_raw, default=now - timedelta(hours=default_hours))
    stop = parse_grafana_time(to_raw, default=now)
    if stop < start:
        start, stop = stop, start
    return start, stop


def rows_from_records(records: Iterable[Any]) -> list[ErrorRow]:
    """Собрать строки из Influx query records (или mock-объектов с теми же атрибутами)."""
    rows: list[ErrorRow] = []
    for record in records:
        ts = _record_time(record)
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        values = getattr(record, "values", None) or {}
        run_type = values.get("run_type") if isinstance(values, dict) else None
        if run_type is None and hasattr(record, "get"):
            try:
                run_type = record.get("run_type")  # type: ignore[union-attr]
            except Exception:
                run_type = None
        error = _record_error(record)
        rows.append(
            ErrorRow(
                date=ts.astimezone(timezone.utc),
                error=error,
                run=normalize_run_type(str(run_type) if run_type is not None else ""),
            )
        )
    rows.sort(key=lambda r: r.date, reverse=True)
    return rows


def _record_time(record: Any) -> datetime | None:
    if hasattr(record, "get_time"):
        return record.get_time()
    values = getattr(record, "values", None)
    if isinstance(values, dict) and "_time" in values:
        return values["_time"]
    return getattr(record, "time", None) or getattr(record, "_time", None)


def _record_error(record: Any) -> str:
    if hasattr(record, "get_value"):
        val = record.get_value()
    else:
        values = getattr(record, "values", None) or {}
        val = values.get("_value") if isinstance(values, dict) else getattr(record, "error", "")
    text = str(val or "").strip()
    return text.replace("\r\n", "\n")


def build_failure_flux(*, start: datetime, stop: datetime, bucket: str | None = None) -> str:
    b = bucket or INFLUXDB_BUCKET
    return f'''
from(bucket: "{b}")
  |> range(start: {start.isoformat()}, stop: {stop.isoformat()})
  |> filter(fn: (r) => r._measurement == "bid_failure" and r._field == "error")
  |> sort(columns: ["_time"], desc: true)
'''.strip()


def fetch_failure_rows(
    *,
    start: datetime,
    stop: datetime,
    query_api: Any | None = None,
) -> list[ErrorRow]:
    """Запрос bid_failure из Influx. query_api можно подменить в тестах."""
    if query_api is None:
        if not INFLUXDB_TOKEN:
            raise RuntimeError("INFLUXDB_TOKEN не задан")
        from influxdb_client import InfluxDBClient

        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
            return fetch_failure_rows(start=start, stop=stop, query_api=client.query_api())

    flux = build_failure_flux(start=start, stop=stop)
    tables = query_api.query(flux, org=INFLUXDB_ORG)
    records: list[Any] = []
    for table in tables:
        records.extend(table.records)
    return rows_from_records(records)


def build_xlsx_bytes(rows: Sequence[ErrorRow], *, sheet_title: str = "errors") -> bytes:
    """XLSX: колонки дата | ошибка | прогон."""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title[:31]
    ws.append(["дата", "ошибка", "прогон"])
    for row in rows:
        ws.append([row.date_display(), row.error, row.run])

    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 80
    ws.column_dimensions["C"].width = 14

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
