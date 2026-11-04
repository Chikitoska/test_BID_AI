"""WRITE-only restore: 13:02 stays fail; unknown slots not painted green."""

from pathlib import Path

from datetime import datetime, timezone

from monitor.restore_influx_now import (
    FAIL_RUN_STAMP,
    collect_run_points,
    in_fail_1302_slot,
    points_from_health_log,
)


def test_1302_slot_window():
    assert in_fail_1302_slot(FAIL_RUN_STAMP) is True
    assert in_fail_1302_slot(datetime(2026, 11, 3, 10, 1, 59, tzinfo=timezone.utc)) is False
    assert in_fail_1302_slot(datetime(2026, 11, 3, 10, 3, 0, tzinfo=timezone.utc)) is False


def test_collect_keeps_1302_fail_and_drops_green_in_that_minute():
    snapshot = {
        "health": [
            {
                "t": "2026-11-03T10:02:10.000Z",
                "success": 1,
                "run_status": "ok",
                "skipped": 0,
            },
            {
                "t": "2026-11-02T12:20:49.162Z",
                "success": 1,
                "run_status": "ok",
                "skipped": 0,
            },
        ],
        "combat": [],
    }
    points = collect_run_points(snapshot=snapshot, logs={})
    slot = [p for p in points if p.measurement == "bid_lk_run" and in_fail_1302_slot(p.time)]
    assert len(slot) == 1
    assert slot[0].success == 0
    assert slot[0].run_status == "fail"
    assert slot[0].time == FAIL_RUN_STAMP
    ok_health = [
        p
        for p in points
        if p.measurement == "bid_lk_run" and p.success == 1 and p.time.year == 2026
    ]
    assert any(p.time.isoformat().startswith("2026-11-02T12:20:49") for p in ok_health)


def test_health_log_without_date_is_skipped():
    text = """
=== BID Health Monitor (landing + LK) ===
[OK] main_page 200 120ms
Health monitor finished in 12.0s — OK (run_status=ok)
"""
    assert points_from_health_log(text) == []


def test_health_log_assistant_and_500_are_fail():
    text = """
=== BID Health Monitor (landing + LK) ===
[FAIL] landing_chatbot_topics ассистент недоступен
[FAIL] lk_auth_login HTTP 500
Date: Tue, 03 Nov 2026 10:02:46 GMT
Health monitor finished in 120.0s — FAIL (run_status=fail)
"""
    points = points_from_health_log(text)
    assert len(points) == 1
    assert points[0].success == 0
    assert points[0].run_status == "fail"


def test_restore_script_is_write_only():
    source = (Path(__file__).resolve().parents[2] / "monitor" / "restore_influx_now.py").read_text(
        encoding="utf-8"
    )
    assert "delete_api" not in source
    assert "no email" in source.lower() or "без писем" in source


def test_overnight_and_daily_are_present():
    points = collect_run_points(snapshot={"health": [], "combat": []}, logs={})
    combat = [p for p in points if p.measurement == "bid_lk_pytest"]
    daily = [p for p in points if p.measurement == "bid_run"]
    assert len(combat) == 6
    assert all(p.success == 1 for p in combat)
    assert len(daily) == 2
    assert all(p.success == 1 for p in daily)
