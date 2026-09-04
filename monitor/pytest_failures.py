"""Разбор упавших pytest-тестов для алертов и Grafana."""

from __future__ import annotations

import re

from monitor.metrics import FailureEvent


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
