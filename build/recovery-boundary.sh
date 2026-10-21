# Only generated system staging is changed, never boot/recovery partitions.
remove_recovery_update() {
  [[ -d "$1" && "$1" != / ]] || return 1
  rm -f "$1/bin/install-recovery.sh" "$1/etc/install-recovery.sh" \
    "$1/recovery-from-boot.p"
}

assert_no_recovery_update() {
  [[ -d "$1" && "$1" != / ]] || return 1
  local candidate
  for candidate in bin/install-recovery.sh etc/install-recovery.sh recovery-from-boot.p; do
    if [[ -e "$1/$candidate" || -L "$1/$candidate" ]]; then
      echo "Refusing system image with automatic recovery updater: $candidate" >&2
      return 1
    fi
  done
}
