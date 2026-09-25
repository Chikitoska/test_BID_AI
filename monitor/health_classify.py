"""Классификация сбоев health: prod (ЛК/сайт) vs infra (Chrome/WebDriver)."""

from __future__ import annotations

import re
from typing import Literal

from monitor.checks import CheckResult
from monitor.http_status import is_http_4xx_or_5xx, results_have_http_4xx_or_5xx

HealthFailureKind = Literal["prod", "infra"]
HealthRunStatus = Literal["ok", "fail", "skipped_busy", "infra"]

# Инфра браузера на VPS — не путать с «ЛК лежит».
# Не использовать голое «chromedriver» / «stacktrace»:
# путь к chromedriver и Stacktrace есть почти в любом Selenium-логе.
_CHROME_INFRA_MARKERS = (
    "chromedriver unexpectedly exited",
    "chrome not reachable",
    "chrome failed to start",
    "session deleted",
    "invalid session",
    "no such window",
    "session not created",
    "sessionnotcreatedexception",
    "webdriver exception",
    "devtoolsautomevent",
    "cannot connect to chrome",
    "disconnected: not connected to devtools",
    "browser has closed",
    "target window already closed",
    "user data directory is already in use",
)

# UI-ожидания/селекторы — для health это скорее «ЛК/страница», не краш Chrome.
# Пустой Message: у TimeoutException не глушим как infra.
_UI_WAIT_EXCEPTION_MARKERS = (
    "timeoutexception",
    "nosuchelementexception",
    "staleelementreferenceexception",
    "elementclickinterceptedexception",
    "elementnotinteractableexception",
    "elementnotvisibleexception",
    "invalidselectorexception",
    "assertionerror",
)

# Пустой Message: / Message:\nStacktrace без имени wait-exception — краш драйвера.
_EMPTY_WEBDRIVER_MESSAGE_RE = re.compile(
    r"(?:^|\b)Message:\s*(?:\n|$|Stacktrace)",
    re.IGNORECASE,
)


def is_chrome_infra_error(error: str) -> bool:
    """True, если текст ошибки указывает на сбой Chrome/WebDriver, а не на BID."""
    text = (error or "").strip()
    if not text:
        # Пустая ошибка у упавшего UI-шага — почти всегда мёртвый драйвер.
        return True
    lower = text.lower()
    if any(marker in lower for marker in _CHROME_INFRA_MARKERS):
        return True
    # Пустой Message: — infra только если это не именованный UI wait/assert.
    if _EMPTY_WEBDRIVER_MESSAGE_RE.search(text):
        if any(marker in lower for marker in _UI_WAIT_EXCEPTION_MARKERS):
            return False
        return True
    return False


def classify_health_failure(results: list[CheckResult]) -> HealthFailureKind:
    """prod = сеть/4xx/5xx/логин BID; infra = только Chrome/WebDriver-флаки.

    Если среди FAIL есть подтверждённый HTTP 4xx/5xx — всегда prod.
    Infra только когда *все* упавшие проверки выглядят как браузерная инфра.
    Смешанные/непонятные FAIL → prod (безопаснее алертить).
    """
    failed = [item for item in results if not item.success]
    if not failed:
        return "prod"

    if results_have_http_4xx_or_5xx(failed):
        return "prod"

    for item in failed:
        if is_http_4xx_or_5xx(http_code=item.http_code, error=item.error):
            return "prod"
        # HTTP-проверка лендинга (не UI) — всегда prod/сеть.
        if (item.method or "").upper() in ("GET", "POST", "HEAD"):
            return "prod"
        if not is_chrome_infra_error(item.error):
            return "prod"

    return "infra"


def health_run_status(
    *,
    overall_ok: bool,
    lk_skipped_busy: bool = False,
    failure_kind: HealthFailureKind | None = None,
) -> HealthRunStatus:
    """Статус прогона для логов / Influx tag run_status."""
    if lk_skipped_busy and not overall_ok:
        return "skipped_busy"
    if overall_ok:
        return "ok"
    if failure_kind == "infra":
        return "infra"
    return "fail"
