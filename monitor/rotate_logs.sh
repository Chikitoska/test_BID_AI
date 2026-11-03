# Обрезать лог cron, если разросся (диск 15 ГБ). Подключать до exec в run_*.sh.
rotate_monitor_log() {
  local log="$1"
  local keep_bytes="${2:-2097152}"
  [ -f "$log" ] || return 0
  local sz
  sz=$(wc -c < "$log" 2>/dev/null || echo 0)
  sz=${sz// /}
  if [ "${sz:-0}" -gt "$keep_bytes" ]; then
    tail -c "$keep_bytes" "$log" > "${log}.tmp" && mv "${log}.tmp" "$log"
  fi
}
