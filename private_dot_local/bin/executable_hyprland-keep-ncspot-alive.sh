#!/bin/bash

set -e
set -u

CLASS_NAME="kitty-music"
SESSION_FILE=~/.config/kitty/sessions/ncspot.session
BASE_CONFIG_FILE=~/.config/kitty/kitty.conf
ADDITIONAL_CONFIG_FILE=~/.config/kitty/sessions/ncspot.conf

QUERY=".[] | select(.class == \"$CLASS_NAME\")"

if ! hyprctl clients -j | jq -e "$QUERY" >/dev/null; then
  echo "[$(date)] $CLASS_NAME not found, launching..."
  kitty -c "$BASE_CONFIG_FILE" -c "$ADDITIONAL_CONFIG_FILE" --class "$CLASS_NAME" --session "$SESSION_FILE" &
else
  echo "[$(date)] $CLASS_NAME is already running."
fi
