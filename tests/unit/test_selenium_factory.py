from utils.selenium_factory import (
    _CHROME_CANDIDATES,
    _alloc_user_data_dir,
    _is_gost_chrome_path,
    _pids_for_user_data_dir,
    _resolve_chrome_binary,
    kill_orphans_for_user_data_dir,
    user_data_dir_from_options,
)


def test_alloc_user_data_dir_is_unique():
    first = _alloc_user_data_dir()
    second = _alloc_user_data_dir()
    assert first != second
    assert "bid-chrome-" in first


def test_user_data_dir_from_options():
    class Opts:
        arguments = ["--headless=new", "--user-data-dir=/tmp/bid-chrome-abc123"]

    assert user_data_dir_from_options(Opts()) == "/tmp/bid-chrome-abc123"


def test_pids_for_short_dir_is_empty():
    assert _pids_for_user_data_dir("x") == []
    assert kill_orphans_for_user_data_dir("") == 0


def test_chrome_candidates_are_stock_not_gost():
    assert _CHROME_CANDIDATES
    assert all(not _is_gost_chrome_path(path) for path in _CHROME_CANDIDATES)


def test_resolve_chrome_binary_ignores_gost_override(monkeypatch, tmp_path):
    gost = tmp_path / "chromium-gost"
    gost.write_text("", encoding="utf-8")
    gost.chmod(0o755)
    monkeypatch.setenv("CHROME_BINARY", str(gost))
    resolved = _resolve_chrome_binary()
    assert resolved != str(gost)
    assert not _is_gost_chrome_path(resolved)


def test_create_chrome_driver_does_not_look_for_gost():
    import inspect

    from utils import selenium_factory

    source = inspect.getsource(selenium_factory)
    assert "chromium-gost-profile" not in source
    assert all("gost" not in path.lower() for path in selenium_factory._CHROME_CANDIDATES)
    assert selenium_factory._is_gost_chrome_path("/opt/chromium-gost/chrome") is True
    assert selenium_factory._is_gost_chrome_path("/usr/bin/chromium") is False
