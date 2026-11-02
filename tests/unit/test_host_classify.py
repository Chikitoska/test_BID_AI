from monitor.host_classify import (
    classify_bid_host,
    format_host_error,
    short_network_kind,
)


def test_classify_landing():
    assert classify_bid_host("https://bid.gazprom-neft.ru/") == "landing"


def test_classify_spa_back():
    assert classify_bid_host("https://spa-back.gazprom-neft.ru/events") == "spa-back"
    assert classify_bid_host("Read timed out for spa-back.gazprom-neft.ru") == "spa-back"


def test_classify_lk():
    assert classify_bid_host("https://lk.bid.gazprom-neft.ru/service-providers") == "lk"
    assert classify_bid_host("https://id.bid.gazprom-neft.ru/realms/") == "lk"


def test_spa_back_timeout_is_not_landing_down():
    err = format_host_error(
        url="https://spa-back.gazprom-neft.ru/static/counter.js",
        error="HTTPSConnectionPool: Read timed out",
    )
    assert err.startswith("spa-back timeout")
    assert "lending" not in err.lower()
    assert "лендинг" not in err.lower()


def test_landing_http_keeps_landing_host():
    err = format_host_error(
        url="https://bid.gazprom-neft.ru/",
        error="HTTP 502: Bad Gateway",
        http_code=502,
    )
    assert err.startswith("landing HTTP 502")


def test_timeout_kind():
    assert short_network_kind("Read timed out") == "timeout"
