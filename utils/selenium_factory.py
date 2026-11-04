"""Фабрика Chrome WebDriver для мониторинга и тестов ЛК."""

from __future__ import annotations

import atexit
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager

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
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
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

# Snap Chromium: реальный профиль в snap-private-tmp, /tmp/<name> часто 4KB-заглушка.
SNAP_CHROMIUM_PRIVATE_TMP = "/tmp/snap-private-tmp/snap.chromium/tmp"

# Ниже этого Chrome не стартуем: 15Г VPS, Influx WAL падает раньше Allure.
CHROME_MIN_FREE_MB_DEFAULT = 500

_LIVE_USER_DATA_DIRS: set[str] = set()
_ATEXIT_REGISTERED = False
_PREV_SIGTERM = None


class ChromeDiskFullError(RuntimeError):
    """Avail < CHROME_MIN_FREE_MB — не стартуем Chrome, чтобы не убить Influx WAL."""


def user_data_dir_from_options(options) -> str:
    """--user-data-dir этого запуска (уникальный temp)."""
    args = getattr(options, "arguments", None) or []
    for arg in args:
        if isinstance(arg, str) and arg.startswith("--user-data-dir="):
            return arg.split("=", 1)[1].strip()
    return ""


def _pids_for_user_data_dir(user_data_dir: str) -> list[int]:
    """Только chrome/chromedriver с ЭТИМ user-data-dir — чужой Chrome на Mac не трогаем."""
    marker = (user_data_dir or "").strip()
    if len(marker) < 12:
        return []
    try:
        proc = subprocess.run(
            ["ps", "-ax", "-o", "pid=,command="],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    pids: list[int] = []
    for line in (proc.stdout or "").splitlines():
        raw = line.strip()
        if marker not in raw:
            continue
        low = raw.lower()
        if not any(token in low for token in ("chromedriver", "google chrome", "chromium", "/chrome")):
            continue
        try:
            pid = int(raw.split(None, 1)[0])
        except (ValueError, IndexError):
            continue
        if pid > 0 and pid != os.getpid():
            pids.append(pid)
    return pids


def kill_orphans_for_user_data_dir(user_data_dir: str) -> int:
    """Убить висящие chrome/chromedriver только этого профиля (после SessionNotCreated)."""
    pids = _pids_for_user_data_dir(user_data_dir)
    killed = 0
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            killed += 1
        except OSError:
            continue
    if killed:
        time.sleep(0.25)
        for pid in _pids_for_user_data_dir(user_data_dir):
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                continue
    if killed:
        print(
            f"[chrome] сняли {killed} процесс(ов) для user-data-dir={user_data_dir}",
            flush=True,
        )
    return killed


def _bid_chrome_profile_name(user_data_dir: str) -> str:
    """Имя temp-профиля этого запуска (bid-chrome-*); чужие каталоги не трогаем."""
    name = os.path.basename(os.path.normpath(user_data_dir or ""))
    if not name.startswith("bid-chrome-") or name in (".", ".."):
        return ""
    return name


def snap_private_twin_dir(user_data_dir: str) -> str:
    """/tmp/snap-private-tmp/snap.chromium/tmp/<basename> — только этот профиль."""
    name = _bid_chrome_profile_name(user_data_dir)
    if not name:
        return ""
    return os.path.join(SNAP_CHROMIUM_PRIVATE_TMP, name)


def chrome_min_free_bytes() -> int:
    try:
        mb = int(os.getenv("CHROME_MIN_FREE_MB", str(CHROME_MIN_FREE_MB_DEFAULT)))
    except ValueError:
        mb = CHROME_MIN_FREE_MB_DEFAULT
    return max(0, mb) * 1024 * 1024


def disk_free_bytes(path: str = "/") -> int:
    try:
        return int(shutil.disk_usage(path).free)
    except OSError:
        return 0


def assert_disk_for_chrome(*, path: str = "/") -> None:
    """Hard preflight: нет 500 МБ — Chrome/Allure не пишем, Influx WAL важнее."""
    free = disk_free_bytes(path)
    need = chrome_min_free_bytes()
    if free < need:
        free_mb = free / (1024 * 1024)
        need_mb = need / (1024 * 1024)
        raise ChromeDiskFullError(
            f"ENOSPC: Avail={free_mb:.0f}MB < {need_mb:.0f}MB — Chrome not launched "
            f"(no space left on device)"
        )


def _bid_chrome_search_roots() -> list[str]:
    roots: list[str] = []
    for item in (SNAP_CHROMIUM_PRIVATE_TMP, "/tmp", tempfile.gettempdir()):
        if item and item not in roots:
            roots.append(item)
    return roots


def _user_data_dirs_from_running_chrome() -> list[str]:
    """--user-data-dir живого chrome/chromedriver (health vs combat)."""
    try:
        proc = subprocess.run(
            ["ps", "-ax", "-o", "pid=,command="],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    found: list[str] = []
    for line in (proc.stdout or "").splitlines():
        low = line.lower()
        if not any(
            token in low for token in ("chromedriver", "google chrome", "chromium", "/chrome")
        ):
            continue
        for part in line.split():
            if part.startswith("--user-data-dir="):
                path = part.split("=", 1)[1].strip()
                if _bid_chrome_profile_name(path):
                    found.append(path)
    return found


def live_bid_chrome_names() -> set[str]:
    """Имена профилей, которые сейчас locked/живые — sweep их не трогает."""
    names: set[str] = set()
    for path in list(_LIVE_USER_DATA_DIRS) + _user_data_dirs_from_running_chrome():
        name = _bid_chrome_profile_name(path)
        if name:
            names.add(name)
    return names


def sweep_stale_bid_chrome_profiles() -> int:
    """Удалить leftover bid-chrome-* в /tmp и snap-private, кроме живого профиля.

    SIGTERM/cron убивает Chrome без rmtree — каталоги остаются и забивают 15Г.
    """
    live = live_bid_chrome_names()
    removed = 0
    for root in _bid_chrome_search_roots():
        try:
            entries = os.listdir(root)
        except OSError:
            continue
        for name in entries:
            if not name.startswith("bid-chrome-") or name in (".", ".."):
                continue
            if name in live:
                continue
            path = os.path.join(root, name)
            try:
                if not os.path.isdir(path):
                    continue
            except OSError:
                continue
            shutil.rmtree(path, ignore_errors=True)
            removed += 1
    if removed:
        print(f"[chrome] sweep stale bid-chrome profiles: {removed}", flush=True)
    return removed


def _register_live_user_data_dir(path: str) -> None:
    normalized = os.path.normpath(path or "")
    if normalized:
        _LIVE_USER_DATA_DIRS.add(normalized)
    install_chrome_crash_cleanup()


def _cleanup_live_profiles() -> None:
    for path in list(_LIVE_USER_DATA_DIRS):
        try:
            kill_orphans_for_user_data_dir(path)
        except Exception:
            pass
        remove_chrome_user_data_dir(path)


def _atexit_chrome_cleanup() -> None:
    _cleanup_live_profiles()


def _sigterm_chrome_cleanup(signum, frame) -> None:
    """Слот health 220с шлёт TERM — профиль надо снести до SIGKILL+15с."""
    _cleanup_live_profiles()
    prev = _PREV_SIGTERM
    if callable(prev) and prev is not _sigterm_chrome_cleanup:
        prev(signum, frame)
    elif prev in (None, signal.SIG_DFL) and hasattr(signal, "SIGTERM"):
        try:
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)
        except OSError:
            pass


def install_chrome_crash_cleanup() -> None:
    """atexit + SIGTERM: удалить live bid-chrome-* даже без quit_chrome_driver."""
    global _ATEXIT_REGISTERED, _PREV_SIGTERM
    if not _ATEXIT_REGISTERED:
        atexit.register(_atexit_chrome_cleanup)
        _ATEXIT_REGISTERED = True
    if not hasattr(signal, "SIGTERM"):
        return
    try:
        current = signal.getsignal(signal.SIGTERM)
    except (ValueError, OSError):
        return
    if current is _sigterm_chrome_cleanup:
        return
    _PREV_SIGTERM = current
    try:
        signal.signal(signal.SIGTERM, _sigterm_chrome_cleanup)
    except (ValueError, OSError):
        pass


@contextmanager
def chrome_profile_lifecycle():
    """Sweep leftover в начале и в конце health/daily/combat."""
    sweep_stale_bid_chrome_profiles()
    install_chrome_crash_cleanup()
    try:
        yield
    finally:
        sweep_stale_bid_chrome_profiles()


def remove_chrome_user_data_dir(user_data_dir: str) -> None:
    """Удалить temp-профиль этого запуска и snap-private близнеца, если есть."""
    name = _bid_chrome_profile_name(user_data_dir)
    if not name:
        return
    shutil.rmtree(user_data_dir, ignore_errors=True)
    twin = snap_private_twin_dir(user_data_dir)
    if twin:
        shutil.rmtree(twin, ignore_errors=True)
    _LIVE_USER_DATA_DIRS.discard(os.path.normpath(user_data_dir))


def quit_chrome_driver(driver) -> None:
    """quit, сироты этого профиля, затем rmtree user-data-dir и snap-private twin."""
    user_dir = getattr(driver, "_bid_user_data_dir", "") or ""
    if not user_dir:
        try:
            caps = getattr(driver, "capabilities", None) or {}
            chrome_opts = caps.get("goog:chromeOptions") or caps.get("chromeOptions") or {}
            args = chrome_opts.get("args") or []
            for arg in args:
                if isinstance(arg, str) and arg.startswith("--user-data-dir="):
                    user_dir = arg.split("=", 1)[1].strip()
                    break
        except Exception:
            user_dir = ""
    try:
        driver.quit()
    except Exception:
        pass
    finally:
        if user_dir:
            kill_orphans_for_user_data_dir(user_dir)
            remove_chrome_user_data_dir(user_dir)


def _alloc_user_data_dir() -> str:
    """Свой профиль на каждый старт: иначе второй Chrome в combat pytest падает.

    Общий CHROME_USER_DATA_DIR не переиспользуем — SingletonLock / «already in use».
    Профиль обычного Chrome/Chromium, не Chromium-GOST.
    """
    explicit = os.getenv("CHROME_USER_DATA_DIR", "").strip()
    if explicit and os.getenv("CHROME_REUSE_USER_DATA_DIR", "").lower() in (
        "1",
        "true",
        "yes",
    ):
        return explicit
    parent = explicit if explicit and os.path.isdir(explicit) else None
    path = tempfile.mkdtemp(prefix="bid-chrome-", dir=parent)
    _register_live_user_data_dir(path)
    return path


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


def _is_gost_chrome_path(path: str) -> bool:
    """Chromium-GOST больше не используем в мониторе и автотестах."""
    low = (path or "").lower()
    return "chromium-gost" in low or "chrome-gost" in low or "/gost/" in low


def _resolve_chrome_binary() -> str:
    explicit = os.getenv("CHROME_BINARY", "").strip()
    if explicit:
        if _is_gost_chrome_path(explicit):
            print(
                f"[chrome] CHROME_BINARY={explicit} — Chromium-GOST игнорируем, "
                "берём обычный Chrome/Chromium",
                flush=True,
            )
        elif os.path.isfile(explicit) and os.access(explicit, os.X_OK):
            return explicit
    for path in _CHROME_CANDIDATES:
        if _is_gost_chrome_path(path):
            continue
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

# localStorage-ключ counter.js (spa-back) — опционально, не источник истины.
GPN_SPA_LOCALSTORAGE_KEY = "gpnSpaUid"

# Имя cookie фронта (SPA_USER_ID_KEY) — источник истины для сквозного UUID.
SPA_USER_ID_COOKIE_KEY = os.getenv(
    "SPA_USER_ID_COOKIE_KEY",
    "gpn_spa_custom_user_id_cookie",
)

# root_domain из конфига лендинга: общий для bid / id.bid / lk.bid.
# Cookie Domain=bid.gazprom-neft.ru покрывает все три неймспейса.
MONITOR_SPA_ROOT_DOMAIN = os.getenv(
    "MONITOR_SPA_ROOT_DOMAIN",
    "bid.gazprom-neft.ru",
)

# Аналог DEFAULT_COOKIE_AGE_SECONDS на фронте («бесконечная жизнь» через max-age).
# Число DEFAULT_COOKIE_AGE_SECONDS фронт не назвал — держим 365d; сверить, когда дадут.
SPA_USER_ID_COOKIE_MAX_AGE_SEC = int(
    os.getenv("SPA_USER_ID_COOKIE_MAX_AGE_SEC", str(365 * 24 * 60 * 60))
)


def _shared_cookie_js(uid: str, cookie_key: str, root_domain: str, max_age: int) -> str:
    """JS как setSharedCookie; localStorage gpnSpaUid — опционально (не SoT)."""
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
    cookie_key = SPA_USER_ID_COOKIE_KEY.strip() or "gpn_spa_custom_user_id_cookie"
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


def _inject_events_uid_rewrite(driver: webdriver.Chrome, uid: str) -> None:
    """Патч fetch/XHR/sendBeacon: uid в POST /events = MONITOR_ANALYTICS_UID."""
    from utils.spa_analytics import events_uid_rewrite_js

    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": events_uid_rewrite_js(uid)},
        )
    except Exception as exc:
        print(f"[chrome] WARN: SPA events uid rewrite: {exc}", flush=True)


