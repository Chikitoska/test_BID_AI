"""Daily: столбец bid_run пишем раньше деталей HTTP."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_daily_writes_pytest_run_before_check_results():
    source = (ROOT / "monitor" / "run_daily.py").read_text(encoding="utf-8")
    body = source[source.index("def _run_daily_body") :]
    run_at = body.index("write_pytest_run(")
    mincifry_at = body.index("mincifry_results = _run_daily_mincifry()")
    checks_at = body.index("write_check_results(")
    assert run_at < mincifry_at < checks_at
    assert "write_pytest_run failed" in source
    assert "write_check_results failed" in source
    assert 'CHROME_LOCK_WAIT_DAILY_SEC", "90"' in source
    assert 'CHROME_LOCK_WAIT_DAILY_SEC", "1200"' not in source


def test_cron_shells_rotate_logs():
    daily = (ROOT / "monitor" / "run_daily.sh").read_text(encoding="utf-8")
    health = (ROOT / "monitor" / "run_health_monitor.sh").read_text(encoding="utf-8")
    assert "rotate_logs.sh" in daily
    assert "cron.log" in daily
    assert "rotate_logs.sh" in health
    assert "health.log" in health
