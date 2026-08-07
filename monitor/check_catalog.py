"""Краткие описания HTTP-проверок лендинга (для логов, Grafana, алертов)."""

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
    return CHECK_LABELS.get(name, name)
