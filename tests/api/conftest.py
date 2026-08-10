"""Fixtures для API-тестов (без Selenium — работает на VPS probe)."""

import pytest
import requests


@pytest.fixture(scope="session")
def http_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9",
        }
    )
    yield session
    session.close()
