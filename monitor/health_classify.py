"""Классификация сбоев: prod (сеть/4xx/5xx) vs autotest (UI-флак / Chrome).

Оранжевый в Grafana = `run_status=autotest`.
Красный = сеть или HTTP 4xx/5xx (боевые/сетевые проблемы продукта).
Legacy alias `infra` принимается в TG suppress / Grafana (старые точки Influx).
"""

from __future__ import annotations

import re
from typing import Literal

from monitor.checks import CheckResult
from monitor.http_status import is_http_4xx_or_5xx, results_have_http_4xx_or_5xx

FailureKind = Literal["prod", "autotest"]
# Legacy: infra ≡ autotest (Chrome/WebDriver до переименования).
HealthFailureKind = Literal["prod", "autotest", "infra"]
HealthRunStatus = Literal["ok", "fail", "skipped_busy", "autotest", "infra"]

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

# Сниффер пуст при живой странице — harness, не «лендинг/spa-back лежит».
_HARNESS_EVENTS_MARKERS = (
    "post /events не обнаружен",
    "сниффер пуст",
    "harness:",
    "spaeventsharnesserror",
)

# spa-back 5xx/timeout — красный network, не harness.
_SPA_BACK_NETWORK_MARKERS = (
    "spaeventsnetworkerror",
    "spa-back http 5",
    "spa-back timeout",
    "spa-back dns",
)

