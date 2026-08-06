"""Отправка статуса probe на GitHub → workflow шлёт Telegram."""

from __future__ import annotations

import json

import requests

from monitor.alerts import failures_for_relay
from monitor.checks import CheckResult
from monitor.config import GITHUB_DISPATCH_ENABLED, GITHUB_PAT, GITHUB_REPO


def notify_github_probe_status(
    *,
    status: str,
    http_results: list[CheckResult],
    failed_count: int = 0,
    duration_sec: float = 0,
) -> bool:
    if not GITHUB_DISPATCH_ENABLED:
        print("GitHub dispatch skipped (add GITHUB_PAT to monitor/.env)")
        return False

    failed_checks = [item for item in http_results if not item.success]
    failures_json = json.dumps(failures_for_relay(failed_checks), ensure_ascii=False)

    url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
    payload = {
        "event_type": "bid-probe",
        "client_payload": {
            "status": status,
            "failed_count": failed_count,
            "duration_sec": round(duration_sec, 1),
            "failures_json": failures_json,
        },
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {GITHUB_PAT}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=15,
        )
        if response.status_code == 204:
            print("GitHub dispatch sent")
            return True
        print(f"WARN: GitHub dispatch HTTP {response.status_code}: {response.text[:200]}")
        return False
    except requests.RequestException as exc:
        print(f"WARN: GitHub dispatch failed: {exc}")
        return False
