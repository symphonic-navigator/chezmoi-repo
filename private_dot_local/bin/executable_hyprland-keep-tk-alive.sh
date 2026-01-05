#!/bin/bash

set -e
set -u

CLASS_NAME="tk-scratchpad"

QUERY=".[] | select(.class == \"$CLASS_NAME\")"

if ! hyprctl clients -j | jq -e "$QUERY" >/dev/null; then
  echo "[$(date)] $CLASS_NAME not found, launching..."
  ~/.local/share/multibrowser/start_multibrowser.sh --config ~/.multibrowser/tabs.json &
else
  echo "[$(date)] $CLASS_NAME is already running."
fi
