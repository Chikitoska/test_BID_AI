import os
import signal

import pytest

from utils import selenium_factory as selenium_factory_mod
from utils.selenium_factory import (
    ChromeDiskFullError,
    _CHROME_CANDIDATES,
    _alloc_user_data_dir,
    _is_gost_chrome_path,
    _pids_for_user_data_dir,
    _resolve_chrome_binary,
    assert_disk_for_chrome,
    create_chrome_driver,
    kill_orphans_for_user_data_dir,
    quit_chrome_driver,
    remove_chrome_user_data_dir,
    snap_private_twin_dir,
    sweep_stale_bid_chrome_profiles,
    user_data_dir_from_options,
)


def test_alloc_user_data_dir_is_unique():
    first = _alloc_user_data_dir()
    second = _alloc_user_data_dir()
    try:
        assert first != second
        assert "bid-chrome-" in first
    finally:
        remove_chrome_user_data_dir(first)
        remove_chrome_user_data_dir(second)


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


def test_sweep_skips_live_and_deletes_stale(tmp_path, monkeypatch):
    snap = tmp_path / "snap.chromium" / "tmp"
    snap.mkdir(parents=True)
    tmp_root = tmp_path / "tmp"
    tmp_root.mkdir()
    live = tmp_root / "bid-chrome-live"
    live.mkdir()
    stale = tmp_root / "bid-chrome-stale"
    stale.mkdir()
    (snap / "bid-chrome-live").mkdir()
    (snap / "bid-chrome-stale").mkdir()
    other = tmp_root / "not-chrome"
    other.mkdir()

    monkeypatch.setattr(selenium_factory_mod, "SNAP_CHROMIUM_PRIVATE_TMP", str(snap))
    monkeypatch.setattr(
        selenium_factory_mod, "_bid_chrome_search_roots", lambda: [str(tmp_root), str(snap)]
    )
    monkeypatch.setattr(selenium_factory_mod, "_user_data_dirs_from_running_chrome", lambda: [])
    selenium_factory_mod._LIVE_USER_DATA_DIRS.clear()
    selenium_factory_mod._LIVE_USER_DATA_DIRS.add(str(live))
    try:
        removed = sweep_stale_bid_chrome_profiles()
        assert live.exists()
        assert (snap / "bid-chrome-live").exists()
        assert not stale.exists()
        assert not (snap / "bid-chrome-stale").exists()
        assert other.exists()
        assert removed == 2
    finally:
        selenium_factory_mod._LIVE_USER_DATA_DIRS.clear()


def test_assert_disk_for_chrome_raises_below_500mb(monkeypatch):
    monkeypatch.setattr(selenium_factory_mod, "disk_free_bytes", lambda path="/": 100 * 1024 * 1024)
    monkeypatch.setenv("CHROME_MIN_FREE_MB", "500")
    with pytest.raises(ChromeDiskFullError) as exc:
        assert_disk_for_chrome()
    assert "no space left on device" in str(exc.value).lower()


def test_create_chrome_driver_refuses_when_disk_full(monkeypatch):
    def _boom(*, path: str = "/") -> None:
        raise ChromeDiskFullError("ENOSPC: Avail=12MB < 500MB — no space left on device")

    monkeypatch.setattr(selenium_factory_mod, "sweep_stale_bid_chrome_profiles", lambda: 0)
    monkeypatch.setattr(selenium_factory_mod, "assert_disk_for_chrome", _boom)
    with pytest.raises(ChromeDiskFullError):
        create_chrome_driver()


def test_sigterm_removes_live_profile(tmp_path, monkeypatch):
    user_dir = tmp_path / "bid-chrome-term"
    user_dir.mkdir()
    monkeypatch.setattr(selenium_factory_mod, "kill_orphans_for_user_data_dir", lambda _dir: 0)
    selenium_factory_mod._LIVE_USER_DATA_DIRS.clear()
    selenium_factory_mod._register_live_user_data_dir(str(user_dir))
    prev = selenium_factory_mod._PREV_SIGTERM
    selenium_factory_mod._PREV_SIGTERM = signal.SIG_IGN
    try:
        selenium_factory_mod._sigterm_chrome_cleanup(signal.SIGTERM, None)
        assert not user_dir.exists()
        assert os.path.normpath(str(user_dir)) not in selenium_factory_mod._LIVE_USER_DATA_DIRS
    finally:
        selenium_factory_mod._PREV_SIGTERM = prev
        selenium_factory_mod._LIVE_USER_DATA_DIRS.clear()
