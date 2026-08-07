"""Состояние алертов между прогонами (anti-flap, без спама в Telegram)."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

from monitor.config import ALERT_STATE_FILE


@dataclass
class AlertState:
    probe_ok: bool | None = None
    consecutive_probe_failures: int = 0
    incident_active: bool = False
    last_probe_fail_alert_at: float | None = None

    @classmethod
    def load(cls) -> AlertState:
        if not ALERT_STATE_FILE.exists():
            return cls()
        try:
            data = json.loads(ALERT_STATE_FILE.read_text(encoding="utf-8"))
            return cls(
                probe_ok=data.get("probe_ok"),
                consecutive_probe_failures=int(data.get("consecutive_probe_failures", 0)),
                incident_active=bool(data.get("incident_active", False)),
                last_probe_fail_alert_at=data.get("last_probe_fail_alert_at"),
            )
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            return cls()

    def save(self) -> None:
        ALERT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        ALERT_STATE_FILE.write_text(
            json.dumps(
                {
                    "probe_ok": self.probe_ok,
                    "consecutive_probe_failures": self.consecutive_probe_failures,
                    "incident_active": self.incident_active,
                    "last_probe_fail_alert_at": self.last_probe_fail_alert_at,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def evaluate_probe_alert(
        self,
        ok: bool,
        *,
        threshold: int,
        repeat_hours: float,
    ) -> tuple[bool, bool]:
        """Возвращает (send_failure_alert, send_recovery_alert)."""
        send_fail = False
        send_recovery = False

        if ok:
            if self.incident_active:
                send_recovery = True
            self.consecutive_probe_failures = 0
            self.probe_ok = True
            self.incident_active = False
        else:
            self.consecutive_probe_failures += 1
            self.probe_ok = False
            if self.consecutive_probe_failures >= threshold:
                if not self.incident_active:
                    send_fail = True
                    self.incident_active = True
                    self.last_probe_fail_alert_at = time.time()
                elif self._should_repeat(repeat_hours):
                    send_fail = True
                    self.last_probe_fail_alert_at = time.time()

        self.save()
        return send_fail, send_recovery

    def _should_repeat(self, repeat_hours: float) -> bool:
        if self.last_probe_fail_alert_at is None:
            return True
        elapsed_hours = (time.time() - self.last_probe_fail_alert_at) / 3600
        return elapsed_hours >= repeat_hours

    # legacy API for alert_policy full runs
    def mark_probe_result(self, ok: bool) -> tuple[bool, bool]:
        from monitor.config import MONITOR_ALERT_AFTER_FAILURES, TELEGRAM_ALERT_REPEAT_HOURS

        return self.evaluate_probe_alert(
            ok,
            threshold=MONITOR_ALERT_AFTER_FAILURES,
            repeat_hours=TELEGRAM_ALERT_REPEAT_HOURS,
        )

    def should_repeat_failure_alert(self, repeat_hours: float) -> bool:
        if not self.incident_active:
            return False
        return self._should_repeat(repeat_hours)
