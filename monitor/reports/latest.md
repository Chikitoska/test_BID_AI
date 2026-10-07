# BID monitor digest

- Generated: `2026-10-07T08:50:03.873154+03:00` (Europe/Moscow)
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
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 20975ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 133.5s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 27954ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 138.2s — FAIL (run_status=fail)
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[FAIL] lk_auth_login 16304ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Health monitor finished in 127.8s — FAIL (run_status=fail)
[FAIL] lk_auth_login 15206ms ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500
Metrics sent to InfluxDB (run_status=fail)
Alert suppressed: health fail streak 2/1
Health monitor finished in 80.6s — FAIL (run_status=fail)
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
[lk] 4xx/5xx на попытке 1/2: ЛК вернул HTTP error page после входа, URL: https://lk.bid.gazprom-neft.ru/error/500. Повтор через 90 с…
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 266.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 529.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 256.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 279.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 266.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 264.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 271.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 265.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 267.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 271.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 268.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 274.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 520.6s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 285.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 260.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 261.8s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 266.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 272.7s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 263.0s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.2s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 255.5s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 254.3s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 251.1s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 249.4s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 248.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 250.9s
LK pytest: 17/20 passed, failed=0, errors=0, skipped=3 in 252.6s
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.5s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 7.0s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.1s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.7s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 14.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 9.5s
Metrics sent to InfluxDB (run_status=ok)
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.8s
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

