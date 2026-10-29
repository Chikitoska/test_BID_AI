#!/usr/bin/env python3
"""Проверка: MONITOR_ANALYTICS_UID в cookie (SoT) и POST /events (лендинг + ЛК)."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from config.lk_settings import LK_CREDENTIALS_SET  # noqa: E402
from monitor.config import (  # noqa: E402
    MONITOR_ANALYTICS_UID,
    MONITOR_SPA_ROOT_DOMAIN,
    SPA_USER_ID_COOKIE_KEY,
)
from pages.lk_flow import LkFlow  # noqa: E402
from selenium import webdriver  # noqa: E402
from selenium.common.exceptions import TimeoutException  # noqa: E402
from selenium.webdriver.chrome.options import Options  # noqa: E402
from selenium.webdriver.chrome.service import Service  # noqa: E402
from utils.selenium_factory import (  # noqa: E402
    GPN_SPA_LOCALSTORAGE_KEY,
    _build_chrome_options,
    _inject_gpn_spa_analytics_uid,
    _resolve_chromedriver_path,
)
from utils.spa_analytics import extract_uids_from_events_body  # noqa: E402

LANDING_URL = "https://bid.gazprom-neft.ru/"
KEYCLOAK_ORIGIN = "id.bid.gazprom-neft.ru"
LK_ORIGIN = "lk.bid.gazprom-neft.ru"
EVENTS_HOST = "spa-back.gazprom-neft.ru/events"


def _create_driver_with_network_log() -> webdriver.Chrome:
    # Как create_chrome_driver: на Mac headless часто хуже для PROD.
    use_headless = True
    if sys.platform == "darwin" and os.getenv("MONITOR_FORCE_HEADLESS") != "true":
        use_headless = False
    options: Options = _build_chrome_options(use_headless=use_headless)
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    chromedriver_path = _resolve_chromedriver_path()
    service = Service(executable_path=chromedriver_path) if chromedriver_path else Service()
    driver = webdriver.Chrome(service=service, options=options)
    _inject_gpn_spa_analytics_uid(driver)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.set_page_load_timeout(int(os.getenv("LK_PAGE_LOAD_TIMEOUT", "45")))
    return driver


def _cdp_spa_cookie(driver, expected_name: str) -> str | None:
    try:
        cookies = driver.execute_cdp_cmd("Network.getAllCookies", {}).get("cookies") or []
    except Exception as exc:
        print(f"WARN: CDP getAllCookies: {exc}")
        return None
    matches = [c for c in cookies if c.get("name") == expected_name]
    if not matches:
        print(f"CDP cookies: нет {expected_name!r} (всего {len(cookies)})")
        return None
    cookie = matches[0]
    print(
        f"CDP cookie {expected_name!r} domain={cookie.get('domain')!r} "
        f"value={cookie.get('value')!r}"
    )
    return str(cookie.get("value") or "") or None


def _collect_events_post_data(driver) -> list[str]:
    posts: list[str] = []
    for entry in driver.get_log("performance"):
        try:
            message = json.loads(entry["message"])["message"]
        except (KeyError, json.JSONDecodeError, TypeError):
            continue
        if message.get("method") != "Network.requestWillBeSent":
            continue
        params = message.get("params", {})
        request = params.get("request", {})
        url = request.get("url", "")
        if EVENTS_HOST not in url or request.get("method") != "POST":
            continue
        body = request.get("postData") or ""
        if not body:
            request_id = params.get("requestId")
            if request_id:
                try:
                    data = driver.execute_cdp_cmd(
                        "Network.getRequestPostData", {"requestId": request_id}
                    )
                    body = data.get("postData") or ""
                except Exception:
                    body = ""
        posts.append(body)
    return posts


def _uids_from_post(post_data: str) -> list[str]:
    return extract_uids_from_events_body(post_data)


def _read_gpn_spa_uid(driver) -> str | None:
    """Опционально: localStorage не SoT, только для info/warn."""
    key = GPN_SPA_LOCALSTORAGE_KEY
    try:
        return driver.execute_script(
            "try { return localStorage.getItem(arguments[0]); } catch (e) { return null; }",
            key,
        )
    except Exception as exc:
        print(f"WARN: localStorage недоступен ({exc.__class__.__name__})")
        return None


def _read_spa_user_cookie(driver) -> str | None:
    """Аналог фронтового getCookie(SPA_USER_ID_KEY) — источник истины."""
    name = SPA_USER_ID_COOKIE_KEY.strip() or "gpn_spa_custom_user_id_cookie"
    try:
        return driver.execute_script(
            """
            const name = arguments[0];
            const value = '; ' + document.cookie;
            const parts = value.split('; ' + name + '=');
            if (parts.length === 2) {
              return parts.pop().split(';').shift() || null;
            }
            return null;
            """,
            name,
        )
    except Exception as exc:
        print(f"WARN: document.cookie недоступен ({exc.__class__.__name__})")
        return None


def _verify_events_context(
    driver,
    *,
    expected: str,
    context_label: str,
    require_posts: bool = True,
    require_cookie: bool = True,
) -> bool:
    print(f"\n--- {context_label} ---")
    print(f"URL: {driver.current_url}")
    storage_uid = _read_gpn_spa_uid(driver)
    cookie_uid = _read_spa_user_cookie(driver)
    if not cookie_uid:
        cookie_uid = _cdp_spa_cookie(driver, SPA_USER_ID_COOKIE_KEY.strip())
    posts = _collect_events_post_data(driver)
    uids = [u for p in posts for u in _uids_from_post(p)]

    print(f"cookie[{SPA_USER_ID_COOKIE_KEY!r}] = {cookie_uid!r}")
    print(f"localStorage.{GPN_SPA_LOCALSTORAGE_KEY} = {storage_uid!r} (optional)")
    print(f"POST /events (всего в сессии): {len(posts)}")
    if uids:
        print(f"uid в POST /events: {uids}")
    elif posts:
        print("WARN: POST /events есть, но uid в теле не разобран")
        print(f"тело[0]: {posts[0][:500]!r}")

    ok = True
    if require_cookie and cookie_uid != expected:
        print(
            f"FAIL: cookie uid {cookie_uid!r} != {expected!r} "
            f"(ключ {SPA_USER_ID_COOKIE_KEY!r})"
        )
        ok = False

    if storage_uid is not None and storage_uid != expected:
        print(
            f"WARN: localStorage uid {storage_uid!r} != {expected!r} "
            f"(не SoT, не влияет на результат)"
        )

    if require_posts and not posts:
        print("FAIL: POST /events не обнаружен (аналитика не сработала?)")
        ok = False

    if require_posts and posts and not uids:
        print("FAIL: POST /events без uid в теле (ожидали фиксированный MONITOR_ANALYTICS_UID)")
        ok = False

    if uids and expected not in uids:
        print("FAIL: ожидаемый uid не найден в теле запросов")
        ok = False

    foreign = [u for u in uids if u != expected]
    if foreign:
        print(f"FAIL: найдены другие uid (случайная генерация?): {foreign}")
        ok = False

    if ok:
        print(f"OK: {context_label} — фиксированный uid в cookie, без post-генерации")
    return ok


def _open_or_warn(driver, url: str, label: str) -> None:
    try:
        driver.get(url)
    except TimeoutException as exc:
        print(f"WARN: timeout {label}: {exc.__class__.__name__} — проверяем cookie/events как есть")
    except Exception as exc:
        print(f"WARN: навигация {label}: {exc}")


def _http_page_loaded(driver) -> bool:
    url = driver.current_url or ""
    return url.startswith("http://") or url.startswith("https://")


def _verify_landing(driver, expected: str) -> bool:
    print(f"Открываем {LANDING_URL} …")
    _open_or_warn(driver, LANDING_URL, "лендинг")
    if _http_page_loaded(driver):
        time.sleep(8)
        return _verify_events_context(driver, expected=expected, context_label="Лендинг")
    print(f"FAIL: лендинг не открылся (URL={driver.current_url!r}) — нет сети до PROD с этой машины")
    _cdp_spa_cookie(driver, SPA_USER_ID_COOKIE_KEY.strip())
    return False


def _verify_keycloak_cookie(driver, expected: str) -> bool:
    """На Keycloak counter может не жить — достаточно shared cookie на root domain."""
    print(f"\n--- Keycloak cookie ({KEYCLOAK_ORIGIN}) ---")
    # Минимальный URL realm; даже 404/редирект даёт документ на нужном домене.
    url = f"https://{KEYCLOAK_ORIGIN}/"
    print(f"Открываем {url} …")
    _open_or_warn(driver, url, "Keycloak")
    if not _http_page_loaded(driver):
        print(f"SKIP/WARN: Keycloak не открылся (URL={driver.current_url!r})")
        return True
    time.sleep(3)
    cookie_uid = _read_spa_user_cookie(driver)
    if not cookie_uid:
        cookie_uid = _cdp_spa_cookie(driver, SPA_USER_ID_COOKIE_KEY.strip())
    print(f"URL: {driver.current_url}")
    print(f"cookie[{SPA_USER_ID_COOKIE_KEY!r}] = {cookie_uid!r}")
    if KEYCLOAK_ORIGIN not in driver.current_url and cookie_uid != expected:
        print("SKIP/WARN: не на домене Keycloak и cookie не видна")
        return True
    if cookie_uid == expected:
        print("OK: shared cookie видна на Keycloak-домене")
        return True
    print(
        f"FAIL: cookie на Keycloak {cookie_uid!r} != {expected!r} "
        f"(root_domain={MONITOR_SPA_ROOT_DOMAIN!r})"
    )
    return False


def _verify_lk(driver, expected: str) -> bool:
    if not LK_CREDENTIALS_SET:
        print("\n--- ЛК ---")
        print("SKIP: нет BID_USERNAME/BID_PASSWORD/BID_TOTP_SECRET — проверка ЛК пропущена")
        return True

    print("\nВход в ЛК …")
    LkFlow(driver).login()
    time.sleep(8)
    if LK_ORIGIN not in driver.current_url:
        print(f"FAIL: после входа не на домене ЛК (URL: {driver.current_url})")
        return False
    return _verify_events_context(driver, expected=expected, context_label="ЛК")


def main() -> int:
    expected = MONITOR_ANALYTICS_UID.strip()
    if not expected:
        print("FAIL: MONITOR_ANALYTICS_UID не задан в monitor/.env")
        return 1

    print("=== Verify GPN SPA analytics uid (лендинг + Keycloak cookie + ЛК) ===")
    print(f"Ожидаемый uid: {expected}")
    print(f"cookie key (SoT): {SPA_USER_ID_COOKIE_KEY!r}")
    print(f"root_domain: {MONITOR_SPA_ROOT_DOMAIN!r}")

    landing_ok = False
    keycloak_ok = True
    lk_ok = True
    prod_reachable = False

    driver = _create_driver_with_network_log()
    try:
        print("\n--- CDP inject (до навигации) ---")
        cdp_uid = _cdp_spa_cookie(driver, SPA_USER_ID_COOKIE_KEY.strip())
        if cdp_uid != expected:
            print(f"FAIL: CDP cookie {cdp_uid!r} != {expected!r}")
            landing_ok = False
        else:
            print("OK: фиксированный uid записан в cookie до открытия PROD")
        landing_ok = _verify_landing(driver, expected) and cdp_uid == expected
        prod_reachable = _http_page_loaded(driver)
        if prod_reachable:
            keycloak_ok = _verify_keycloak_cookie(driver, expected)
        else:
            print("SKIP: Keycloak — PROD с этой машины недоступен")
            keycloak_ok = True
    finally:
        driver.quit()

    if LK_CREDENTIALS_SET and not prod_reachable:
        print("SKIP: ЛК — PROD с этой машины недоступен")
    elif LK_CREDENTIALS_SET:
        driver = _create_driver_with_network_log()
        try:
            lk_ok = _verify_lk(driver, expected)
        finally:
            driver.quit()

    if landing_ok and keycloak_ok and lk_ok:
        print(
            "\nOK: MONITOR_ANALYTICS_UID в cookie и POST /events "
            "(лендинг; Keycloak cookie; ЛК при наличии credentials)"
        )
        return 0

    print("\nFAIL: проверка uid не пройдена")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
