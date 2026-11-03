"""Daily: столбец bid_run пишем раньше деталей HTTP."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_daily_writes_pytest_run_before_check_results():
    source = (ROOT / "monitor" / "run_daily.py").read_text(encoding="utf-8")
    run_at = source.index("write_pytest_run(")
    checks_at = source.index("write_check_results(")
    assert run_at < checks_at
    assert "write_pytest_run failed" in source
    assert "write_check_results failed" in source


def test_cron_shells_rotate_logs():
    daily = (ROOT / "monitor" / "run_daily.sh").read_text(encoding="utf-8")
    health = (ROOT / "monitor" / "run_health_monitor.sh").read_text(encoding="utf-8")
    assert "rotate_logs.sh" in daily
    assert "cron.log" in daily
    assert "rotate_logs.sh" in health
    assert "health.log" in health
