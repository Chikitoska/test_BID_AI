import shutil

from utils import selenium_factory as selenium_factory_mod
from utils.selenium_factory import (
    _CHROME_CANDIDATES,
    _alloc_user_data_dir,
    _is_gost_chrome_path,
    _pids_for_user_data_dir,
    _resolve_chrome_binary,
    kill_orphans_for_user_data_dir,
    quit_chrome_driver,
    remove_chrome_user_data_dir,
    snap_private_twin_dir,
    user_data_dir_from_options,
)


def test_alloc_user_data_dir_is_unique():
    first = _alloc_user_data_dir()
    second = _alloc_user_data_dir()
    try:
        assert first != second
        assert "bid-chrome-" in first
    finally:
        shutil.rmtree(first, ignore_errors=True)
        shutil.rmtree(second, ignore_errors=True)


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


def test_snap_private_twin_dir_only_this_basename():
    assert snap_private_twin_dir("/tmp/bid-chrome-abc") == (
        f"{selenium_factory_mod.SNAP_CHROMIUM_PRIVATE_TMP}/bid-chrome-abc"
    )
    assert snap_private_twin_dir("/tmp/other-profile") == ""
    assert snap_private_twin_dir("") == ""


def test_remove_skips_non_bid_chrome_profile(tmp_path):
    user_dir = tmp_path / "shared-chrome-profile"
    user_dir.mkdir()
    remove_chrome_user_data_dir(str(user_dir))
    assert user_dir.exists()


def test_quit_chrome_driver_removes_user_data_dir_and_snap_twin(tmp_path, monkeypatch):
    user_dir = tmp_path / "bid-chrome-testrun"
    user_dir.mkdir()
    (user_dir / "Default").write_text("stub", encoding="utf-8")

    snap_base = tmp_path / "snap.chromium" / "tmp"
    snap_base.mkdir(parents=True)
    twin = snap_base / "bid-chrome-testrun"
    twin.mkdir()
    (twin / "Default").write_text("real", encoding="utf-8")
    sibling = snap_base / "bid-chrome-sibling"
    sibling.mkdir()
    other_snap = tmp_path / "snap.firefox" / "tmp" / "bid-chrome-testrun"
    other_snap.mkdir(parents=True)

    monkeypatch.setattr(selenium_factory_mod, "SNAP_CHROMIUM_PRIVATE_TMP", str(snap_base))
    monkeypatch.setattr(selenium_factory_mod, "kill_orphans_for_user_data_dir", lambda _dir: 0)

    class Driver:
        _bid_user_data_dir = str(user_dir)

        def quit(self):
            self.quit_called = True

    driver = Driver()
    quit_chrome_driver(driver)
    assert driver.quit_called is True
    assert not user_dir.exists()
    assert not twin.exists()
    assert sibling.exists()
    assert other_snap.exists()


def test_quit_chrome_driver_removes_dir_if_quit_raises(tmp_path, monkeypatch):
    user_dir = tmp_path / "bid-chrome-dead"
    user_dir.mkdir()
    snap_base = tmp_path / "snap.chromium" / "tmp"
    snap_base.mkdir(parents=True)
    twin = snap_base / "bid-chrome-dead"
    twin.mkdir()
    monkeypatch.setattr(selenium_factory_mod, "SNAP_CHROMIUM_PRIVATE_TMP", str(snap_base))
    monkeypatch.setattr(selenium_factory_mod, "kill_orphans_for_user_data_dir", lambda _dir: 0)

    class Driver:
        _bid_user_data_dir = str(user_dir)

        def quit(self):
            raise RuntimeError("chrome already dead")

    quit_chrome_driver(Driver())
    assert not user_dir.exists()
    assert not twin.exists()
