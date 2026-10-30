"""Живой BID: в мониторе не skip, локально без сети — skip."""

from __future__ import annotations

import os
import socket

import pytest

BID_HOST = "bid.gazprom-neft.ru"


def bid_tcp_ok(timeout: float = 8) -> bool:
    try:
        with socket.create_connection((BID_HOST, 443), timeout=timeout):
            return True
    except OSError:
        return False


def require_live_bid() -> None:
    if bid_tcp_ok():
        return
    message = f"{BID_HOST}:443 недоступен с этой машины"
    if os.getenv("MONITOR_REQUIRE_LIVE", "").lower() in ("1", "true", "yes"):
        pytest.fail(f"{message} — монитор не пропускает живой шаг")
    pytest.skip(f"{message} — живой прогон лендинга пропущен")
