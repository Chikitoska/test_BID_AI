from pages.widget_urls import is_blank_target


def test_blank_targets() -> None:
    assert is_blank_target(None) is True
    assert is_blank_target("") is True
    assert is_blank_target("about:blank") is True
    assert is_blank_target("javascript:void(0)") is True
    assert is_blank_target("#") is True


def test_real_targets() -> None:
    assert is_blank_target("https://www.gosuslugi.ru/crt") is False
    assert is_blank_target("https://bid.gazprom-neft.ru/certs") is False
