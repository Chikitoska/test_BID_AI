"""Разбор упавших pytest-тестов для алертов и Grafana."""

from __future__ import annotations

import re
from typing import Literal

from monitor.metrics import FailureEvent

FailureKind = Literal["prod", "autotest"]

# Сеть / PROD / инфраструктура — алертим сразу (даже из боевого UI-прогона).
# Не ставить короткие/шумные подстроки вроде "dns" или просто "chromedriver":
# путь к chromedriver есть почти в любом Selenium-логе → ложный prod-алерт.
_PROD_MARKERS = (
    "Read timed out",
    "ConnectTimeout",
    "ConnectionError",
    "Connection refused",
    "ConnectionReset",
    "NameResolutionError",
    "Failed to establish a new connection",
    "Max retries exceeded",
    "HTTPConnectionPool",
    "HTTPSConnectionPool",
    "urllib3.exceptions",
    "SSLError",
    "SSLCertVerificationError",
    "502 Bad Gateway",
    "503 Service",
    "504 Gateway",
    "Gateway Time-out",
    "net::ERR_",
    "ERR_CONNECTION",
    "ERR_NAME_NOT_RESOLVED",
    "ERR_TIMED_OUT",
    "Temporary failure in name resolution",
    "SessionNotCreatedException",
    "chrome not reachable",
    "chromedriver unexpectedly exited",
    "Chrome failed to start",
    "session not created",
    "WebDriverException: Message: unknown error: net::",
    "/error/4",
    "/error/5",
    "HttpStatusError",
)

# Типичный хрупкий UI-автотест — в Grafana пишем, в TG/email не спамим.
_AUTOTEST_MARKERS = (
    "TimeoutException",
    "NoSuchElementException",
    "StaleElementReferenceException",
    "ElementClickInterceptedException",
    "ElementNotInteractableException",
    "ElementNotVisibleException",
    "AssertionError",
    "InvalidSelectorException",
    "Failed: Раздел",
    "не загрузился или нет текущего уровня",
    "Аккредитация",
    "page_error",
)

_URL_RE = re.compile(r"https?://[^\s\]\)\"'>,|;]+")
_EMPTY_MESSAGE_RE = re.compile(
    r"^(?:[\w.]+\.)?(?P<exc>\w+(?:Error|Exception|Failure))\s*:\s*Message:\s*$",
    re.IGNORECASE,
)
_EXC_PREFIX_RE = re.compile(
    r"^(?:[\w.]+\.)?(?P<exc>\w+(?:Error|Exception|Failure))\s*:\s*(?P<body>.*)$",
    re.DOTALL,
)

# Пустой Selenium Message → краткий смысл по типу исключения.
_EMPTY_MESSAGE_FALLBACKS: dict[str, str] = {
    "TimeoutException": "element not found / wait timed out",
    "NoSuchElementException": "element not found",
    "StaleElementReferenceException": "stale element reference",
    "ElementClickInterceptedException": "click intercepted",
    "ElementNotInteractableException": "element not interactable",
    "ElementNotVisibleException": "element not visible",
    "InvalidSelectorException": "invalid selector",
    "InvalidSessionIdException": "invalid session / browser closed",
    "NoSuchWindowException": "target window already closed",
    "WebDriverException": "webdriver error",
    "SessionNotCreatedException": "session not created",
}


