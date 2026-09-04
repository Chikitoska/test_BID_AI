"""Мониторинг ЛК: лёгкий (prod) и полный (только pytest)."""

from __future__ import annotations

import time

from config.lk_settings import BID_EXPECTED_COMPANY, BID_EXPECTED_FIO, BID_LK_EXPECTED_URL
from monitor.checks import CheckResult
from monitor.secrets_redact import redact_secrets
from pages.lk_flow import LkAuthError, LkFlow
from pages.lk_page import LkPage
from utils.lk_modals import accept_lk_consent_modals
from utils.selenium_factory import create_chrome_driver


def _result(name: str, *, success: bool, duration_ms: float, error: str = "") -> CheckResult:
    return CheckResult(
        name=name,
        url=BID_LK_EXPECTED_URL,
        method="UI",
        success=success,
        http_code=200 if success else 0,
        duration_ms=duration_ms,
        error=error,
    )


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


def run_lk_monitor_checks() -> list[CheckResult]:
    """Лёгкий мониторинг ЛК: вход + ФИО и компания в шапке (~15–30 с).

    Тяжёлые проверки (витрина, аккредитация, Processor) — только в pytest tests/lk/.
    """
    last_results: list[CheckResult] = []
    for attempt in range(1, 3):
        last_results = _run_lk_monitor_checks_once()
        auth = last_results[0] if last_results else None
        if auth and auth.name == "lk_auth_login" and not auth.success and attempt < 2:
            print("[lk] повтор входа после ошибки авторизации…", flush=True)
            time.sleep(3)
            continue
        return last_results
    return last_results


def _run_lk_monitor_checks_once() -> list[CheckResult]:
    driver = None
    results: list[CheckResult] = []
    flow: LkFlow | None = None

    try:
        driver = create_chrome_driver()
        flow = LkFlow(driver)

        results.append(_run_step("lk_auth_login", lambda: flow.login()))
        if not results[-1].success:
            return results

        results.append(_run_step("lk_redirect", lambda: _has_lk_session(flow)))
        if not results[-1].success:
            return results

        accept_lk_consent_modals(driver)
        page = LkPage(driver)

        results.append(_run_step("lk_user_fio", lambda: _check_fio(page)))
        results.append(_run_step("lk_company_badge", lambda: _check_company(page)))
        return results
    finally:
        if driver is not None:
            driver.quit()


# Обратная совместимость (старое имя)
run_lk_checks = run_lk_monitor_checks


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
