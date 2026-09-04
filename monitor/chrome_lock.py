"""Эксклюзивный доступ к Chrome/chromedriver между прогонами мониторинга."""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path

from monitor.config import PROJECT_ROOT

CHROME_LOCK_FILE = Path(
    os.getenv("CHROME_LOCK_FILE", str(PROJECT_ROOT / "monitor" / ".chrome.lock"))
)
CHROME_LOCK_POLL_SEC = float(os.getenv("CHROME_LOCK_POLL_SEC", "5"))
CHROME_LOCK_LOG_EVERY_SEC = float(os.getenv("CHROME_LOCK_LOG_EVERY_SEC", "30"))


class ChromeBusyError(RuntimeError):
    """Chrome занят другим прогоном дольше лимита ожидания."""


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _read_lock_holder(path: Path) -> tuple[str, int]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        owner = lines[0].strip() if lines else "?"
        pid = int(lines[1].strip()) if len(lines) > 1 else 0
        return owner, pid
    except (OSError, ValueError):
        return "?", 0


@contextmanager
def chrome_run_lock(*, owner: str, wait_sec: float):
    """Один Chrome-прогон на VPS (health vs lk pytest)."""
    CHROME_LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + max(wait_sec, 0)
    lock_fd = os.open(str(CHROME_LOCK_FILE), os.O_CREAT | os.O_RDWR, 0o644)

    acquired = False
    wait_logged_at = 0.0
    try:
        while True:
            try:
                import fcntl

                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
                break
            except BlockingIOError:
                holder_owner, holder_pid = _read_lock_holder(CHROME_LOCK_FILE)
                if holder_pid and not _pid_alive(holder_pid):
                    time.sleep(1)
                elif time.time() >= deadline:
                    raise ChromeBusyError(
                        f"Chrome занят прогоном «{holder_owner}» (pid={holder_pid}) "
                        f"— ждали {wait_sec:.0f} с"
                    )
                else:
                    now = time.time()
                    if now - wait_logged_at >= CHROME_LOCK_LOG_EVERY_SEC:
                        print(
                            f"[chrome-lock] ждём «{holder_owner}» (pid={holder_pid}), "
                            f"наш прогон: {owner}",
                            flush=True,
                        )
                        wait_logged_at = now
                    time.sleep(CHROME_LOCK_POLL_SEC)

        os.ftruncate(lock_fd, 0)
        os.lseek(lock_fd, 0, os.SEEK_SET)
        os.write(lock_fd, f"{owner}\n{os.getpid()}\n{time.time():.0f}\n".encode())
        print(f"[chrome-lock] acquired by {owner} (pid={os.getpid()})", flush=True)
        yield
    finally:
        if acquired:
            import fcntl

            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            print(f"[chrome-lock] released by {owner}", flush=True)
        os.close(lock_fd)
