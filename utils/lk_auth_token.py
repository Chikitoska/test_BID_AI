"""Извлечение auth для BE-smoke ЛК после FE-логина (Keycloak + TOTP).

Ищем Bearer JWT в cookie / localStorage / sessionStorage; cookies Selenium
копируем в requests.Session (часто достаточно для same-site /api).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import requests
from selenium.webdriver.remote.webdriver import WebDriver

_JWT_RE = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")
_TOKEN_KEY_HINTS = (
    "access_token",
    "accessToken",
    "id_token",
    "idToken",
    "authToken",
    "authorization",
    "kc-access",
    "token",
)

_EXTRACT_JS = r"""
return (function () {
  const jwtRe = /eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/;
  const keyHints = [
    "access_token", "accessToken", "id_token", "idToken",
    "authToken", "authorization", "kc-access", "token"
  ];
  const out = { bearer: null, source: null, keys: [] };

  function consider(key, value, source) {
    if (value == null) return;
    const text = String(value);
    out.keys.push(source + ":" + key);
    const keyL = String(key).toLowerCase();
    const hintHit = keyHints.some(h => keyL.includes(h.toLowerCase()));
    let token = null;
    if (hintHit && jwtRe.test(text)) {
      const m = text.match(jwtRe);
      token = m ? m[0] : null;
    }
    if (!token && text.trim().startsWith("{")) {
      try {
        const obj = JSON.parse(text);
        for (const k of Object.keys(obj || {})) {
          const kl = k.toLowerCase();
          if (keyHints.some(h => kl.includes(h.toLowerCase()))) {
            const v = obj[k];
            if (typeof v === "string" && jwtRe.test(v)) {
              token = v.match(jwtRe)[0];
              break;
            }
          }
        }
        if (!token && typeof obj.access_token === "string" && jwtRe.test(obj.access_token)) {
          token = obj.access_token.match(jwtRe)[0];
        }
      } catch (e) {}
    }
    if (!token && hintHit && text.length > 20 && text.indexOf(".") > 0 && !text.includes(" ")) {
      // opaque bearer (non-JWT)
      token = text.replace(/^Bearer\s+/i, "").trim();
    }
    if (token && !out.bearer) {
      out.bearer = token;
      out.source = source + ":" + key;
    }
  }

  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      consider(k, localStorage.getItem(k), "localStorage");
    }
  } catch (e) {}
  try {
    for (let i = 0; i < sessionStorage.length; i++) {
      const k = sessionStorage.key(i);
      consider(k, sessionStorage.getItem(k), "sessionStorage");
    }
  } catch (e) {}

  return out;
})();
"""


@dataclass
class LkAuthMaterial:
    bearer: str | None = None
    bearer_source: str | None = None
    cookies: list[dict[str, Any]] = field(default_factory=list)
    storage_keys: list[str] = field(default_factory=list)

    @property
    def has_auth(self) -> bool:
        return bool(self.bearer) or bool(self.cookies)


def _cookie_bearer(cookies: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    for cookie in cookies:
        name = str(cookie.get("name") or "")
        value = str(cookie.get("value") or "")
        name_l = name.lower()
        if any(h in name_l for h in _TOKEN_KEY_HINTS):
            match = _JWT_RE.search(value)
            if match:
                return match.group(0), f"cookie:{name}"
            if value and len(value) > 20:
                return value.replace("Bearer ", "").strip(), f"cookie:{name}"
        match = _JWT_RE.search(value)
        if match and "token" in name_l:
            return match.group(0), f"cookie:{name}"
    return None, None


def extract_lk_auth(driver: WebDriver) -> LkAuthMaterial:
    """Собрать Bearer + cookies с текущей вкладки ЛК."""
    cookies = list(driver.get_cookies() or [])
    storage: dict[str, Any] = {"bearer": None, "source": None, "keys": []}
    try:
        raw = driver.execute_script(_EXTRACT_JS)
        if isinstance(raw, dict):
            storage = raw
    except Exception as exc:  # noqa: BLE001 — диагностика, не роняем suite
        print(f"[lk_be] storage scan failed: {exc}", flush=True)

    bearer = storage.get("bearer") if isinstance(storage.get("bearer"), str) else None
    source = storage.get("source") if isinstance(storage.get("source"), str) else None
    keys = storage.get("keys") if isinstance(storage.get("keys"), list) else []

    if not bearer:
        cookie_token, cookie_source = _cookie_bearer(cookies)
        bearer, source = cookie_token, cookie_source

    material = LkAuthMaterial(
        bearer=bearer,
        bearer_source=source,
        cookies=cookies,
        storage_keys=[str(k) for k in keys],
    )
    print(
        f"[lk_be] auth: bearer={'yes' if bearer else 'no'}"
        f" source={source!r} cookies={len(cookies)} storage_keys={len(keys)}",
        flush=True,
    )
    return material


def apply_lk_auth(session: requests.Session, material: LkAuthMaterial) -> None:
    """Настроить requests.Session: cookies + optional Authorization Bearer."""
    session.cookies.clear()
    for cookie in material.cookies:
        name = cookie.get("name")
        value = cookie.get("value")
        if not name or value is None:
            continue
        domain = (cookie.get("domain") or "").lstrip(".")
        path = cookie.get("path") or "/"
        # requests cookie jar: omit leading-dot issues by setting per host later
        try:
            session.cookies.set(name, value, domain=domain or None, path=path)
        except Exception:
            session.cookies.set(str(name), str(value))

    session.headers.pop("Authorization", None)
    if material.bearer:
        session.headers["Authorization"] = f"Bearer {material.bearer}"


def cookies_for_url(material: LkAuthMaterial, url: str) -> dict[str, str]:
    """Подмножество cookies, подходящих под host URL (на случай jar quirks)."""
    host = urlparse(url).hostname or ""
    out: dict[str, str] = {}
    for cookie in material.cookies:
        name = cookie.get("name")
        value = cookie.get("value")
        if not name or value is None:
            continue
        domain = (cookie.get("domain") or "").lstrip(".")
        if domain and host.endswith(domain):
            out[str(name)] = str(value)
        elif not domain:
            out[str(name)] = str(value)
    return out


def dump_auth_debug(material: LkAuthMaterial) -> str:
    """Короткий debug без значений секретов."""
    cookie_names = [str(c.get("name")) for c in material.cookies]
    return json.dumps(
        {
            "bearer": bool(material.bearer),
            "bearer_source": material.bearer_source,
            "cookie_names": cookie_names,
            "storage_keys": material.storage_keys[:40],
        },
        ensure_ascii=False,
    )
