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


def parse_pytest_failures(output: str) -> list[FailureEvent]:
    """Строки FAILED/ERROR … → события для InfluxDB / таблицы Grafana."""
    events: list[FailureEvent] = []
    seen: set[str] = set()

    def _add(test_id: str, detail: str) -> None:
        if test_id in seen:
            return
        seen.add(test_id)
        short = test_id.split("::")[-1] if "::" in test_id else test_id
        label = test_id if len(test_id) <= 120 else f"…{test_id[-117:]}"
        error = f"{test_id}: {detail}".strip(": ")
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
        lines = [f"• {e.label}: {e.error[:200]}" for e in events[:limit]]
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
