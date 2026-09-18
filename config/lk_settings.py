"""Настройки авторизации и ЛК BID (только из env, без секретов в коде)."""

import os

LANDING_BASE_URL = os.getenv("BID_LANDING_URL", "https://bid.gazprom-neft.ru/")

BID_USERNAME = os.getenv("BID_USERNAME", "")
BID_PASSWORD = os.getenv("BID_PASSWORD", "")
BID_TOTP_SECRET = os.getenv("BID_TOTP_SECRET", "")

BID_LK_EXPECTED_URL = os.getenv(
    "BID_LK_EXPECTED_URL",
    "https://lk.bid.gazprom-neft.ru/service-providers",
)
BID_EXPECTED_COMPANY = os.getenv("BID_EXPECTED_COMPANY", "")
BID_EXPECTED_FIO = os.getenv("BID_EXPECTED_FIO", "")
BID_PROCESSOR_URL = os.getenv("BID_PROCESSOR_URL", "https://processor.gazprom-neft.ru/")

MONITOR_RUN_LK = os.getenv("MONITOR_RUN_LK", "false").lower() in ("1", "true", "yes")
MONITOR_HEADLESS = os.getenv("MONITOR_HEADLESS", "true").lower() in ("1", "true", "yes")
LK_AUTH_WAIT_SEC = int(os.getenv("LK_AUTH_WAIT_SEC", "12"))
LK_LOGIN_WAIT_SEC = int(os.getenv("LK_LOGIN_WAIT_SEC", "30"))
LK_UI_WAIT_SEC = int(os.getenv("LK_UI_WAIT_SEC", os.getenv("LK_LOGIN_WAIT_SEC", "45")))
# Мягкие повторы чтения ФИО/компании в шапке Processor (флаки ночных SPA).
LK_PROCESSOR_HEADER_ATTEMPTS = int(os.getenv("LK_PROCESSOR_HEADER_ATTEMPTS", "2"))
LK_PROCESSOR_HEADER_RETRY_DELAY_SEC = float(
    os.getenv("LK_PROCESSOR_HEADER_RETRY_DELAY_SEC", "3")
)
LK_SKIP_LANDING = os.getenv("LK_SKIP_LANDING", "false").lower() in ("1", "true", "yes")

LK_CREDENTIALS_SET = bool(BID_USERNAME and BID_PASSWORD and BID_TOTP_SECRET)
LK_MONITOR_ENABLED = MONITOR_RUN_LK and LK_CREDENTIALS_SET
