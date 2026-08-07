"""Загрузка monitor/.env и корневого .env (как run_light.sh)."""

from __future__ import annotations

import os
from pathlib import Path


def load_project_env(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parents[1]
    for env_file in (root / "monitor" / ".env", root / ".env"):
        if not env_file.is_file():
            continue
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
