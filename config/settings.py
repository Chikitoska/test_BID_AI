"""Конфигурация автотестов BID (без авторизации)."""

BASE_URL = "https://bid.gazprom-neft.ru/"
PAGE_TITLE = "Газпром Бизнес ID"

# Публичные API, которые должны отвечать 2xx при загрузке лендинга
PUBLIC_API_ENDPOINTS = [
    "/config.json",
    "/api/gateway/public/api/public/service-provider",
    (
        "/api/gateway/global/legal-documents/v1"
        "?filtering=name%20in%20(BID_Agreement_processing_of_personal_data,"
        "BID_Agreement_processing_of_personal_data_CURATOR,"
        "BID_Policy_processing_of_personal_data,BID_Agreement_of_using,"
        "BID_Advertising_consent,Policy_using_of_cookie,BID_Services_and_partners,"
        "BID_Agreement_processing_of_personal_data_for_visitors)%20and%20isValid%20eq%20true"
    ),
    "/version",
]

PUBLIC_EXTERNAL_URLS = [
    "https://spa-back.gazprom-neft.ru/static/counter.js",
]

# URL/паттерны авторизации — исключаем из проверок backend (Войти / Keycloak / OIDC)
AUTH_URL_PATTERNS = (
    "self-authentication",
    "openid-connect",
    "id.bid.gazprom-neft.ru",
    "/realms/",
    "/auth?",
    "login_required",
    "kc-login",
    "/protocol/openid-connect/",
)

HTTP_TIMEOUT = 30
PAGE_LOAD_TIMEOUT = 60
IMPLICIT_WAIT = 5
