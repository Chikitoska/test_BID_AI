"""Каталог BE API ЛК для daily/smoke polling (из capture Заявки 2026-10-04).

Источник: artifacts/lk_gateway_requests_20261004_120103.md /
monitor/reports/lk_gateway_api_catalog.md (26 unique METHOD+path).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LkBeEndpoint:
    """Один endpoint для HTTP smoke."""

    name: str
    method: str
    url: str
    expect_status: int = 200
    skip_reason: str | None = None


LK_ORIGIN = "https://lk.bid.gazprom-neft.ru"
BID_ORIGIN = "https://bid.gazprom-neft.ru"
GOST_ORIGIN = "https://gost-lk.bid.gazprom-neft.ru"
SPA_ORIGIN = "https://spa-back.gazprom-neft.ru"

# Query из реального capture — без них часть справочников отдаёт неполные ответы.
_LEGAL_DOCS_FILTER = (
    "?filtering=name%20in%20(BID_Agreement_processing_of_personal_data,"
    "BID_Agreement_processing_of_personal_data_CURATOR,"
    "BID_Policy_processing_of_personal_data,BID_Agreement_of_using,"
    "BID_Advertising_consent,Policy_using_of_cookie,BID_Services_and_partners,"
    "BID_Agreement_processing_of_personal_data_for_visitors)%20and%20isValid%20eq%20true"
)
_AGG_PROFILES_QS = (
    "?filtering=requestType%20eq%20%27EMPLOYEE%27"
    "&sort=status%2Cdesc&page=0&pageSize=10"
)

# Active GET endpoints that returned 200 in capture — expect HTTP 200.
LK_BE_ACTIVE_ENDPOINTS: list[LkBeEndpoint] = [
    LkBeEndpoint(
        name="gateway_legal_documents",
        method="GET",
        url=f"{BID_ORIGIN}/api/gateway/global/legal-documents/v1{_LEGAL_DOCS_FILTER}",
    ),
    LkBeEndpoint(
        name="gateway_service_provider",
        method="GET",
        url=f"{BID_ORIGIN}/api/gateway/public/api/public/service-provider",
    ),
    LkBeEndpoint(
        name="agg_update_profiles_list",
        method="GET",
        url=f"{LK_ORIGIN}/api/agg-update-profiles-list/v1{_AGG_PROFILES_QS}",
    ),
    LkBeEndpoint(
        name="applications_available",
        method="GET",
        url=f"{LK_ORIGIN}/api/applications-available/v1",
    ),
    LkBeEndpoint(
        name="global_country",
        method="GET",
        url=f"{LK_ORIGIN}/api/global/country/v1?pageSize=1000",
    ),
    LkBeEndpoint(
        name="global_currency",
        method="GET",
        url=f"{LK_ORIGIN}/api/global/currency/v1?pageSize=1000",
    ),
    LkBeEndpoint(
        name="global_phone_code",
        method="GET",
        url=f"{LK_ORIGIN}/api/global/phone-code/v1?pageSize=1000",
    ),
    LkBeEndpoint(
        name="me",
        method="GET",
        url=f"{LK_ORIGIN}/api/me",
    ),
    LkBeEndpoint(
        name="me_bid",
        method="GET",
        url=f"{LK_ORIGIN}/api/me/bid",
    ),
    LkBeEndpoint(
        name="me_bid_accreditation",
        method="GET",
        url=f"{LK_ORIGIN}/api/me/bid/accreditation",
    ),
    LkBeEndpoint(
        name="me_bid_agreement_accepts",
        method="GET",
        url=f"{LK_ORIGIN}/api/me/bid/agreement-accepts",
    ),
    LkBeEndpoint(
        name="notifications_bell",
        method="GET",
        url=f"{LK_ORIGIN}/api/notifications/bell",
    ),
    LkBeEndpoint(
        name="public_captcha",
        method="GET",
        url=f"{LK_ORIGIN}/api/public/captcha",
    ),
    LkBeEndpoint(
        name="public_frontend_config",
        method="GET",
        url=f"{LK_ORIGIN}/api/public/frontend/config",
    ),
    LkBeEndpoint(
        name="public_legal_docs",
        method="GET",
        url=f"{LK_ORIGIN}/api/public/legal-docs",
    ),
    LkBeEndpoint(
        name="request_accreditation_level_up_exists",
        method="GET",
        url=f"{LK_ORIGIN}/api/request/BK_ACCREDITATION_LEVEL_UP/current/exists",
    ),
    LkBeEndpoint(
        name="request_role_curator_kz",
        method="GET",
        url=f"{LK_ORIGIN}/api/request/ROLE_CURATOR_KZ",
    ),
    LkBeEndpoint(
        name="request_role_curator_kz_exists",
        method="GET",
        url=f"{LK_ORIGIN}/api/request/ROLE_CURATOR_KZ/current/exists",
    ),
    LkBeEndpoint(
        name="requests_active",
        method="GET",
        url=f"{LK_ORIGIN}/api/requests/active",
    ),
    LkBeEndpoint(
        name="service_provider",
        method="GET",
        url=f"{LK_ORIGIN}/api/service-provider",
    ),
    LkBeEndpoint(
        name="service_provider_tags",
        method="GET",
        url=f"{LK_ORIGIN}/api/service-provider/tags",
    ),
    LkBeEndpoint(
        name="uaa_me",
        method="GET",
        url=f"{LK_ORIGIN}/api/uaa/me",
    ),
]

# Included for catalog completeness but skipped until env/ACL ready.
LK_BE_SKIPPED_ENDPOINTS: list[LkBeEndpoint] = [
    LkBeEndpoint(
        name="gost_accreditation_draft_current",
        method="GET",
        url=f"{GOST_ORIGIN}/api/gost/request/accreditation/draft/current",
        skip_reason="GOST/CA later",
    ),
    LkBeEndpoint(
        name="gost_accreditation_draft_current_options",
        method="OPTIONS",
        url=f"{GOST_ORIGIN}/api/gost/request/accreditation/draft/current",
        skip_reason="GOST/CA later",
    ),
    LkBeEndpoint(
        name="requests_archived",
        method="GET",
        url=f"{LK_ORIGIN}/api/requests/archived",
        expect_status=403,
        skip_reason="403 ACL — permissions TBD (want 200 later)",
    ),
    LkBeEndpoint(
        name="spa_events",
        method="POST",
        url=f"{SPA_ORIGIN}/events",
        skip_reason="analytics POST — daily GET-only smoke",
    ),
]

LK_BE_ALL_ENDPOINTS: list[LkBeEndpoint] = [
    *LK_BE_ACTIVE_ENDPOINTS,
    *LK_BE_SKIPPED_ENDPOINTS,
]
