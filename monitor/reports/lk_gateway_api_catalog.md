# LK gateway / backend API catalog (Заявки)

- Generated: `2026-10-04T12:01:03+03:00`
- Output: `/Users/nikitasmirnov/Projects/test_BID_AI/artifacts/lk_gateway_requests_20261004_120103.md`
- Unique endpoints (METHOD + path): **26**
- Raw backend hits (before dedupe): **44**
- GOST/cert blocked: **yes**

## Flow steps

1. Reachability probe: ok=False status=None error='<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)>'
1. Chrome started with performance log + Network.enable
1. Login OK (landing → Keycloak + TOTP → ЛК)
1. LK ready: `https://lk.bid.gazprom-neft.ru/service-providers`
1. Opened «Заявки»: `https://lk.bid.gazprom-neft.ru/data-change-requests?tab=my&status=active`
1. Clicked «Подать заявку» (menu/open templates)
1. FAILED template «На куратора»: Не найден кликабельный текст из ['На куратора']; last=None
1. FAILED template «Повышение уровня аккредитации»: Не найден кликабельный текст из ['Повышение уровня аккредитации']; last=None

## Reachability probe

- URL: `https://bid.gazprom-neft.ru/`
- OK: `False` status=`None`
- Error: `<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)>`

## GOST / certificates

- Probe reported certificate/SSL issue: `<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)>`

### How to install corporate / GOST certs for Chrome (macOS) later

1. Obtain the corporate root/intermediate CA (often `.cer` / `.crt`) from IT / CryptoPro docs.
2. Open **Keychain Access** → login or System keychain → **File → Import Items…** → select the cert.
3. Double-click the imported cert → **Trust** → set **When using this certificate** to **Always Trust**.
4. Restart Chrome. Confirm `chrome://certificate-manager` (or macOS Keychain) shows the CA.
5. If the site still requires GOST TLS (CryptoPro CSP / CryptoPro Browser plugin), install the vendor plugin for Chrome and follow Gazprom Neft / BID internal instructions — standard Chrome alone may reject GOST-only endpoints.
6. Alternative for automation-only: ensure the host trusts the CA system-wide (`security add-trusted-cert` on macOS) so Selenium Chrome inherits trust.

## Errors / blockers

- BID landing not reachable from this environment (status=None, error='<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)>'). Cursor local proxy may return 403 CONNECT; without proxy DNS may fail. Re-run …
- Template «На куратора» failed: Не найден кликабельный текст из ['На куратора']; last=None
- Template «Повышение уровня аккредитации» failed: Не найден кликабельный текст из ['Повышение уровня аккредитации']; last=None

## Catalog table

| METHOD | URL path | status | count |
| --- | --- | --- | ---: |
| `GET` | `bid.gazprom-neft.ru/api/gateway/global/legal-documents/v1` | 200 | 1 |
| `GET` | `bid.gazprom-neft.ru/api/gateway/public/api/public/service-provider` | 200 | 1 |
| `GET` | `gost-lk.bid.gazprom-neft.ru/api/gost/request/accreditation/draft/current` | 0 | 1 |
| `OPTIONS` | `gost-lk.bid.gazprom-neft.ru/api/gost/request/accreditation/draft/current` | 0 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/agg-update-profiles-list/v1` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/applications-available/v1` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/global/country/v1` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/global/currency/v1` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/global/phone-code/v1` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/me` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/me/bid` | 200 | 3 |
| `GET` | `lk.bid.gazprom-neft.ru/api/me/bid/accreditation` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/me/bid/agreement-accepts` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/notifications/bell` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/public/captcha` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/public/frontend/config` | 200 | 3 |
| `GET` | `lk.bid.gazprom-neft.ru/api/public/legal-docs` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/request/BK_ACCREDITATION_LEVEL_UP/current/exists` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/request/ROLE_CURATOR_KZ` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/request/ROLE_CURATOR_KZ/current/exists` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/requests/active` | 200 | 2 |
| `GET` | `lk.bid.gazprom-neft.ru/api/requests/archived` | 403 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/service-provider` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/service-provider/tags` | 200 | 1 |
| `GET` | `lk.bid.gazprom-neft.ru/api/uaa/me` | 200 | 1 |
| `POST` | `spa-back.gazprom-neft.ru/events` | 200 | 6 |

## Optional raw list (redacted)

| METHOD | status | URL (redacted) |
| --- | --- | --- |
| `GET` | 200 | `https://bid.gazprom-neft.ru/api/gateway/public/api/public/service-provider` |
| `GET` | 200 | `https://bid.gazprom-neft.ru/api/gateway/global/legal-documents/v1?filtering=name%20in%20(BID_Agreement_processing_of_personal_data,BID_Agreement_processing_of_personal_data_CURATOR,BID_Policy_processing_of_personal_data,BID_Agreement_of_using,BID_Advertising_consent,Policy_using_of_cookie,BID_Services_and_partners,BID_Agreement_processing_of_personal_data_for_visitors)%20and%20isValid%20eq%20true` |
| `POST` | 200 | `https://spa-back.gazprom-neft.ru/events` |
| `POST` | 200 | `https://spa-back.gazprom-neft.ru/events` |
| `POST` | 200 | `https://spa-back.gazprom-neft.ru/events` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/captcha` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/global/country/v1?pageSize=1000` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/global/currency/v1?pageSize=1000` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/global/phone-code/v1?pageSize=1000` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/legal-docs` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/frontend/config` |
| `POST` | 200 | `https://spa-back.gazprom-neft.ru/events` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/captcha` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/global/country/v1?pageSize=1000` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/global/currency/v1?pageSize=1000` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/global/phone-code/v1?pageSize=1000` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/legal-docs` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/frontend/config` |
| `POST` | 200 | `https://spa-back.gazprom-neft.ru/events` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me/bid` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/public/frontend/config` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/notifications/bell` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/applications-available/v1` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me/bid/agreement-accepts` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/uaa/me` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me/bid` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me/bid/accreditation` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/request/BK_ACCREDITATION_LEVEL_UP/current/exists` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/request/ROLE_CURATOR_KZ` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/request/ROLE_CURATOR_KZ/current/exists` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/service-provider` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/service-provider/tags` |
| `POST` | 200 | `https://spa-back.gazprom-neft.ru/events` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me/bid` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/agg-update-profiles-list/v1?filtering=requestType%20eq%20%27EMPLOYEE%27&sort=status%2Cdesc&page=0&pageSize=10` |
| `GET` | 0 | `https://gost-lk.bid.gazprom-neft.ru/api/gost/request/accreditation/draft/current` |
| `GET` | 403 | `https://lk.bid.gazprom-neft.ru/api/requests/archived` |
| `GET` | — | `https://lk.bid.gazprom-neft.ru/api/requests/active` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/me/bid/accreditation` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/applications-available/v1` |
| `OPTIONS` | 0 | `https://gost-lk.bid.gazprom-neft.ru/api/gost/request/accreditation/draft/current` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/requests/active` |
| `GET` | 200 | `https://lk.bid.gazprom-neft.ru/api/notifications/bell` |

## Re-run

```bash
# Prefer BID network path (often VPN OFF). Cursor agent may need VPN ON.
cd /Users/nikitasmirnov/Projects/test_BID_AI
# ensure monitor/.env has BID_USERNAME / BID_PASSWORD / BID_TOTP_SECRET
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy
.venv/bin/python scripts/capture_lk_gateway_apis.py --headed \
  --out artifacts/lk_gateway_requests_$(date +%Y%m%d_%H%M%S).md \
  --also-report
```

Do not merge this catalog into main until endpoints are reviewed/kept.
