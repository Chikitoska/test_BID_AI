"""Состояние алертов между прогонами (без спама в Telegram)."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

from monitor.config import ALERT_STATE_FILE


@dataclass
class AlertState:
    probe_ok: bool | None = None
    last_probe_fail_alert_at: float | None = None

    @classmethod
    def load(cls) -> AlertState:
        if not ALERT_STATE_FILE.exists():
            return cls()
        try:
            data = json.loads(ALERT_STATE_FILE.read_text(encoding="utf-8"))
            return cls(
                probe_ok=data.get("probe_ok"),
                last_probe_fail_alert_at=data.get("last_probe_fail_alert_at"),
            )
        except (json.JSONDecodeError, OSError, TypeError):
            return cls()

    def save(self) -> None:
        ALERT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        ALERT_STATE_FILE.write_text(
            json.dumps(
                {
                    "probe_ok": self.probe_ok,
                    "last_probe_fail_alert_at": self.last_probe_fail_alert_at,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def mark_probe_result(self, ok: bool) -> tuple[bool, bool]:
        """Возвращает (notify_failure, notify_recovery)."""
        was_ok = self.probe_ok
        notify_failure = False
        notify_recovery = False

        if ok:
            if was_ok is False:
                notify_recovery = True
            self.probe_ok = True
        else:
            self.probe_ok = False
            if was_ok is not False:
                notify_failure = True
                self.last_probe_fail_alert_at = time.time()
            elif self.last_probe_fail_alert_at is None:
                notify_failure = True
                self.last_probe_fail_alert_at = time.time()

        self.save()
        return notify_failure, notify_recovery

    def should_repeat_failure_alert(self, repeat_hours: float) -> bool:
        if self.probe_ok is not False:
            return False
        if self.last_probe_fail_alert_at is None:
            return True
        elapsed_hours = (time.time() - self.last_probe_fail_alert_at) / 3600
        if elapsed_hours >= repeat_hours:
            self.last_probe_fail_alert_at = time.time()
            self.save()
            return True
        return False
