"""Unit tests: run_status tags on metrics writers (no Influx)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import monitor.metrics as metrics


def test_write_lk_pytest_run_tags_autotest(monkeypatch) -> None:
    monkeypatch.setattr(metrics, "INFLUXDB_TOKEN", "tok")
    captured: list = []

    class FakePoint:
        def __init__(self, name):
            self.name = name
            self.tags = {}
            self.fields = {}

        def tag(self, k, v):
            self.tags[k] = v
            return self

        def field(self, k, v):
            self.fields[k] = v
            return self

        def time(self, t):
            self._time = t
            return self

    write_api = MagicMock()
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    client.write_api.return_value = write_api

    def capture_write(**kwargs):
        captured.append(kwargs["record"])

    write_api.write.side_effect = capture_write

    with patch.object(metrics, "Point", FakePoint), patch.object(
        metrics, "InfluxDBClient", return_value=client
    ):
        metrics.write_lk_pytest_run(
            total=5, passed=4, failed=1, duration_sec=10.0, run_status="autotest"
        )

    assert captured[0].tags["run_status"] == "autotest"
    assert captured[0].fields["success"] == 0


def test_write_pytest_run_tags_fail_on_5xx(monkeypatch) -> None:
    monkeypatch.setattr(metrics, "INFLUXDB_TOKEN", "tok")
    captured: list = []

    class FakePoint:
        def __init__(self, name):
            self.tags = {}
            self.fields = {}

        def tag(self, k, v):
            self.tags[k] = v
            return self

        def field(self, k, v):
            self.fields[k] = v
            return self

        def time(self, t):
            return self

    write_api = MagicMock()
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    client.write_api.return_value = write_api
    write_api.write.side_effect = lambda **kw: captured.append(kw["record"])

    with patch.object(metrics, "Point", FakePoint), patch.object(
        metrics, "InfluxDBClient", return_value=client
    ):
        metrics.write_pytest_run(
            total=3, passed=2, failed=1, duration_sec=5.0, run_status="fail"
        )

    assert captured[0].tags["run_status"] == "fail"
    assert captured[0].fields["success"] == 0


def test_write_lk_run_tags_autotest(monkeypatch) -> None:
    monkeypatch.setattr(metrics, "INFLUXDB_TOKEN", "tok")
    captured: list = []

    class FakePoint:
        def __init__(self, name):
            self.tags = {}
            self.fields = {}

        def tag(self, k, v):
            self.tags[k] = v
            return self

        def field(self, k, v):
            self.fields[k] = v
            return self

        def time(self, t):
            return self

    write_api = MagicMock()
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    client.write_api.return_value = write_api
    write_api.write.side_effect = lambda **kw: captured.append(kw["record"])

    with patch.object(metrics, "Point", FakePoint), patch.object(
        metrics, "InfluxDBClient", return_value=client
    ):
        metrics.write_lk_run(
            success=False,
            failed_count=1,
            duration_sec=12.0,
            run_status="autotest",
        )

    assert captured[0].tags["run_status"] == "autotest"
    assert captured[0].fields["success"] == 0
