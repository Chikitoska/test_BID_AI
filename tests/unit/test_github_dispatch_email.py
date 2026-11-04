"""Email с VPS уходит даже если GitHub dispatch выключен."""

from monitor.checks import CheckResult
from monitor.github_dispatch import notify_github_on_failure


def _fail() -> CheckResult:
    return CheckResult(
        name="lk_auth_login",
        url="https://lk.bid.gazprom-neft.ru/error/500",
        method="UI",
        success=False,
        http_code=500,
        duration_ms=100.0,
        error="HTTP 500",
    )


def test_notify_sends_email_when_dispatch_disabled(monkeypatch) -> None:
    sent = {"email": 0}

    monkeypatch.setattr("monitor.github_dispatch.GITHUB_DISPATCH_ENABLED", False)

    def _email(**_kwargs):
        sent["email"] += 1
        return True

    monkeypatch.setattr("monitor.github_dispatch.send_vps_email_on_failure", _email)
    ok = notify_github_on_failure(
        run_type="health",
        http_results=[_fail()],
        failed_count=1,
        duration_sec=12.0,
    )
    assert ok is True
    assert sent["email"] == 1
