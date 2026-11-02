from utils.selenium_factory import (
    _alloc_user_data_dir,
    _pids_for_user_data_dir,
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
