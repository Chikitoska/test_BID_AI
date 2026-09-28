#!/usr/bin/env python3
"""HTTP endpoint: выгрузка bid_failure → XLSX с HTTP Basic Auth.

GET /export/errors.xlsx?from=${__from}&to=${__to}

Параметры from/to — как в Grafana dashboard/data links (обычно epoch ms).
Логин/пароль: EXPORT_BASIC_USER / EXPORT_BASIC_PASSWORD (не коммитить).
"""

from __future__ import annotations

import base64
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from monitor.export_errors_xlsx import (  # noqa: E402
    build_xlsx_bytes,
    fetch_failure_rows,
    resolve_time_range,
)

EXPORT_BASIC_USER = os.getenv("EXPORT_BASIC_USER", "").strip()
EXPORT_BASIC_PASSWORD = os.getenv("EXPORT_BASIC_PASSWORD", "").strip()
EXPORT_BIND = os.getenv("EXPORT_BIND", "127.0.0.1").strip() or "127.0.0.1"
EXPORT_PORT = int(os.getenv("EXPORT_PORT", "8765"))


def _auth_configured() -> bool:
    return bool(EXPORT_BASIC_USER and EXPORT_BASIC_PASSWORD)


def _check_basic_auth(header: str | None) -> bool:
    if not _auth_configured():
        return False
    if not header or not header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(header[6:].strip()).decode("utf-8")
    except Exception:
        return False
    user, sep, password = decoded.partition(":")
    if not sep:
        return False
    return user == EXPORT_BASIC_USER and password == EXPORT_BASIC_PASSWORD


class ExportHandler(BaseHTTPRequestHandler):
    server_version = "BIDExport/1.0"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path in ("/health", "/healthz"):
            self._send(200, b"ok\n", content_type="text/plain; charset=utf-8")
            return

        if path not in ("/export/errors.xlsx", "/export/errors"):
            self._send(404, b"not found\n", content_type="text/plain; charset=utf-8")
            return

        if not _auth_configured():
            self._send(
                503,
                b"EXPORT_BASIC_USER / EXPORT_BASIC_PASSWORD not configured\n",
                content_type="text/plain; charset=utf-8",
            )
            return

        if not _check_basic_auth(self.headers.get("Authorization")):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="BID errors export"')
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"unauthorized\n")
            return

        qs = parse_qs(parsed.query)
        from_raw = (qs.get("from") or [None])[0]
        to_raw = (qs.get("to") or [None])[0]
        try:
            start, stop = resolve_time_range(from_raw, to_raw)
            rows = fetch_failure_rows(start=start, stop=stop)
            payload = build_xlsx_bytes(rows)
        except Exception as exc:
            msg = f"export failed: {exc}\n".encode("utf-8")
            self._send(500, msg, content_type="text/plain; charset=utf-8")
            return

        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"bid_errors_{stamp}.xlsx"
        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send(self, code: int, body: bytes, *, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    if not _auth_configured():
        print(
            "WARN: задайте EXPORT_BASIC_USER и EXPORT_BASIC_PASSWORD "
            "(иначе /export/* вернёт 503)",
            file=sys.stderr,
        )
    server = ThreadingHTTPServer((EXPORT_BIND, EXPORT_PORT), ExportHandler)
    print(
        f"BID errors XLSX export on http://{EXPORT_BIND}:{EXPORT_PORT}/export/errors.xlsx"
    )
    print("Grafana link: .../export/errors.xlsx?from=${__from}&to=${__to}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
