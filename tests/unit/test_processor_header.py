"""Processor: ФИО/компания только в шапке/iframe, не anywhere-in-body."""

from pathlib import Path

FLOW = Path(__file__).resolve().parents[2] / "pages" / "lk_flow.py"


def test_processor_does_not_accept_body_wide_match():
    source = FLOW.read_text(encoding="utf-8")
    assert "if expected in body" not in source
    assert 'By.TAG_NAME, "body"' not in source.split("def _read_processor_user_field")[1].split(
        "def _read_processor_field_in_context"
    )[0]


def test_processor_selectors_stay_in_header_context():
    chunk = FLOW.read_text(encoding="utf-8").split("def _read_processor_user_field")[1].split(
        "def _read_processor_field_in_context"
    )[0]
    assert "[class*='{child_token}']" not in chunk
    assert "User-Block" in chunk
    assert "header" in chunk
    assert "iframe" in chunk
