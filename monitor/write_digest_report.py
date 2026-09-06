#!/usr/bin/env python3
"""Собрать digest мониторинга за N часов → monitor/reports/latest.md (+ опционально push в GitHub)."""

from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from monitor.load_env import load_project_env

load_project_env(PROJECT_ROOT)

from monitor.config import (  # noqa: E402
    GITHUB_PAT,
    GITHUB_REPO,
    INFLUXDB_BUCKET,
    INFLUXDB_ORG,
    INFLUXDB_TOKEN,
    INFLUXDB_URL,
)

REPORT_PATH = PROJECT_ROOT / "monitor" / "reports" / "latest.md"
MSK = timezone(timedelta(hours=3))

RUN_NAMES = {
    "health": "Лендинг + мин ЛК (5 мин)",
    "full": "Лендинг + API autotests",
    "lk_pytest": "Боевой прогон ЛК (2 ч)",
    "probe": "HTTP probe (legacy)",
}


def _tail_grep(path: Path, pattern: str, *, limit: int = 30) -> list[str]:
    if not path.is_file():
        return [f"(нет файла {path.name})"]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"(не прочитан {path.name}: {exc})"]
    rx = re.compile(pattern, re.I)
    matched = [line.rstrip() for line in text.splitlines() if rx.search(line)]
    if not matched:
        return ["(совпадений нет)"]
    return matched[-limit:]


def _influx_failures(hours: int) -> list[str]:
    if not INFLUXDB_TOKEN:
        return ["INFLUXDB_TOKEN не задан"]
    try:
        from influxdb_client import InfluxDBClient
    except ImportError:
        return ["influxdb_client не установлен"]

    start = datetime.now(timezone.utc) - timedelta(hours=hours)
    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: {start.isoformat()})
  |> filter(fn: (r) => r._measurement == "bid_failure" and r._field == "error")
  |> sort(columns: ["_time"], desc: true)
  |> limit(n: 40)
'''
    lines: list[str] = []
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        for table in client.query_api().query(flux):
            for record in table.records:
                rt = record.values.get("run_type", "?")
                check = record.values.get("check", "")
                label = record.values.get("label", "")
                err = str(record.get_value() or "").replace("\n", " ")[:400]
                lines.append(
                    f"- `{record.get_time()}` | {RUN_NAMES.get(rt, rt)} | "
                    f"`{check}` | {label} | {err}"
                )
    return lines or ["(ошибок bid_failure за период нет)"]


def _influx_counts(hours: int) -> list[str]:
    if not INFLUXDB_TOKEN:
        return ["INFLUXDB_TOKEN не задан"]
    try:
        from influxdb_client import InfluxDBClient
    except ImportError:
        return ["influxdb_client не установлен"]

    days = max(1, (hours + 23) // 24)
    flux = f'''
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -{days}d)
  |> filter(fn: (r) =>
      r._measurement == "bid_lk_run" or
      r._measurement == "bid_run" or
      r._measurement == "bid_lk_pytest" or
      r._measurement == "bid_failure"
  )
  |> group(columns: ["_measurement"])
  |> count()
'''
    lines: list[str] = []
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        for table in client.query_api().query(flux, org=INFLUXDB_ORG):
            for record in table.records:
                m = record.values.get("_measurement", "?")
                n = record.values.get("_value", 0)
                lines.append(f"- `{m}`: {n} точек (~{days}д)")
    return lines or ["(пусто)"]


def _git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(PROJECT_ROOT), "log", "-1", "--oneline"],
            text=True,
            timeout=10,
        ).strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "(git log недоступен)"


def build_report(hours: int) -> str:
    now = datetime.now(MSK)
    lines = [
        f"# BID monitor digest",
        "",
        f"- Generated: `{now.isoformat()}` (Europe/Moscow)",
        f"- Window: last **{hours}** hours",
        f"- Host: VPS `/opt/test_BID_AI`",
        f"- Git HEAD: `{_git_head()}`",
        "",
        "## Influx volume",
        "",
        *_influx_counts(hours),
        "",
        "## Failures (bid_failure)",
        "",
        *_influx_failures(hours),
        "",
        "## health.log (FAIL/ERROR/WARN/ImportError)",
        "",
        "```",
        *_tail_grep(PROJECT_ROOT / "monitor" / "health.log", r"FAIL|ERROR|WARN|ImportError"),
        "```",
        "",
        "## lk-pytest.log (FAIL/ERROR/ImportError|failed=)",
        "",
        "```",
        *_tail_grep(
            PROJECT_ROOT / "monitor" / "lk-pytest.log",
            r"FAIL|ERROR|ImportError|failed=|LK pytest:",
        ),
        "```",
        "",
        "## cron.log (daily) tail markers",
        "",
        "```",
        *_tail_grep(
            PROJECT_ROOT / "monitor" / "cron.log",
            r"FAIL|ERROR|WARN|Pytest:|Metrics sent|BID Daily",
        ),
        "```",
        "",
        "## Agent instructions (read by Cursor Automation)",
        "",
        "1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).",
        "2. If only prod/network — do **not** change code; summarize only.",
        "3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).",
        "4. Keep changes minimal; do not touch secrets or monitor/.env.",
        "",
    ]
    return "\n".join(lines) + "\n"


def _push_to_github(content: str) -> None:
    if not GITHUB_PAT or not GITHUB_REPO:
        print("SKIP GitHub upload: нет GITHUB_PAT / GITHUB_REPO")
        return

    import urllib.error
    import urllib.request

    api = f"https://api.github.com/repos/{GITHUB_REPO}/contents/monitor/reports/latest.md"
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "bid-monitor-digest",
    }

    sha = None
    try:
        req = urllib.request.Request(api, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            sha = data.get("sha")
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            print(f"WARN: get contents HTTP {exc.code}: {exc.read()[:200]!r}")
            return

    body = {
        "message": f"chore(monitor): digest report {datetime.now(MSK).strftime('%Y-%m-%d %H:%M %Z')}",
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": "main",
    }
    if sha:
        body["sha"] = sha

    req = urllib.request.Request(
        api,
        data=json.dumps(body).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        print(f"GitHub updated: {result.get('content', {}).get('html_url', api)}")
    except urllib.error.HTTPError as exc:
        print(f"ERROR: GitHub upload HTTP {exc.code}: {exc.read()[:300]!r}")
        raise SystemExit(1) from exc


def main() -> int:
    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    push = "--push" in sys.argv or os.getenv("DIGEST_PUSH", "").lower() in ("1", "true", "yes")

    report = build_report(hours)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH} ({len(report)} bytes)")

    if push:
        _push_to_github(report)
    else:
        print("Local only (add --push to upload to GitHub)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
