"""Фабрика Chrome WebDriver для мониторинга и тестов ЛК."""

from __future__ import annotations

import os
import subprocess
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config.lk_settings import MONITOR_HEADLESS

try:
    from config.settings import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT
except ImportError:
    PAGE_LOAD_TIMEOUT = 60
    IMPLICIT_WAIT = 5

LK_PAGE_LOAD_TIMEOUT = int(os.getenv("LK_PAGE_LOAD_TIMEOUT", "30"))
LK_IMPLICIT_WAIT = float(os.getenv("LK_IMPLICIT_WAIT", "0"))

_CHROME_CANDIDATES = (
    "/usr/bin/google-chrome-stable",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
    "/snap/bin/chromium",
)

_CHROMEDRIVER_CANDIDATES = (
    "/usr/lib/chromium-browser/chromedriver",
    "/usr/lib/chromium/chromedriver",
    "/usr/bin/chromedriver",
    "/snap/bin/chromium.chromedriver",
)


def _chromedriver_ok(path: str) -> bool:
    if not path or not os.path.isfile(path) or not os.access(path, os.X_OK):
        return False
    try:
        proc = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=8,
        )
        return proc.returncode == 0 and "ChromeDriver" in (proc.stdout + proc.stderr)
    except (OSError, subprocess.TimeoutExpired):
        return False


def _resolve_chrome_binary() -> str:
    explicit = os.getenv("CHROME_BINARY", "").strip()
    if explicit and os.path.isfile(explicit) and os.access(explicit, os.X_OK):
        return explicit
    for path in _CHROME_CANDIDATES:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return ""


def _resolve_chromedriver_path() -> str:
    explicit = os.getenv("CHROMEDRIVER_PATH", "").strip()
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    for path in _CHROMEDRIVER_CANDIDATES:
        if path not in candidates:
            candidates.append(path)
    for path in candidates:
        if _chromedriver_ok(path):
            return path
    return ""

USER_AGENT = os.getenv(
    "MONITOR_USER_AGENT",
    "Mozilla/5.0 (compatible; BID-QA-Monitor/1.0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
)

# Должен совпадать с monitor/config.py — см. MONITOR_ANALYTICS_UID в monitor/.env
MONITOR_ANALYTICS_UID = os.getenv(
    "MONITOR_ANALYTICS_UID",
    "b1d00000-0000-4000-a000-000000000001",
)

# localStorage-ключ counter.js (spa-back) — оставляем для совместимости.
GPN_SPA_LOCALSTORAGE_KEY = "gpnSpaUid"

# Имя cookie фронта (константа SPA_USER_ID_KEY). В репо значения нет —
# уточнить у фронта фактическую строку; пока placeholder + override через env.
SPA_USER_ID_COOKIE_KEY = os.getenv("SPA_USER_ID_COOKIE_KEY", "spa_user_id")

# root_domain из конфига лендинга: общий для bid / id.bid / lk.bid.
# Cookie Domain=bid.gazprom-neft.ru покрывает все три неймспейса.
MONITOR_SPA_ROOT_DOMAIN = os.getenv(
    "MONITOR_SPA_ROOT_DOMAIN",
    "bid.gazprom-neft.ru",
)

# Аналог DEFAULT_COOKIE_AGE_SECONDS на фронте («бесконечная жизнь» через max-age).
SPA_USER_ID_COOKIE_MAX_AGE_SEC = int(
    os.getenv("SPA_USER_ID_COOKIE_MAX_AGE_SEC", str(365 * 24 * 60 * 60))
)


def _shared_cookie_js(uid: str, cookie_key: str, root_domain: str, max_age: int) -> str:
    """JS как setSharedCookie + localStorage gpnSpaUid (без randomUUID)."""
    return (
        "(function () {\n"
        f"  var uid = {uid!r};\n"
        f"  var cookieKey = {cookie_key!r};\n"
        f"  var rootDomain = {root_domain!r};\n"
        f"  var maxAge = {int(max_age)};\n"
        f"  try {{ localStorage.setItem({GPN_SPA_LOCALSTORAGE_KEY!r}, uid); }} catch (e) {{}}\n"
        "  try {\n"
        "    var s = cookieKey + '=' + uid\n"
        "      + '; max-age=' + maxAge\n"
        "      + '; path=/; SameSite=Lax'\n"
        "      + (rootDomain ? ('; domain=' + rootDomain) : '');\n"
        "    if (location.protocol === 'https:') s += '; Secure';\n"
        "    document.cookie = s;\n"
        "  } catch (e) {}\n"
        "})();"
    )


