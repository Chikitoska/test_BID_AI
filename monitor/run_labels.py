"""Русские названия типов прогона — для Telegram и email."""

from __future__ import annotations

# run_type → заголовок в Telegram / тема письма
RUN_TYPE_LABELS: dict[str, str] = {
    "probe": "Мониторинг каждые 5 мин",  # legacy run_light
    "health": "Лендинг + мин ЛК (каждые 5 мин)",
    "full": "Лендинг + API autotests",
    "lk_pytest": "Боевой прогон ЛК (каждые 2 ч)",
    "lk": "Лендинг + мин ЛК",
}

# run_type → где искать ошибку (вторая строка алерта)
RUN_TYPE_ZONES: dict[str, str] = {
    "probe": "HTTP-проверки лендинга (run_light)",
    "health": "лендинг (HTTP) или личный кабинет (run_health_monitor)",
    "full": "HTTP/API лендинга и pytest tests/api (run_daily)",
    "lk_pytest": "pytest tests/lk — авторизация и UI ЛК (run_lk_pytest)",
    "lk": "личный кабинет",
}


def get_run_label(run_type: str) -> str:
    return RUN_TYPE_LABELS.get(run_type, "Мониторинг BID")


def get_run_zone(run_type: str) -> str:
    return RUN_TYPE_ZONES.get(run_type, "BID")
