# BID monitor digest

- Generated: `2026-10-01T08:50:03.871088+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f14f91f feat(monitor): orange Grafana for autotest failures on all 3 runs`

## Influx volume

- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

(ошибок bid_failure за период нет)

## health.log (FAIL/ERROR/WARN/ImportError)

```
[FAIL] main_page 0 101ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 1/2
Health monitor finished in 11.2s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 82ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 11.3s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 171ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 3/2
Health monitor finished in 11.4s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 84ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 4/2
Health monitor finished in 11.2s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 126ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 5/2
Health monitor finished in 10.2s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))), повтор через 10 с (ещё 1 раз)…
[FAIL] main_page 0 15106ms HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 6/2
Health monitor finished in 35.7s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 251.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 250.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 260.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 261.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 260.7s
ERROR tests/lk/test_lk_accreditation.py::test_lk_accreditation_navigation - selenium.common.exceptions.TimeoutException: Message:
=== 18 passed, 1 skipped, 3 warnings, 1 error, 3 rerun in 893.52s (0:14:53) ====
LK pytest: 18/20 passed, failed=0, errors=1, skipped=1 in 894.9s
Failure events sent to InfluxDB (таблица Grafana)
Alert suppressed: lk_pytest failures look like autotest/UI flake (TimeoutException/assert/selector) — Grafana only; prod pulse is health every 5 min
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 256.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 258.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 254.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 262.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 255.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 254.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 261.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 258.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 286.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 258.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 257.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 250.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 260.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 253.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 256.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 256.8s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 12.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 11.1s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.2s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.4s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.8s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.4s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 10.0s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB (run_status=ok)
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