def _set_spa_uid_cookies_cdp(driver: webdriver.Chrome, uid: str) -> None:
    """CDP Network.setCookie на root_domain до навигации (как setSharedCookie)."""
    cookie_key = SPA_USER_ID_COOKIE_KEY.strip() or "spa_user_id"
    root = MONITOR_SPA_ROOT_DOMAIN.strip().lstrip(".")
    expires = time.time() + SPA_USER_ID_COOKIE_MAX_AGE_SEC
    try:
        driver.execute_cdp_cmd("Network.enable", {})
        # Domain cookie: bid.gazprom-neft.ru + id.bid.* + lk.bid.*
        driver.execute_cdp_cmd(
            "Network.setCookie",
            {
                "name": cookie_key,
                "value": uid,
                "domain": root,
                "path": "/",
                "secure": True,
                "httpOnly": False,
                "sameSite": "Lax",
                "expires": expires,
            },
        )
    except Exception as exc:
        print(f"[chrome] WARN: CDP setCookie SPA uid: {exc}", flush=True)


def _inject_gpn_spa_analytics_uid(driver: webdriver.Chrome) -> None:
    """Фиксированный MONITOR_ANALYTICS_UID на все SPA-неймспейсы.

    Фронт: getOrCreateCustomUserId читает cookie SPA_USER_ID_KEY и пишет
    shared cookie на root_domain. Мониторинг НЕ генерирует randomUUID —
    всегда хардкодный uid + cookie (CDP до навигации) + localStorage
    (Page.addScriptToEvaluateOnNewDocument) для совместимости с counter.js.
    """
    uid = MONITOR_ANALYTICS_UID.strip()
    if not uid:
        return

    _set_spa_uid_cookies_cdp(driver, uid)

    script = _shared_cookie_js(
        uid,
        SPA_USER_ID_COOKIE_KEY.strip() or "spa_user_id",
        MONITOR_SPA_ROOT_DOMAIN.strip().lstrip("."),
        SPA_USER_ID_COOKIE_MAX_AGE_SEC,
    )
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": script},
        )
    except Exception as exc:
        print(f"[chrome] WARN: не удалось задать SPA uid script: {exc}", flush=True)


def create_chrome_driver(*, headless: bool | None = None) -> webdriver.Chrome:
    use_headless = MONITOR_HEADLESS if headless is None else headless
    # На Mac headless=new часто падает на кликах — для локальных тестов лучше окно.
    if sys.platform == "darwin" and use_headless and os.getenv("MONITOR_FORCE_HEADLESS") != "true":
        use_headless = False

    options = _build_chrome_options(use_headless)
    retries = int(os.getenv("CHROME_START_RETRIES", "3"))
    delay = float(os.getenv("CHROME_START_RETRY_DELAY_SEC", "3"))
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            chromedriver_path = _resolve_chromedriver_path()
            service = Service(executable_path=chromedriver_path) if chromedriver_path else Service()
            driver = webdriver.Chrome(service=service, options=options)
            _inject_gpn_spa_analytics_uid(driver)
            driver.set_page_load_timeout(LK_PAGE_LOAD_TIMEOUT)
            driver.implicitly_wait(LK_IMPLICIT_WAIT)
            if not use_headless:
                driver.maximize_window()
            return driver
        except Exception as exc:
            last_error = exc
            if attempt >= retries:
                break
            print(
                f"[chrome] старт WebDriver не удался ({attempt}/{retries}): {exc}; "
                f"повтор через {delay:.0f} с",
                flush=True,
            )
            time.sleep(delay)

    assert last_error is not None
    raise last_error


def _build_chrome_options(use_headless: bool) -> Options:
    options = Options()
    if use_headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--no-first-run")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument(
        "--disable-features=PasswordManager,PasswordCheck,PasswordLeakDetection,"
        "AutofillServerCommunication,TranslateUI"
    )
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    })
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    options.add_experimental_option("useAutomationExtension", False)
    options.page_load_strategy = os.getenv("LK_PAGE_LOAD_STRATEGY", "eager")

    chrome_binary = _resolve_chrome_binary()
    if chrome_binary:
        options.binary_location = chrome_binary
    return options
