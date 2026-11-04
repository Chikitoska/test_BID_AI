from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_combat_pytest_does_not_include_landing_chatbot_or_mincifry():
    source = (ROOT / "monitor" / "run_lk_pytest.py").read_text(encoding="utf-8")
    assert "tests/lk/" in source
    assert "test_landing_chatbot.py" not in source
    assert "test_mincifry.py" not in source
    assert "200 * 1024" not in source
    assert "assert_disk_for_chrome" in source
    assert "chrome_min_free_bytes" in source
    assert "chrome_profile_lifecycle" in source


def test_vps_free_disk_never_prunes_influx_grafana():
    source = (ROOT / "monitor" / "vps_free_disk.sh").read_text(encoding="utf-8")
    active = "\n".join(
        ln for ln in source.splitlines() if ln.strip() and not ln.lstrip().startswith("#")
    )
    assert "volume prune" not in active
    assert "docker restart" not in active
    assert "docker builder prune" in active
    crontab = (ROOT / "monitor" / "crontab.example").read_text(encoding="utf-8")
    assert "vps_free_disk.sh" in crontab
    assert "*/20" in crontab


def test_daily_shell_has_slot_timeout():
    source = (ROOT / "monitor" / "run_daily.sh").read_text(encoding="utf-8")
    assert "timeout --signal=TERM" in source
    assert "600" in source


def test_mincifry_lock_wait_defaults_to_600():
    source = (ROOT / "monitor" / "run_mincifry.py").read_text(encoding="utf-8")
    assert '"600"' in source
    assert 'CHROME_LOCK_WAIT_HEALTH_SEC", "120"' not in source
    assert 'MINCIFRY_ALERT", "false"' in source
