"""Каталог API-методов лендинга bid.gazprom-neft.ru (из Network DevTools)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LandingApiMethod:
    name: str
    method: str
    path: str
    description: str
    base: str = "https://bid.gazprom-neft.ru"


# Все fetch/XHR методы, которые вызываются при загрузке лендинга
LANDING_API_METHODS: list[LandingApiMethod] = [
    LandingApiMethod(
        name="config",
        method="GET",
        path="/config.json",
        description="Конфигурация лендинга (ссылки, counterId, doc ids)",
    ),
    LandingApiMethod(
        name="service_providers",
        method="GET",
        path="/api/gateway/public/api/public/service-provider",
        description="Список сервис-провайдеров для карточек на лендинге",
    ),
    LandingApiMethod(
        name="legal_documents_bulk",
        method="GET",
        path=(
            "/api/gateway/global/legal-documents/v1"
            "?filtering=name%20in%20(BID_Agreement_processing_of_personal_data,"
            "BID_Agreement_processing_of_personal_data_CURATOR,"
            "BID_Policy_processing_of_personal_data,BID_Agreement_of_using,"
            "BID_Advertising_consent,Policy_using_of_cookie,BID_Services_and_partners,"
            "BID_Agreement_processing_of_personal_data_for_visitors)%20and%20isValid%20eq%20true"
        ),
        description="Пакетная загрузка юридических документов для футера/модалок",
    ),
    LandingApiMethod(
        name="version",
        method="GET",
        path="/version",
        description="Проверка версии/кеш-бастинг фронтенда",
    ),
]

# Внешние API лендинга (analytics)
EXTERNAL_LANDING_API_METHODS: list[LandingApiMethod] = [
    LandingApiMethod(
        name="spa_counter_js",
        method="GET",
        path="/static/counter.js",
        description="Скрипт счётчика аналитики",
        base="https://spa-back.gazprom-neft.ru",
    ),
    LandingApiMethod(
        name="spa_events",
        method="POST",
        path="/events",
        description="Отправка analytics-событий с лендинга",
        base="https://spa-back.gazprom-neft.ru",
    ),
]

# Юридические документы — отдельные GET из bulk-запроса
LEGAL_DOCUMENT_NAMES: list[str] = [
    "BID_Agreement_processing_of_personal_data",
    "BID_Agreement_processing_of_personal_data_CURATOR",
    "BID_Policy_processing_of_personal_data",
    "BID_Agreement_of_using",
    "BID_Advertising_consent",
    "Policy_using_of_cookie",
    "BID_Services_and_partners",
    "BID_Agreement_processing_of_personal_data_for_visitors",
]

# Теги вкладок на лендинге (фильтрация сервисов на UI)
LANDING_SERVICE_TAGS: list[str] = [
    "Потребителям",
    "Поддержка бизнеса",
    "Другие сервисы",
    "Отраслевые сервисы",
    "Поставщикам",
    "B2B Маркетплейс",
]

CONFIG_REQUIRED_KEYS: list[str] = [
    "gpn_spa_counter_id",
    "gpn_spa_counter_url",
    "gpn_spa_events_url",
    "registration_form_link",
    "services_info",
]

SERVICE_PROVIDER_REQUIRED_FIELDS: list[str] = [
    "id",
    "name",
    "description",
    "code",
    "tags",
]
