#!/usr/bin/env python3
"""Проверка: POST spa-back/events шлёт MONITOR_ANALYTICS_UID (лендинг + ЛК)."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from config.lk_settings import BID_LK_EXPECTED_URL, LK_CREDENTIALS_SET  # noqa: E402
from monitor.config import MONITOR_ANALYTICS_UID  # noqa: E402
from pages.lk_flow import LkFlow  # noqa: E402
from selenium import webdriver  # noqa: E402
from selenium.webdriver.chrome.options import Options  # noqa: E402
from selenium.webdriver.chrome.service import Service  # noqa: E402
from utils.selenium_factory import (  # noqa: E402
    _build_chrome_options,
    _inject_gpn_spa_analytics_uid,
    _resolve_chromedriver_path,
)

LANDING_URL = "https://bid.gazprom-neft.ru/"
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
    return driver.execute_script(
        "try { return localStorage.getItem('gpnSpaUid'); } catch (e) { return null; }"
    )


def _verify_events_context(
    driver,
    *,
    expected: str,
    context_label: str,
    require_posts: bool = True,
) -> bool:
    print(f"\n--- {context_label} ---")
    print(f"URL: {driver.current_url}")
    storage_uid = _read_gpn_spa_uid(driver)
    posts = _collect_events_post_data(driver)
    uids = [u for u in (_uid_from_post(p) for p in posts) if u]

    print(f"localStorage.gpnSpaUid = {storage_uid!r}")
    print(f"POST /events (всего в сессии): {len(posts)}")
    if uids:
        print(f"uid в POST /events: {uids}")

    ok = True
    if storage_uid != expected:
        print(f"FAIL: localStorage uid {storage_uid!r} != {expected!r}")
        ok = False

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
        print(f"OK: {context_label} — фиксированный uid, без post-генерации")
    return ok


def _verify_landing(driver, expected: str) -> bool:
    print(f"Открываем {LANDING_URL} …")
    driver.get(LANDING_URL)
    time.sleep(8)
    return _verify_events_context(driver, expected=expected, context_label="Лендинг")


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

    print("=== Verify GPN SPA analytics uid (лендинг + ЛК) ===")
    print(f"Ожидаемый uid: {expected}")

    landing_ok = False
    lk_ok = True

    driver = _create_driver_with_network_log()
    try:
        landing_ok = _verify_landing(driver, expected)
    finally:
        driver.quit()

    if LK_CREDENTIALS_SET:
        driver = _create_driver_with_network_log()
        try:
            lk_ok = _verify_lk(driver, expected)
        finally:
            driver.quit()

    if landing_ok and lk_ok:
        print("\nOK: лендинг и ЛК используют MONITOR_ANALYTICS_UID в localStorage и POST /events")
        return 0

    print("\nFAIL: проверка uid не пройдена")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
