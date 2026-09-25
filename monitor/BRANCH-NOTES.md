# Заметки по веткам monitor

- **`feature/grafana-errors-xlsx-export`** — HTTP Basic Auth выгрузка `bid_failure` → XLSX + ссылка Grafana `${__from}`/`${__to}`. Не мержить / не деплоить без отмашки. См. `monitor/EXPORT-ERRORS-XLSX.md`.
- **`feature/unified-spa-uuid`** — единый SPA UUID; merge/деплой только после релиза фронта и явной отмашки.
