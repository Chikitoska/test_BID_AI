"""Краткие описания HTTP-проверок лендинга (для логов, Grafana, алертов)."""

LK_CHECK_LABELS: dict[str, str] = {
    "lk_auth_login": "ЛК: вход (логин + 2FA)",
    "lk_redirect": "ЛК: редирект после входа",
    "lk_user_fio": "ЛК: ФИО в шапке",
    "lk_company_badge": "ЛК: компания в шапке",
}

CHECK_LABELS: dict[str, str] = {
    "main_page": "Главная страница лендинга",
    "config": "Настройки сайта (config.json)",
    "service_providers": "Список сервисов на главной",
    "legal_documents_bulk": "Юридические документы (оферты, cookie)",
    "version": "Версия фронтенда",
    "spa_counter_js": "Скрипт веб-аналитики",
    "external_counter.js": "Внешний счётчик посещений",
}


def get_check_label(name: str) -> str:
    if name in LK_CHECK_LABELS:
        return LK_CHECK_LABELS[name]
    return CHECK_LABELS.get(name, name)


def get_check_order(name: str) -> int:
    for index, key in enumerate(CHECK_LABELS, start=1):
        if key == name:
            return index
    return 100
