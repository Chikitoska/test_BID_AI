#!/usr/bin/env python3
"""Проверка: MONITOR_ANALYTICS_UID в cookie (SoT) и POST /events (лендинг + ЛК)."""

from __future__ import annotations

import json
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
from selenium.webdriver.chrome.options import Options  # noqa: E402
from selenium.webdriver.chrome.service import Service  # noqa: E402
from utils.selenium_factory import (  # noqa: E402
    GPN_SPA_LOCALSTORAGE_KEY,
    _build_chrome_options,
    _inject_gpn_spa_analytics_uid,
    _resolve_chromedriver_path,
)

LANDING_URL = "https://bid.gazprom-neft.ru/"
KEYCLOAK_ORIGIN = "id.bid.gazprom-neft.ru"
LK_ORIGIN = "lk.bid.gazprom-neft.ru"
EVENTS_HOST = "spa-back.gazprom-neft.ru/events"


def _create_driver_with_network_log() -> webdriver.Chrome:
    options: Options = _build_chrome_options(use_headless=True)
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    chromedriver_path = _resolve_chromedriver_path()
    service = Service(executable_path=chromedriver_path) if chromedriver_path else Service()
    driver = webdriver.Chrome(service=service, options=options)
    _inject_gpn_spa_analytics_uid(driver)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.set_page_load_timeout(60)
    return driver


def _collect_events_post_data(driver) -> list[str]:
    posts: list[str] = []
    for entry in driver.get_log("performance"):
        try:
            message = json.loads(entry["message"])["message"]
        except (KeyError, json.JSONDecodeError, TypeError):
            continue
        if message.get("method") != "Network.requestWillBeSent":
            continue
        request = message.get("params", {}).get("request", {})
        url = request.get("url", "")
        if EVENTS_HOST in url and request.get("method") == "POST":
            posts.append(request.get("postData") or "")
    return posts


def _uid_from_post(post_data: str) -> str | None:
    if not post_data:
        return None
    try:
        payload = json.loads(post_data)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict):
        uid = payload.get("uid")
        return str(uid) if uid else None
    return None


def _read_gpn_spa_uid(driver) -> str | None:
    """Опционально: localStorage не SoT, только для info/warn."""
    key = GPN_SPA_LOCALSTORAGE_KEY
    return driver.execute_script(
        "try { return localStorage.getItem(arguments[0]); } catch (e) { return null; }",
        key,
    )


def _read_spa_user_cookie(driver) -> str | None:
    """Аналог фронтового getCookie(SPA_USER_ID_KEY) — источник истины."""
    name = SPA_USER_ID_COOKIE_KEY.strip() or "gpn_spa_custom_user_id_cookie"
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
    posts = _collect_events_post_data(driver)
    uids = [u for u in (_uid_from_post(p) for p in posts) if u]

    print(f"cookie[{SPA_USER_ID_COOKIE_KEY!r}] = {cookie_uid!r}")
    print(f"localStorage.{GPN_SPA_LOCALSTORAGE_KEY} = {storage_uid!r} (optional)")
    print(f"POST /events (всего в сессии): {len(posts)}")
    if uids:
        print(f"uid в POST /events: {uids}")

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


def _verify_landing(driver, expected: str) -> bool:
    print(f"Открываем {LANDING_URL} …")
    driver.get(LANDING_URL)
    time.sleep(8)
    return _verify_events_context(driver, expected=expected, context_label="Лендинг")


def _verify_keycloak_cookie(driver, expected: str) -> bool:
    """На Keycloak counter может не жить — достаточно shared cookie на root domain."""
    print(f"\n--- Keycloak cookie ({KEYCLOAK_ORIGIN}) ---")
    # Минимальный URL realm; даже 404/редирект даёт документ на нужном домене.
    url = f"https://{KEYCLOAK_ORIGIN}/"
    print(f"Открываем {url} …")
    try:
        driver.get(url)
    except Exception as exc:
        print(f"WARN: навигация Keycloak: {exc}")
    time.sleep(3)
    cookie_uid = _read_spa_user_cookie(driver)
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

    driver = _create_driver_with_network_log()
    try:
        landing_ok = _verify_landing(driver, expected)
        keycloak_ok = _verify_keycloak_cookie(driver, expected)
    finally:
        driver.quit()

    if LK_CREDENTIALS_SET:
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