# UI-ожидания/селекторы — проблема автотеста (оранжевый), не сеть/4xx/5xx.
_UI_WAIT_EXCEPTION_MARKERS = (
    "timeoutexception",
    "nosuchelementexception",
    "staleelementreferenceexception",
    "elementclickinterceptedexception",
    "elementnotinteractableexception",
    "elementnotvisibleexception",
    "invalidselectorexception",
    "assertionerror",
    "chatboterror",
    "mincifryerror",
    "темы не отображаются",
    "окно чат-бота",
    "вернуться в начало",
    "post /events не обнаружен",
    "сниффер пуст",
    "harness:",
    "spaeventsharnesserror",
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
    # Пустой Message: — chrome-infra только если это не именованный UI wait/assert.
    if _EMPTY_WEBDRIVER_MESSAGE_RE.search(text):
        if any(marker in lower for marker in _UI_WAIT_EXCEPTION_MARKERS):
            return False
        return True
    return False


def is_widget_icon_miss(error: str) -> bool:
    """Иконка чат-бота не появилась за ICON_WAIT_SEC — боевой fail виджета, не harness."""
    return "иконка чат-бота не отображается" in (error or "").lower()


def is_widget_assistant_down(error: str) -> bool:
    """Виджет открылся и сам показал «ассистент недоступен» — сбой бэкенда ассистента."""
    lower = (error or "").lower()
    return "ассистент недоступен" in lower


def is_ui_autotest_error(error: str) -> bool:
    """True для Selenium wait/assert/селектор — флак автотеста, не HTTP/сеть."""
    lower = (error or "").lower()
    if not lower.strip():
        return False
    if is_widget_icon_miss(error) or is_widget_assistant_down(error):
        return False
    return any(marker in lower for marker in _UI_WAIT_EXCEPTION_MARKERS)


def is_spa_back_network_error(error: str) -> bool:
    """spa-back 5xx/timeout — боевая сеть, не harness."""
    lower = (error or "").lower()
    if not lower.strip():
        return False
    if any(marker in lower for marker in _SPA_BACK_NETWORK_MARKERS):
        return True
    if "spa-back" in lower and (
        is_http_4xx_or_5xx(error=error) or "timeout" in lower or "timed out" in lower
    ):
        return True
    return False


def is_events_harness_miss(error: str) -> bool:
    """POST /events не пойман сниффером при живой странице — оранжевый harness."""
    lower = (error or "").lower()
    if is_spa_back_network_error(error):
        return False
    return any(marker in lower for marker in _HARNESS_EVENTS_MARKERS)


def is_monitor_disk_full(error: str) -> bool:
    """ENOSPC на VPS — harness монитора, не «PROD лежит»."""
    lower = (error or "").lower()
    return (
        "no space left on device" in lower
        or "errno 28" in lower
        or "enospc" in lower
    )


_LK_USER_COMPANY_CHECKS = frozenset({"lk_user_fio", "lk_company_badge"})
_LK_USER_COMPANY_TESTS = (
    "test_company_name_in_lk",
    "test_fio_in_service_provider",
    "test_company_in_service_provider",
)
_LK_USER_COMPANY_ERROR_MARKERS = (
    "микросервис user",
    "микросервис company",
    "фио в шапке лк не отобразилось",
    "фио в шапке лк пустое",
    "в шапке лк нет фио",
    "название компании в шапке лк не отобразилось",
    "название компании в шапке лк пустое",
    "в шапке лк нет названия компании",
)
_LK_ACCREDITATION_ERROR_MARKERS = (
    "микросервис accreditation",
    "не отображается текущий уровень аккредитации",
    "раздел «аккредитация» не",
    'раздел "аккредитация" не',
)


def is_hard_chrome_crash(error: str) -> bool:
    """Реальный краш Chrome/диск — не пустой Selenium wait на элементе."""
    lower = (error or "").lower()
    if is_monitor_disk_full(error):
        return True
    return any(marker in lower for marker in _CHROME_INFRA_MARKERS)


def is_lk_user_company_miss(*, error: str = "", check: str = "") -> bool:
    """ФИО/компания в шапке не пришли — микросервис user/company, не harness."""
    if is_hard_chrome_crash(error):
        return False
    name = (check or "").lower()
    if name in _LK_USER_COMPANY_CHECKS or any(token in name for token in _LK_USER_COMPANY_TESTS):
        return True
    lower = (error or "").lower()
    return any(marker in lower for marker in _LK_USER_COMPANY_ERROR_MARKERS)


def is_accreditation_miss(*, error: str = "", check: str = "") -> bool:
    """Раздел аккредитации пуст — микросервис accreditation, не UI-флак."""
    if is_hard_chrome_crash(error):
        return False
    name = (check or "").lower()
    if "accreditation" in name:
        return True
    lower = (error or "").lower()
    return any(marker in lower for marker in _LK_ACCREDITATION_ERROR_MARKERS)


def is_lk_ms_data_miss(*, error: str = "", check: str = "") -> bool:
    return is_lk_user_company_miss(error=error, check=check) or is_accreditation_miss(
        error=error, check=check
    )


def lk_ms_data_message(check: str, error: str = "", *, wait_sec: int = 30) -> str | None:
    """Человекочитаемый текст для bid_failure: какой микросервис не ответил."""
    if not is_lk_ms_data_miss(error=error, check=check):
        return None
    lower = (error or "").lower()
    first = (error or "").strip().splitlines()[0].strip() if error else ""
    if "микросервис" in first.lower():
        return first[:500]
    name = (check or "").lower()
    if (
        name == "lk_user_fio"
        or "fio" in name
        or "фио" in lower
        or "микросервис user" in lower
    ):
        return (
            f"ФИО в шапке ЛК не отобразилось за {wait_sec} с — "
            "микросервис user не ответил (сеть/PROD)"
        )
    if "accreditation" in name or "аккредит" in lower:
        return (
            "Раздел «Аккредитация» не отобразился — "
            "микросервис accreditation недоступен (сеть/PROD)"
        )
    return (
        f"Название компании в шапке ЛК не отобразилось за {wait_sec} с — "
        "микросервис company не ответил (сеть/PROD)"
    )


def is_autotest_error(error: str) -> bool:
    """Chrome/WebDriver или UI wait/assert — оранжевый (autotest)."""
    if (
        is_widget_icon_miss(error)
        or is_widget_assistant_down(error)
        or is_spa_back_network_error(error)
        or is_lk_user_company_miss(error=error)
        or is_accreditation_miss(error=error)
    ):
        return False
    if is_monitor_disk_full(error):
        return True
    return (
        is_chrome_infra_error(error)
        or is_ui_autotest_error(error)
        or is_events_harness_miss(error)
    )


def is_autotest_failure_kind(kind: str | None) -> bool:
    """True для autotest и legacy infra (старые метрики / вызовы)."""
    return kind in ("autotest", "infra")


def classify_health_failure(results: list[CheckResult]) -> FailureKind:
    """prod = сеть/4xx/5xx; autotest = UI-флак или Chrome/WebDriver.

    Если среди FAIL есть подтверждённый HTTP 4xx/5xx — всегда prod.
    Autotest только когда *все* упавшие проверки выглядят как автотест/браузер.
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
        # HTTP-проверка (лендинг / spa-back / ЛК) — сеть, не harness.
        if (item.method or "").upper() in ("GET", "POST", "HEAD"):
            return "prod"
        if (
            is_spa_back_network_error(item.error)
            or is_widget_icon_miss(item.error)
            or is_widget_assistant_down(item.error)
            or is_lk_ms_data_miss(error=item.error, check=item.name)
        ):
            return "prod"
        if not is_autotest_error(item.error):
            return "prod"

    return "autotest"


def health_run_status(
    *,
    overall_ok: bool,
    lk_skipped_busy: bool = False,
    failure_kind: HealthFailureKind | None = None,
    http_ok: bool = False,
) -> HealthRunStatus:
    """Статус прогона для логов / Influx tag run_status.

    Chrome busy при успешном HTTP лендинга — не красим весь health в skipped_busy.
    """
    if lk_skipped_busy:
        if http_ok or overall_ok:
            return "ok"
        return "skipped_busy"
    if overall_ok:
        return "ok"
    if is_autotest_failure_kind(failure_kind):
        return "autotest"
    return "fail"


def pytest_run_status(
    *,
    overall_ok: bool,
    failure_kind: FailureKind | None = None,
) -> str:
    """ok | fail | autotest — для bid_lk_pytest / bid_run."""
    if overall_ok:
        return "ok"
    if failure_kind == "autotest":
        return "autotest"
    return "fail"
