"""HTTP-проверки эндпоинтов BID для мониторинга."""

from dataclasses import dataclass
import time

import requests

from config.api_catalog import EXTERNAL_LANDING_API_METHODS, LANDING_API_METHODS, LandingApiMethod
from config.settings import AUTH_URL_PATTERNS, BASE_URL, PUBLIC_EXTERNAL_URLS
from monitor.check_catalog import get_check_label
from monitor.config import MONITOR_ACCEPT_CODES, MONITOR_HTTP_CONNECT_TIMEOUT, MONITOR_HTTP_TIMEOUT
from utils.auth_filter import is_auth_url


@dataclass
class CheckResult:
    name: str
    url: str
    method: str
    success: bool
    http_code: int
    duration_ms: float
    error: str = ""


def _check_get(session: requests.Session, name: str, url: str) -> CheckResult:
    print(f"  -> {name}: {get_check_label(name)}", flush=True)
    start = time.perf_counter()
    timeout = (MONITOR_HTTP_CONNECT_TIMEOUT, MONITOR_HTTP_TIMEOUT)
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True)
        duration_ms = (time.perf_counter() - start) * 1000
        code = response.status_code
        if 200 <= code < 300 or code in MONITOR_ACCEPT_CODES:
            return CheckResult(name, url, "GET", True, code, duration_ms)
        return CheckResult(
            name, url, "GET", False, code, duration_ms,
            error=f"HTTP {code}: {response.reason}",
        )
    except requests.RequestException as exc:
        duration_ms = (time.perf_counter() - start) * 1000
        return CheckResult(name, url, "GET", False, 0, duration_ms, error=str(exc))


def _url_for_api(api: LandingApiMethod) -> str:
    return f"{api.base.rstrip('/')}{api.path}"


def run_http_checks(session: requests.Session) -> list[CheckResult]:
    results: list[CheckResult] = []

    results.append(_check_get(session, "main_page", BASE_URL))

    for api in LANDING_API_METHODS:
        if api.method == "GET":
            results.append(_check_get(session, api.name, _url_for_api(api)))

    for api in EXTERNAL_LANDING_API_METHODS:
        if api.method == "GET":
            results.append(_check_get(session, api.name, _url_for_api(api)))

    for url in PUBLIC_EXTERNAL_URLS:
        if not is_auth_url(url):
            results.append(_check_get(session, f"external_{url.split('/')[-1]}", url))

    return results
