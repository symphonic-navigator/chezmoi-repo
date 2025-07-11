#!/bin/bash

sleep 10

pidfile="/tmp/kitty-music-watchdog.pid"
if [[ -e "$pidfile" ]]; then
  echo "Watchdog already running (PID $(cat "$pidfile")), exiting."
  exit 1
fi

echo $$ >"$pidfile"
trap "rm -f '$pidfile'" EXIT

while true; do
  if ! hyprctl clients -j | jq -e '.[] | select(.class == "kitty-music")' >/dev/null; then
    echo "[$(date)] kitty-music not found, launching..."
    kitty --class kitty-music --session ~/.config/kitty/sessions/ncspot.conf &
  else
    echo "[$(date)] kitty-music is already running."
  fi
  sleep 5
done
