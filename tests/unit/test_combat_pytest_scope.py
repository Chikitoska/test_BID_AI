from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_combat_pytest_does_not_include_landing_chatbot_or_mincifry():
    source = (ROOT / "monitor" / "run_lk_pytest.py").read_text(encoding="utf-8")
    assert "tests/lk/" in source
    assert "test_landing_chatbot.py" not in source
    assert "test_mincifry.py" not in source


def test_mincifry_lock_wait_defaults_to_600():
    source = (ROOT / "monitor" / "run_mincifry.py").read_text(encoding="utf-8")
    assert '"600"' in source
    assert 'CHROME_LOCK_WAIT_HEALTH_SEC", "120"' not in source
    assert 'MINCIFRY_ALERT", "false"' in source
