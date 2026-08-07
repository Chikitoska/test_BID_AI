"""Telegram-алерты при падении мониторинга."""

from __future__ import annotations

import re

import requests

from monitor.checks import CheckResult
from monitor.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_PROXY, TELEGRAM_VERBOSE, ALERTS_ENABLED


def send_telegram(text: str) -> bool:
    if not ALERTS_ENABLED:
        print("[alert] Telegram не настроен, пропуск алерта")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    proxies = None
    if TELEGRAM_PROXY:
        proxies = {"http": TELEGRAM_PROXY, "https": TELEGRAM_PROXY}

    try:
        response = requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=15,
            proxies=proxies,
        )
        response.raise_for_status()
        return True
    except requests.exceptions.ConnectTimeout:
        print("[alert] api.telegram.org недоступен (таймаут). TELEGRAM_PROXY в monitor/.env")
        return False
    except requests.exceptions.ConnectionError as exc:
        print(f"[alert] api.telegram.org недоступен: {exc}")
        print("[alert] Попробуйте: sysctl IPv6 off, или TELEGRAM_PROXY=socks5://...")
        return False


def short_status(result: CheckResult) -> str:
    """Краткий статус: HTTP-код или тип ошибки."""
    if result.http_code:
        return str(result.http_code)

    err = (result.error or "").lower()
    if "connecttimeout" in err or "timed out" in err or "max retries exceeded" in err:
        return "timeout"
    if "connection refused" in err:
        return "refused"
    if "name or service not known" in err:
        return "dns"
    for code in ("403", "404", "500", "502", "503", "504"):
        if code in err:
            return code

    match = re.search(r"HTTP (\d+)", result.error or "", re.I)
    if match:
        return match.group(1)

    return "error"


def _format_http_failures(failed_checks: list[CheckResult], *, limit: int = 8) -> list[str]:
    lines: list[str] = []
    for item in failed_checks[:limit]:
        status = short_status(item)
        ms = f"{item.duration_ms:.0f}ms"
        lines.append(f"• <code>{item.name}</code>: <b>{status}</b> ({ms})")

    if len(failed_checks) > limit:
        lines.append(f"• … ещё {len(failed_checks) - limit} проверок")
    return lines


def format_failure_alert(
    http_results: list[CheckResult],
    pytest_failed: int,
    pytest_output: str,
    *,
    run_type: str = "full",
) -> str:
    failed_checks = [r for r in http_results if not r.success]
    total = len(http_results)
    ok = total - len(failed_checks)

    if run_type == "full":
        title = f"🔴 BID Full — FAIL ({ok}/{total} HTTP"
        if pytest_failed:
            title += f", pytest −{pytest_failed}"
        title += ")"
    else:
        title = f"🔴 BID Probe — FAIL ({ok}/{total} OK)"

    lines = [f"<b>{title}</b>", ""]

    if failed_checks:
        lines.extend(_format_http_failures(failed_checks))

    if pytest_failed > 0:
        lines.append("")
        lines.append(f"<b>Pytest:</b> упало {pytest_failed}")
        if TELEGRAM_VERBOSE and pytest_output:
            snippet = pytest_output.strip()[-400:]
            lines.append(f"<pre>{snippet}</pre>")

    return "\n".join(lines)


def format_probe_failure_alert(http_results: list[CheckResult]) -> str:
    return format_failure_alert(http_results, pytest_failed=0, pytest_output="", run_type="probe")


def format_recovery_message() -> str:
    return "<b>🟢 BID Probe — OK</b>\n\nHTTP-проверки снова проходят."


def format_relay_ok_message() -> str:
    return "Все ок"


def format_relay_failure_message(
    failures: list[dict],
    *,
    run_type: str = "probe",
    pytest_failed: int = 0,
    pytest_total: int = 0,
) -> str:
    """Краткий алерт для Telegram relay: где упало и описание ошибки."""
    titles = {
        "probe": "Ошибка BID (лендинг)",
        "full": "Ошибка BID (autotests)",
        "lk": "Ошибка BID (ЛК)",
    }
    title = titles.get(run_type, "Ошибка BID")
    lines = [title, ""]

    if failures:
        for item in failures:
            name = item.get("name", "?")
            label = item.get("label", "")
            status = item.get("status", "error")
            detail = (item.get("detail") or "").strip()
            line_title = f"{name}: {status}"
            if label:
                line_title = f"{name} ({label}): {status}"
            lines.append(line_title)
            if detail and status not in detail:
                lines.append(detail)
            lines.append("")
    elif run_type == "full" and pytest_failed:
        lines.append("HTTP-проверки прошли.")
        lines.append("")

    if pytest_failed:
        lines.append(f"Pytest: упало {pytest_failed} из {pytest_total}")

    if len(lines) <= 2:
        return f"{title}\n\nНе удалось получить детали проверок."

    return "\n".join(lines).strip()


def failure_detail(result: CheckResult) -> str:
    if result.error:
        return result.error[:200]
    if result.http_code:
        return f"HTTP {result.http_code}"
    return "unknown error"


def failures_for_relay(failed_checks: list[CheckResult]) -> list[dict]:
    from monitor.check_catalog import get_check_label

    return [
        {
            "name": item.name,
            "label": get_check_label(item.name),
            "status": short_status(item),
            "detail": failure_detail(item),
        }
        for item in failed_checks
    ]


def format_success_message(passed: int, total: int, *, run_type: str = "full") -> str:
    if run_type == "full":
        return f"<b>🟢 BID Full — OK</b>\n\nHTTP + pytest: {passed}/{total}"
    return f"<b>🟢 BID Probe — OK</b>"