def classify_lk_pytest_failure(output: str, *, failed: int = 0, total: int = 0) -> FailureKind:
    """prod = сеть/лежит сайт/инфра; autotest = селекторы/ожидания/assert UI."""
    text = output or ""
    lower = text.lower()

    if total == 0 and failed > 0:
        return "prod"

    prod_hit = any(marker.lower() in lower for marker in _PROD_MARKERS)
    autotest_hit = any(marker.lower() in lower for marker in _AUTOTEST_MARKERS)
    mass_fail = total > 0 and failed >= max(3, (total + 1) // 2)

    # Явная сеть/5xx/падение Chrome — всегда prod (даже если в логе есть UI-слова).
    if prod_hit:
        return "prod"

    # Массовый провал без сетевых маркеров — тоже prod (стенд/логин).
    if mass_fail:
        return "prod"

    # Одиночный UI/assert/pytest.fail — только Grafana.
    if autotest_hit:
        return "autotest"

    # Непонятный одиночный FAIL — не пейджим (пульс PROD = health каждые 5 мин).
    return "autotest"


def short_test_name(test_id: str) -> str:
    """tests/lk/foo.py::test_bar → test_bar."""
    if "::" in test_id:
        return test_id.split("::")[-1]
    return test_id


def extract_failure_url(text: str) -> str | None:
    """Первый осмысленный URL из текста ошибки/traceback (предпочитаем lk/bid)."""
    if not text:
        return None
    urls = _URL_RE.findall(text)
    if not urls:
        return None

    def _clean(url: str) -> str:
        return url.rstrip(".,;:)")

    preferred = (
        "lk.bid.",
        "bid.gazprom",
        "processor.gazprom",
        "auth.",
        "keycloak",
    )
    for url in urls:
        low = url.lower()
        if any(p in low for p in preferred) and "selenium.dev" not in low:
            return _clean(url)[:300]
    for url in urls:
        if "selenium.dev" in url.lower():
            continue
        return _clean(url)[:300]
    return None


def brief_exception_text(detail: str) -> str:
    """Сжимает Selenium/pytest detail: пустой Message → тип + fallback."""
    text = (detail or "").strip()
    if not text:
        return "unknown error"

    # Отрезаем Stacktrace / For documentation… — для Grafana нужна одна строка.
    cut = re.split(r"\n\s*(?:Stacktrace:|For documentation on this error)", text, maxsplit=1)
    text = cut[0].strip()
    # Первая строка часто достаточна; если body многострочный — склеиваем кратко.
    first_line = text.splitlines()[0].strip() if text else ""
    rest = " ".join(ln.strip() for ln in text.splitlines()[1:] if ln.strip())
    compact = f"{first_line} {rest}".strip() if rest and len(first_line) < 80 else first_line

    empty = _EMPTY_MESSAGE_RE.match(compact) or _EMPTY_MESSAGE_RE.match(first_line)
    if empty:
        exc = empty.group("exc")
        fallback = _EMPTY_MESSAGE_FALLBACKS.get(exc, "no details")
        return f"{exc}: {fallback}"

    # TimeoutException: Message:   (с пробелами) / Message:\n...
    soft_empty = re.match(
        r"^(?:[\w.]+\.)?(?P<exc>\w+(?:Error|Exception|Failure))\s*:\s*Message:\s*$",
        compact,
        re.IGNORECASE,
    )
    if soft_empty:
        exc = soft_empty.group("exc")
        fallback = _EMPTY_MESSAGE_FALLBACKS.get(exc, "no details")
        return f"{exc}: {fallback}"

    # selenium.common.exceptions.TimeoutException: Message: foo → TimeoutException: foo
    prefixed = _EXC_PREFIX_RE.match(compact)
    if prefixed:
        exc = prefixed.group("exc")
        body = prefixed.group("body").strip()
        if re.fullmatch(r"Message:\s*", body, re.IGNORECASE):
            fallback = _EMPTY_MESSAGE_FALLBACKS.get(exc, "no details")
            return f"{exc}: {fallback}"
        if body.lower().startswith("message:"):
            body = body.split(":", 1)[1].strip()
            if not body:
                fallback = _EMPTY_MESSAGE_FALLBACKS.get(exc, "no details")
                return f"{exc}: {fallback}"
            return f"{exc}: {body}"[:500]
        return f"{exc}: {body}"[:500] if body else f"{exc}: {_EMPTY_MESSAGE_FALLBACKS.get(exc, 'no details')}"

    return compact[:500]


def format_rich_failure_error(
    *,
    test_name: str,
    detail: str,
    url: str | None = None,
) -> str:
    """Имя теста [| URL] | краткая ошибка — для bid_failure / Grafana."""
    brief = brief_exception_text(detail)
    parts = [test_name.strip() or "unknown_test"]
    if url:
        parts.append(url)
    parts.append(brief)
    return " | ".join(parts)


def _section_blob_for_test(output: str, test_id: str) -> str:
    """Кусок FAILURES/ERRORS вокруг имени теста (для поиска URL)."""
    short = short_test_name(test_id)
    if not output or not short:
        return ""
    # Заголовок секции pytest: _____ test_name _____
    pattern = re.compile(
        rf"^_+\s*{re.escape(short)}\s*_+\s*$",
        re.MULTILINE,
    )
    match = pattern.search(output)
    if not match:
        # Иногда в заголовке полный node id
        pattern2 = re.compile(
            rf"^_+\s*.*{re.escape(short)}\s*_+\s*$",
            re.MULTILINE,
        )
        match = pattern2.search(output)
    if not match:
        return ""
    start = match.start()
    # До следующей секции / short summary / конца
    end_match = re.search(
        r"\n(?:=+\s*(?:short test summary|warnings summary|ERRORS|FAILURES)|_{5,})",
        output[match.end() :],
    )
    end = match.end() + end_match.start() if end_match else len(output)
    return output[start:end]


def parse_pytest_failures(output: str) -> list[FailureEvent]:
    """Строки FAILED/ERROR … → события для InfluxDB / таблицы Grafana."""
    events: list[FailureEvent] = []
    seen: set[str] = set()

    def _add(test_id: str, detail: str) -> None:
        if test_id in seen:
            return
        seen.add(test_id)
        short = short_test_name(test_id)
        label = test_id if len(test_id) <= 120 else f"…{test_id[-117:]}"
        blob = _section_blob_for_test(output, test_id)
        url = extract_failure_url(detail) or extract_failure_url(blob)
        error = format_rich_failure_error(test_name=short, detail=detail, url=url)
        events.append(FailureEvent(check=short[:128], label=label[:256], error=error[:2000]))

    for raw in output.splitlines():
        line = raw.strip()
        if not (line.startswith("FAILED ") or line.startswith("ERROR ")):
            continue
        match = re.match(r"(?:FAILED|ERROR)\s+(\S+)\s+-\s+(.*)", line)
        if match:
            _add(match.group(1), match.group(2).strip())
            continue
        match = re.match(r"(?:FAILED|ERROR)\s+(\S+)", line)
        if match:
            _add(match.group(1), "")

    # short test summary иногда единственное место с текстом ошибки
    if not events:
        in_summary = False
        for raw in output.splitlines():
            line = raw.strip()
            if line.startswith("=") and "short test summary" in line.lower():
                in_summary = True
                continue
            if in_summary and line.startswith("="):
                break
            if in_summary and (line.startswith("FAILED ") or line.startswith("ERROR ")):
                match = re.match(r"(?:FAILED|ERROR)\s+(\S+)\s+-\s+(.*)", line)
                if match:
                    _add(match.group(1), match.group(2).strip())

    return events


def pytest_failure_snippet(output: str, *, limit: int = 8) -> str:
    """Краткий список упавших тестов для Telegram."""
    events = parse_pytest_failures(output)
    if events:
        lines = [f"• {e.error[:240]}" for e in events[:limit]]
        if len(events) > limit:
            lines.append(f"• … ещё {len(events) - limit} тестов")
        return "\n".join(lines)
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    return "\n".join(lines[-8:])


def pytest_summary_failure(*, failed: int, total: int, output: str, crashed: bool = False) -> FailureEvent:
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    tail = "\n".join(lines[-6:])[:2000]
    if crashed:
        return FailureEvent(
            check="pytest",
            label="Pytest: ошибка окружения",
            error=f"Pytest не запустился:\n{tail}",
        )
    return FailureEvent(
        check="pytest",
        label=f"Pytest: упало {failed} из {total}",
        error=tail or f"упало {failed} из {total}",
    )
