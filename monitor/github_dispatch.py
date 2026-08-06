"""Отправка статуса probe на GitHub → workflow шлёт Telegram."""

from __future__ import annotations

import os

import requests

from monitor.config import GITHUB_DISPATCH_ENABLED, GITHUB_PAT, GITHUB_REPO


def notify_github_probe_status(
    *,
    status: str,
    failed_count: int = 0,
    duration_sec: float = 0,
) -> bool:
    if not GITHUB_DISPATCH_ENABLED:
        return False

    url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
    payload = {
        "event_type": "bid-probe",
        "client_payload": {
            "status": status,
            "failed_count": failed_count,
            "duration_sec": round(duration_sec, 1),
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
