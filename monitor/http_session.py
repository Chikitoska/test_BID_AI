"""HTTP-сессия мониторинга с заголовками как у браузера (обход WAF)."""

import requests

from monitor.config import MONITOR_USER_AGENT

DEFAULT_HEADERS = {
    "User-Agent": MONITOR_USER_AGENT,
    "Accept": "text/html,application/json,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9",
}


def create_monitor_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    return session
