from utils.selenium_factory import _alloc_user_data_dir


def test_alloc_user_data_dir_is_unique():
    first = _alloc_user_data_dir()
    second = _alloc_user_data_dir()
    assert first != second
    assert "bid-chrome-" in first
