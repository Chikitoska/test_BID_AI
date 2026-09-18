"""TOTP SHA-256 (Keycloak BID) — 6-значный код из секрета."""

from __future__ import annotations

import base64
import hashlib
import hmac
import struct
import time


def generate_totp_sha256(secret: str, *, interval: int = 30, digits: int = 6) -> str:
    normalized = secret.replace(" ", "").upper()
    padding = len(normalized) % 8
    if padding:
        normalized += "=" * (8 - padding)
    key = base64.b32decode(normalized)
    msg = struct.pack(">Q", int(time.time()) // interval)
    hash_val = hmac.new(key, msg, hashlib.sha256).digest()
    offset = hash_val[-1] & 0x0F
    binary = struct.unpack(">I", hash_val[offset : offset + 4])[0] & 0x7FFFFFFF
    otp = binary % (10**digits)
    return f"{otp:0{digits}d}"
