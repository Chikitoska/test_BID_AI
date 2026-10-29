from pages.widget_urls import (
    is_blank_target,
    is_yandex_browser_href,
    mentions_yandex_browser,
    normalize_page_text,
)


def test_blank_targets() -> None:
    assert is_blank_target(None) is True
    assert is_blank_target("") is True
    assert is_blank_target("about:blank") is True
    assert is_blank_target("javascript:void(0)") is True
    assert is_blank_target("#") is True


def test_real_targets() -> None:
    assert is_blank_target("https://www.gosuslugi.ru/crt") is False
    assert is_blank_target("https://bid.gazprom-neft.ru/certs") is False


def test_yandex_browser_mentions_ignore_nbsp_and_punctuation() -> None:
    assert mentions_yandex_browser("Используйте «Яндекс\xa0Браузер»")
    assert mentions_yandex_browser("Яндекс. Браузером")
    assert mentions_yandex_browser("скачайте Яндекс.Браузер")
    assert mentions_yandex_browser("Install Yandex Browser")
    assert not mentions_yandex_browser("Установите российские сертификаты")


def test_normalize_page_text_collapses_nbsp() -> None:
    assert normalize_page_text("Яндекс\xa0Браузер") == "яндекс браузер"


def test_yandex_browser_href() -> None:
    assert is_yandex_browser_href("https://browser.yandex.ru/")
    assert not is_yandex_browser_href("https://bid.gazprom-neft.ru/")
