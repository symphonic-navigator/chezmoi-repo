#!/bin/bash

set -e
set -u

CLASS_NAME="kitty-music"
SESSION_FILE=~/.config/kitty/sessions/ncspot.conf

QUERY=".[] | select(.class == \"$CLASS_NAME\")"

if ! hyprctl clients -j | jq -e "$QUERY" >/dev/null; then
  echo "[$(date)] $CLASS_NAME not found, launching..."
  kitty --class "$CLASS_NAME" --session "$SESSION_FILE" &
else
  echo "[$(date)] $CLASS_NAME is already running."
fi
