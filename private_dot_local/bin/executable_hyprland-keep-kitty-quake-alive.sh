#!/bin/bash

set -e
set -u

CLASS_NAME="kitty-quake"
SESSION_FILE=~/.config/kitty/sessions/quake.session
BASE_CONFIG_FILE=~/.config/kitty/kitty.conf
ADDITIONAL_CONFIG_FILE=~/.config/kitty/sessions/quake.conf

QUERY=".[] | select(.class == \"$CLASS_NAME\")"

if ! hyprctl clients -j | jq -e "$QUERY" >/dev/null; then
  echo "[$(date)] $CLASS_NAME not found, launching..."
  KITTY_SHELL_OVERRIDE=zellij kitty -c "$BASE_CONFIG_FILE" -c "$ADDITIONAL_CONFIG_FILE" --class "$CLASS_NAME" --session "$SESSION_FILE" &
else
  echo "[$(date)] $CLASS_NAME is already running."
fi
