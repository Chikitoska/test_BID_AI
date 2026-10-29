"""Мониторинг ЛК: лёгкий (prod) и полный (только pytest)."""

from __future__ import annotations

import time

from config.lk_settings import (
    BID_EXPECTED_COMPANY,
    BID_EXPECTED_FIO,
    BID_LK_EXPECTED_URL,
    LANDING_BASE_URL,
)
from monitor.checks import CheckResult
from monitor.config import MONITOR_HTTP_ERROR_RETRIES, MONITOR_HTTP_ERROR_RETRY_DELAY_SEC
from monitor.http_status import results_have_http_4xx_or_5xx
from monitor.secrets_redact import redact_secrets
from pages.chatbot_widget import ChatbotWidget
from pages.lk_flow import LkAuthError, LkFlow
from pages.lk_page import LkPage
from pages.mincifry_page import MincifryPage
from utils.lk_modals import accept_lk_consent_modals
from utils.selenium_factory import create_chrome_driver


def _result(
    name: str,
    *,
    success: bool,
    duration_ms: float,
    error: str = "",
    url: str = "",
) -> CheckResult:
    return CheckResult(
        name=name,
        url=url or BID_LK_EXPECTED_URL,
        method="UI",
        success=success,
        http_code=200 if success else 0,
        duration_ms=duration_ms,
        error=error,
    )


def _run_chatbot_steps(driver, *, prefix: str, url: str) -> list[CheckResult]:
    bot = ChatbotWidget(driver)
    results: list[CheckResult] = []
    try:
        for name, action in bot.health_steps(prefix):
            item = _run_step(name, action)
            item.url = url
            results.append(item)
            if not item.success:
                break
        return results
    finally:
        bot.close()


def _run_step(name: str, action) -> CheckResult:
    start = time.perf_counter()
    try:
        action()
        return _result(name, success=True, duration_ms=(time.perf_counter() - start) * 1000)
    except Exception as exc:
        return _result(
            name,
            success=False,
            duration_ms=(time.perf_counter() - start) * 1000,
            error=redact_secrets(str(exc)),
        )


def _should_retry_lk(results: list[CheckResult], *, attempt: int, max_attempts: int) -> bool:
    if attempt >= max_attempts or not results:
        return False
    if all(item.success for item in results):
        return False
    if results_have_http_4xx_or_5xx(results):
        return True
    auth = next((item for item in results if item.name == "lk_auth_login"), None)
    return auth is not None and not auth.success and attempt == 1


def run_lk_monitor_checks(*, include_lk: bool = True) -> list[CheckResult]:
    """Health UI: чат-бот лендинга всегда; ЛК (вход/ФИО/компания/чат-бот) опционально.

    При 4xx/5xx (например /error/500) повторяет сценарий в том же прогоне
    с паузой ~90 с — алерт только если ошибка подтвердилась.
    """
    max_attempts = 1 + max(1, MONITOR_HTTP_ERROR_RETRIES)
    last_results: list[CheckResult] = []

    for attempt in range(1, max_attempts + 1):
        last_results = _run_lk_monitor_checks_once(include_lk=include_lk)
        if not _should_retry_lk(last_results, attempt=attempt, max_attempts=max_attempts):
            return last_results

        http_err = results_have_http_4xx_or_5xx(last_results)
        delay = MONITOR_HTTP_ERROR_RETRY_DELAY_SEC if http_err else 3
        kind = "4xx/5xx" if http_err else "auth"
        failed = next((r for r in last_results if not r.success), None)
        detail = (failed.error if failed else "")[:160]
        print(
            f"[lk] {kind} на попытке {attempt}/{max_attempts}: {detail}. "
            f"Повтор через {delay} с…",
            flush=True,
        )
        time.sleep(delay)

    return last_results


def _run_lk_monitor_checks_once(*, include_lk: bool = True) -> list[CheckResult]:
    driver = None
    results: list[CheckResult] = []
    flow: LkFlow | None = None

    try:
        driver = create_chrome_driver()
        flow = LkFlow(driver)
        flow.open_landing()
        results.extend(_run_chatbot_steps(driver, prefix="landing_chatbot", url=LANDING_BASE_URL))

        if not include_lk:
            return results

        results.append(
            _run_step("lk_auth_login", lambda: flow.login(already_on_landing=True))
        )
        if not results[-1].success:
            return results

        results.append(_run_step("lk_redirect", lambda: _has_lk_session(flow)))
        if not results[-1].success:
            return results

        accept_lk_consent_modals(driver)
        page = LkPage(driver)

        results.append(_run_step("lk_user_fio", lambda: _check_fio(page)))
        results.append(_run_step("lk_company_badge", lambda: _check_company(page)))
        results.extend(_run_chatbot_steps(driver, prefix="lk_chatbot", url=BID_LK_EXPECTED_URL))
        return results
    finally:
        if driver is not None:
            driver.quit()


run_lk_checks = run_lk_monitor_checks


def run_mincifry_checks() -> list[CheckResult]:
    """Дневной прогон: баннер Минцифр → страница Яндекс Браузера/сертификатов, FAQ, футер."""
    driver = None
    results: list[CheckResult] = []
    try:
        driver = create_chrome_driver()
        driver.get(LANDING_BASE_URL)
        time.sleep(1.5)
        page = MincifryPage(driver)
        for name, action in page.health_steps():
            item = _run_step(name, action)
            item.url = driver.current_url or LANDING_BASE_URL
            print(f"  {name} url={item.url}", flush=True)
            results.append(item)
            if not item.success:
                break
        return results
    except Exception as exc:
        return [
            _result(
                "landing_mincifry",
                success=False,
                duration_ms=0,
                error=redact_secrets(str(exc)),
                url=LANDING_BASE_URL,
            )
        ]
    finally:
        if driver is not None:
            driver.quit()


def _has_lk_session(flow: LkFlow) -> None:
    if not flow._has_lk_session():
        raise LkAuthError("Редirect в ЛК не выполнен")


def _check_fio(page: LkPage) -> None:
    fio = page.read_user_fio()
    if not fio:
        raise LkAuthError("В шапке ЛК нет ФИО")
    if BID_EXPECTED_FIO and fio != BID_EXPECTED_FIO:
        raise LkAuthError("Неверное ФИО в шапке ЛК")


def _check_company(page: LkPage) -> None:
    company = page.read_user_company()
    if not company:
        raise LkAuthError("В шапке ЛК нет названия компании")
    if BID_EXPECTED_COMPANY and company != BID_EXPECTED_COMPANY:
        raise LkAuthError(
            f"Неверная компания в шапке ЛК: факт={company!r}, ожидалось={BID_EXPECTED_COMPANY!r}"
        )