def _inject_gpn_spa_analytics_uid(driver: webdriver.Chrome) -> None:
    """Фиксированный MONITOR_ANALYTICS_UID на все SPA-неймспейсы.

    Фронт: getOrCreateCustomUserId читает cookie SPA_USER_ID_KEY
    (gpn_spa_custom_user_id_cookie) и пишет shared cookie на root_domain.
    Мониторинг НЕ генерирует randomUUID — всегда хардкодный uid + cookie
    (CDP до навигации). localStorage gpnSpaUid пишется опционально
    (совместимость с counter.js), источником истины не является.
    Fetch/XHR/sendBeacon на spa-back/events дополнительно штампуют тот же uid
    в теле (в т.ч. customparams.as_user_id) — Consta-виджет иначе шлёт random UUID.
    """
    from utils.spa_analytics import spa_events_uid

    uid = spa_events_uid() or MONITOR_ANALYTICS_UID.strip()
    if not uid:
        return

    _set_spa_uid_cookies_cdp(driver, uid)

    script = _shared_cookie_js(
        uid,
        SPA_USER_ID_COOKIE_KEY.strip() or "gpn_spa_custom_user_id_cookie",
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

    _inject_events_uid_rewrite(driver, uid)


def create_chrome_driver(
    *,
    headless: bool | None = None,
    enable_performance_log: bool = False,
) -> webdriver.Chrome:
    use_headless = MONITOR_HEADLESS if headless is None else headless
    # На Mac headless=new часто падает на кликах — для локальных тестов лучше окно.
    if sys.platform == "darwin" and use_headless and os.getenv("MONITOR_FORCE_HEADLESS") != "true":
        use_headless = False

    sweep_stale_bid_chrome_profiles()
    assert_disk_for_chrome()
    install_chrome_crash_cleanup()

    retries = int(os.getenv("CHROME_START_RETRIES", "3"))
    delay = float(os.getenv("CHROME_START_RETRY_DELAY_SEC", "3"))
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        options = _build_chrome_options(use_headless)
        user_dir = user_data_dir_from_options(options)
        if enable_performance_log:
            from utils.spa_events_sniffer import enable_performance_log as _enable_perf

            _enable_perf(options)
        try:
            chromedriver_path = _resolve_chromedriver_path()
            service = Service(executable_path=chromedriver_path) if chromedriver_path else Service()
            driver = webdriver.Chrome(service=service, options=options)
            driver._bid_user_data_dir = user_dir
            _inject_gpn_spa_analytics_uid(driver)
            if enable_performance_log:
                try:
                    driver.execute_cdp_cmd("Network.enable", {})
                except Exception as exc:
                    print(f"[chrome] WARN: Network.enable: {exc}", flush=True)
            driver.set_page_load_timeout(LK_PAGE_LOAD_TIMEOUT)
            driver.implicitly_wait(LK_IMPLICIT_WAIT)
            if not use_headless:
                driver.maximize_window()
            return driver
        except Exception as exc:
            last_error = exc
            if user_dir:
                kill_orphans_for_user_data_dir(user_dir)
                remove_chrome_user_data_dir(user_dir)
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
    options.add_argument(f"--user-data-dir={_alloc_user_data_dir()}")
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
