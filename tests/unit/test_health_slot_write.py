"""Health 5-min slot: lock wait cap + bid_lk_run always written separately."""

from pathlib import Path

from monitor.run_health_monitor import HEALTH_LOCK_WAIT_CAP_SEC, health_lock_wait_sec

ROOT = Path(__file__).resolve().parents[2]


def test_health_lock_wait_caps_600_to_90():
    assert HEALTH_LOCK_WAIT_CAP_SEC == 90.0
    assert health_lock_wait_sec(600) == 90.0
    assert health_lock_wait_sec(90) == 90.0
    assert health_lock_wait_sec(30) == 30.0
    assert health_lock_wait_sec(0) == 5.0


def test_health_writes_lk_run_before_check_results():
    source = (ROOT / "monitor" / "run_health_monitor.py").read_text(encoding="utf-8")
    run_at = source.index("write_lk_run(")
    fail_at = source.index("write_failure_events(")
    checks_at = source.index("write_check_results(")
    assert run_at < fail_at < checks_at
    assert "write_lk_run failed" in source
    assert "HEALTH_SLOT_SEC" in source
    assert "SIG_IGN" in source
    assert "prefer_http_error" in source
    assert 'CHROME_LOCK_WAIT_HEALTH_SEC", "90"' in source
    assert 'CHROME_LOCK_WAIT_HEALTH_SEC", "600"' not in source


def test_health_shell_has_slot_timeout():
    source = (ROOT / "monitor" / "run_health_monitor.sh").read_text(encoding="utf-8")
    assert "timeout --signal=TERM" in source
    assert "220" in source
