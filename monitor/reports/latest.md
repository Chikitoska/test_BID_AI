# BID monitor digest

- Generated: `2026-09-29T20:50:00.334977+03:00` (Europe/Moscow)
- Window: last **12** hours
- Host: VPS `/opt/test_BID_AI`
- Git HEAD: `f1df232 fix(grafana): clarify XLSX export link tooltip and help text`

## Influx volume

- `bid_failure`: 7 точек (~1д)
- `bid_lk_pytest`: 60 точек (~1д)
- `bid_lk_run`: 1152 точек (~1д)
- `bid_run`: 10 точек (~1д)

## Failures (bid_failure)

- `2026-09-29 13:30:36.417684+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)
- `2026-09-29 13:25:11.330185+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
- `2026-09-29 13:20:15.826383+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
- `2026-09-29 13:15:15.986686+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
- `2026-09-29 13:10:15.754224+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
- `2026-09-29 13:05:25.709823+00:00` | Лендинг + мин ЛК (5 мин) | `main_page` | Главная страница лендинга | HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
- `2026-09-29 13:34:59.228690+00:00` | Боевой прогон ЛК (2 ч) | `test_lk_accreditation_navigation` | tests/lk/test_lk_accreditation.py::test_lk_accreditation_navigation | tests/lk/test_lk_accreditation.py::test_lk_accreditation_navigation: selenium.common.exceptions.TimeoutException: Message

## health.log (FAIL/ERROR/WARN/ImportError)

```
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Read timed out. (read timeout=15)), повтор через 10 с (ещё 1 раз)…
main_page FAIL (HTTPSConnectionPool(host='bid.gazprom-neft.ru', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'bid.gazprom-neft.ru'. (_ssl.c:1000)")))), повтор через 10 с (ещё 1 раз)…
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
```

## lk-pytest.log (FAIL/ERROR/ImportError|failed=)

```
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 252.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 255.5s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 275.8s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 253.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 250.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 249.6s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 251.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 262.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 263.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 270.7s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 277.4s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 275.3s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 257.0s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 259.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 249.1s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 249.2s
LK pytest: 19/20 passed, failed=0, errors=0, skipped=1 in 249.0s
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
```

## cron.log (daily) tail markers

```
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 6.9s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.3s
Metrics sent to InfluxDB
=== BID Daily Monitor ===
Pytest: 39/39 passed, failed=0, errors=0 in 8.0s
Metrics sent to InfluxDB
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
```

## Agent instructions (read by Cursor Automation)

1. Classify each failure: **prod/network** (timeout, 5xx, DNS) vs **autotest bug** (selector, TimeoutException in UI, AssertionError, ImportError in tests).
2. If only prod/network — do **not** change code; summarize only.
3. If autotest bug — fix in repo and open a **Pull Request** to `main` (never push directly to main).
4. Keep changes minimal; do not touch secrets or monitor/.env.

