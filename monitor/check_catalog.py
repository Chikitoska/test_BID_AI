"""Краткие описания HTTP-проверок лендинга (для логов, Grafana, алертов)."""

LK_CHECK_LABELS: dict[str, str] = {
    "lk_auth_login": "ЛК: вход (логин + 2FA)",
    "lk_redirect": "ЛК: редирект после входа",
    "lk_user_fio": "ЛК: ФИО в шапке",
    "lk_company_badge": "ЛК: компания в шапке",
    "lk_chatbot": "ЛК: чат-бот ассистент",
    "lk_chatbot_icon": "ЛК: иконка чат-бота",
    "lk_chatbot_topics": "ЛК: темы чат-бота",
    "lk_chatbot_question": "ЛК: выбор вопроса в чат-боте",
    "lk_chatbot_answer": "ЛК: ответ чат-бота",
    "lk_chatbot_nav": "ЛК: Назад / в начало чат-бота",
    "lk_chatbot_close": "ЛК: закрытие окна чат-бота",
    "lk_chatbot_events": "ЛК: SPA UUID в events чат-бота",
}

CHECK_LABELS: dict[str, str] = {
    "main_page": "Главная страница лендинга",
    "config": "Настройки сайта (config.json)",
    "service_providers": "Список сервисов на главной",
    "legal_documents_bulk": "Юридические документы (оферты, cookie)",
    "version": "Версия фронтенда",
    "spa_counter_js": "Скрипт веб-аналитики",
    "external_counter.js": "Внешний счётчик посещений",
    "landing_chatbot": "Лендинг: чат-бот ассистент",
    "landing_chatbot_icon": "Лендинг: иконка чат-бота",
    "landing_chatbot_topics": "Лендинг: темы чат-бота",
    "landing_chatbot_question": "Лендинг: выбор вопроса в чат-боте",
    "landing_chatbot_answer": "Лендинг: ответ чат-бота",
    "landing_chatbot_nav": "Лендинг: Назад / в начало чат-бота",
    "landing_chatbot_close": "Лендинг: закрытие окна чат-бота",
    "landing_chatbot_events": "Лендинг: SPA UUID в events чат-бота",
    "landing_mincifry": "Лендинг: страница Минцифр (сертификаты)",
    "landing_mincifry_banner": "Минцифр: блок на лендинге",
    "landing_mincifry_click": "Минцифр: блок кликабелен, открылась страница",
    "landing_mincifry_yandex": "Минцифр: установка Яндекс Браузера",
    "landing_mincifry_certs": "Минцифр: установка сертификатов",
    "landing_mincifry_faq": "Минцифр: блок частых вопросов",
    "landing_mincifry_faq_expand": "Минцифр: раскрытие частых вопросов",
    "landing_mincifry_footer": "Минцифр: футер на странице",
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
